from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')
text = "Barack Obama was the president of the United States."
result = nlp.annotate(text, properties={'annotators': 'ner', 'outputFormat': 'json'})
print(result['sentences'][0]['entitymentions'])
