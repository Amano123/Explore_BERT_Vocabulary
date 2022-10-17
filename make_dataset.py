"""このプログラムは、Wiki40をダウンロードすることを行う。"""
# %%
import os
import tensorflow_datasets as tfds
# from progressbar import progressbar as
from tqdm.std import tqdm
# from bunkai import Bunkai

import functools

from ja_sentence_segmenter.common.pipeline import make_pipeline
from ja_sentence_segmenter.concatenate.simple_concatenator import concatenate_matching
from ja_sentence_segmenter.normalize.neologd_normalizer import normalize
from ja_sentence_segmenter.split.simple_splitter import split_newline, split_punctuation

split_punc2 = functools.partial(split_punctuation, punctuations=r"。")
concat_tail_te = functools.partial(
    concatenate_matching, former_matching_rule=r"^(?P<result>.+)(て)$", remove_former_matched=False)
segmenter = make_pipeline(normalize, split_newline,
                          concat_tail_te, split_punc2)

DATASET_TAGS = ['test', 'train', 'validation']
START_ARTICLE_TAG = '_START_ARTICLE_'
START_PARAGRAPH_TAG = '_START_PARAGRAPH_'
NEW_LINE_TAG = '_NEWLINE_'
# %%


def split_article(article_text: str) -> list:
    "aaa"
    paragraphs = []
    lines = article_text.split('\n')
    for i in range(2, len(lines), 2):
        if lines[i-1] == START_PARAGRAPH_TAG:
            paragraphs.append(lines[i].split(NEW_LINE_TAG))
    return paragraphs


def get_wiki40b_dataset(tag: str):
    """dawnload wiki40b dataset(corpus)"""
    wiki40b_ja = tfds.builder('wiki40b/ja')
    wiki40b_ja.download_and_prepare()
    total_exsamples = wiki40b_ja.info.splits[tag].num_examples
    wiki = wiki40b_ja.as_dataset(split=tag)
    wiki_info = wiki40b_ja.info
    all_sentences = []
    # bunkai = Bunkai()
    print(f"start: wiki40b【{tag}】dataset download.")
    for page in tqdm(wiki, total=total_exsamples):
        # Wikidata id (e.g. Q11331136)
        # wikidata_id = page["wikidata_id"].numpy().decode('utf-8')
        # print(wikidata_id)
        # Version id (e.g. 1848243370795951995)
        # version_id = page["version_id"].numpy().decode('utf-8')
        # print(version_id)
        document = page["text"].numpy().decode('utf-8')
        # 段落
        paragraphs = split_article(document)
        all_sentences.append(START_ARTICLE_TAG)
        for paragraph in paragraphs:
            all_sentences.append(START_PARAGRAPH_TAG)
            for sentences in paragraph:
                # for sentence in bunkai(sentences):
                for sentence in segmenter(sentences):
                    if sentence:
                        all_sentences.append(sentence)
    return wiki_info, all_sentences


def main() -> None:
    for tag in DATASET_TAGS:
        wiki_info, all_sentences = get_wiki40b_dataset(tag)
        output_dir = "./datasets/corpus"
        os.makedirs(output_dir, exist_ok=True)

        with open(os.path.join(output_dir, 'dataset_info_{}.json'.format(tag)), 'w') as f:
            f.write(wiki_info.as_json)

        with open(os.path.join(output_dir, 'ja_wiki40b_{}.txt'.format(tag)), 'w') as f:
            for sentence in all_sentences:
                f.write(sentence + '\n')


# %%
if __name__ == '__main__':
    main()
