from transformers import (
    BertTokenizerFast,
    AutoModel
)

tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
model = AutoModel.from_pretrained('ckiplab/albert-tiny-chinese-ner')

print(model.config.id2label)