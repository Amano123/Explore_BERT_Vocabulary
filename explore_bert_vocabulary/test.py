#%%
from typing import List, Optional
from tokenizers.pre_tokenizers import BertPreTokenizer
from tokenizers.processors import BertProcessing
from tokenizers import NormalizedString, PreTokenizedString, Tokenizer
from tokenizers.implementations import BertWordPieceTokenizer
from tokenizers.pre_tokenizers import BertPreTokenizer, PreTokenizer
import MeCab
import textspan


#%%
tokenizer = BertWordPieceTokenizer(
    handle_chinese_chars=False,
    strip_accents=False,
    lowercase=False
)
# %%
class MecabPreTokenizer:
    def __init__(
        self,
        mecab_dict_path: Optional[str] = None,
    ):
        """Construct a custom PreTokenizer with MeCab for huggingface tokenizers."""

        mecab_option = (
            f"-Owakati -d {mecab_dict_path}"
            if mecab_dict_path is not None
            else "-Owakati"
        )
        self.mecab = MeCab.Tagger(mecab_option)

    def tokenize(self, sequence: str) -> List[str]:
        return self.mecab.parse(sequence).strip().split(" ")

    def custom_split(
        self, i: int, normalized_string: NormalizedString
    ) -> List[NormalizedString]:
        """See. https://github.com/huggingface/tokenizers/blob/b24a2fc/bindings/python/examples/custom_components.py"""
        text = str(normalized_string)
        tokens = self.tokenize(text)
        tokens_spans = textspan.get_original_spans(tokens, text)
        return [
            normalized_string[st:ed]  # type: ignore
            for char_spans in tokens_spans
            for st, ed in char_spans
        ]

    def pre_tokenize(self, pretok: PreTokenizedString):
        pretok.split(self.custom_split)

# %%
tokenizer._tokenizer.pre_tokenizer = PreTokenizer.custom(MecabPreTokenizer())  # type: ignore

# %%
text: List[str] = []
with open("/home/yo/workspace/poli.txt", "r") as f:
    for line in f:
        cur_line = line.strip()
        if cur_line:
            text.append(cur_line)
# %%
tokenizer.train_from_iterator(
    text,  # type: ignore
    limit_alphabet=30000,
    min_frequency=1,
    vocab_size=30000
)
# %%
tokenizer._tokenizer.pre_tokenizer = BertPreTokenizer()  # type: ignore

tokenizer.post_processor = \
    BertProcessing(
        sep=('[SEP]', tokenizer.token_to_id('[SEP]')),
        cls=('[CLS]', tokenizer.token_to_id('[CLS]')),
    )
tokenizer.save("./sample")
# %%
tokenizer.train
# %%
