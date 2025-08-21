from transformers import pipeline
from extractor import *
from glossary import *

# Try this model - it often has better default labeling
ner_pipeline = pipeline(
    'ner',
    model='uer/roberta-base-finetuned-cluener2020-chinese',
    aggregation_strategy="simple"
)


chunk = ""
with open('../../../Database/cybergame/raw/chapter_16.txt', 'r') as f:
    text = f.read()

model = HuggingFaceModel(ner_pipeline)

extractor =  Extractor(model, 450)

def chapter_name_to_num(name : str) -> int:
    return int(name[8:-4])

def normalizer(word : str) -> str:
    return word.replace(' ', '').strip()


glossary = GlossaryBuilder(extractor, chapter_name_to_num=chapter_name_to_num, normalizer=normalizer)

chapters = load_chapters('../../../Database/cybergame/raw/*')

result = glossary.preprocess(chapters, wordy=True)