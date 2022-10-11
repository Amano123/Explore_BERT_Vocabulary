#%%
import spacy

nlp: spacy.Language = spacy.load('ja_ginza')
# %%
text: str = '主要な目標として、中小河川では、護岸や調節池を整備することにより、過去の水害と同規模の降雨による溢水の九割を解消し、残りの一割についても被害の程度を大幅に減少させること、東部低地河川では、伊勢湾台風級の高潮に対する対策や、阪神・淡路大震災を踏まえた外郭堤防と内部護岸などの耐震対策を完了させること、土砂災害の危険のある多摩地域などでは、住民の速やかな避難体制を確立するため、警戒区域の指定や警戒情報を提供するソフト対策を構築するとともに、避難所が立地するすべての危険箇所の安全対策を進めていくこと、さらに、これらの事業を進めるに当たっては、スーパー堤防の整備や多自然川づくりなどにより、景観や緑の視点を取り入れた、安全で潤いのある水辺空間を創出していくことなど、こうした目標を設定し、その達成を目指して積極的に事業に取り組んでまいります。'
doc: spacy.tokens.doc.Doc = nlp(text)
# %%
from spacy import displacy

# 依存関係の可視化（jupyter=TrueとすることでNotebook上で表示できる）
displacy.render(doc, style="dep", options={"compact":True},  jupyter=True)
# %%
svg = displacy.render(doc, style='dep', options={'distance': 200, }, jupyter=False)
from pathlib import Path
output_path = Path("./dependency_plot.svg") # you can keep there only "dependency_plot.svg" if you want to save it in the same folder where you run the script 
output_path.open("w", encoding="utf-8").write(svg)

# %%
