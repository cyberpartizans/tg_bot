from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    LOC,
    ORG,
    
    NamesExtractor,
    DatesExtractor,
    MoneyExtractor,
    AddrExtractor,

    Doc
)

from deeppavlov import configs, build_model

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)
dates_extractor = DatesExtractor(morph_vocab)
money_extractor = MoneyExtractor(morph_vocab)
addr_extractor = AddrExtractor(morph_vocab)

# deeppavlov_bert_rus = build_model(configs.ner.ner_rus_bert, download=True)
# deeppavlov_bert_mult = build_model(configs.ner.ner_ontonotes_bert_mult, 
                                         # download=True)

def natasha_analyze_message(message: str) -> dict:
  '''
  Analyze message using Natasha NER and returns dict which contains of 
  `Location`, `Person`, `Organization`, `Date`. 
  If something not found, than value will be empty
  '''

  message_keyparts = {
      "Person" : [],
      "Location" : [],
      "Organization" : []
  }

  doc = Doc(message)
  doc.segment(segmenter)
  doc.tag_morph(morph_tagger)
  doc.tag_ner(ner_tagger)
  for span in doc.spans:
    span.normalize(morph_vocab)
  
  for span in doc.spans:
    if span.type == PER:
        span.extract_fact(names_extractor)
    elif span.type == LOC:
        span.extract_fact(addr_extractor)
    span.extract_fact(dates_extractor)
  
  for span in doc.spans:
    if span.type == PER:
      message_keyparts["Person"].append(span.normal)
    elif span.type == LOC:
      if span.start != 0 and text[span.start - 1] == '.':
        while text[span.start - 1] != ' ':
          span.start -= 1
      try_get_address = addr_extractor.find(text[span.start : span.stop])
      if try_get_address is not None:
        message_keyparts["Location"].append(try_get_address.fact.as_json())
      else:
        message_keyparts["Location"].append(text[span.start : span.stop])
    elif span.type == ORG:
      message_keyparts["Organization"].append(span.normal)
    
  return message_keyparts

def deeppavlov_analyze_message(message: str) -> dict:
  '''
  Analyze message using DeepPavlov NER and returns dict which contains of 
  `Location`, `Person`, `Organization`, `Date`. 
  If something not found, than value will be empty
  '''

  message_keyparts = {
      "Person" : {
          'BERT RUS' : [],
          'Ontonotes BERT MULT' : []
      },
      "Location" : {
          'BERT RUS' : [],
          'Ontonotes BERT MULT' : []
      },
      "Organization" : {
          'BERT RUS' : [],
          'Ontonotes BERT MULT' : []
      },
      "Date" : {
          'BERT RUS' : [],
          'Ontonotes BERT MULT' : []
      }
  }

  convert_pavlov_type_to_keyparts = {
      "LOC" : "Location",
      "GPE" : "Location",
      "PERSON" : "Person",
      "ORG" : "Organization",
      "PER" : "Person",
      "ORGANIZATION" : "Organization",
      "LOCATION" : "Location",
      "DATE": "Date",
      "TIME" : "Date"
  }

  result_from_bert_rus = deeppavlov_bert_rus([message])
  result_from_bert_mult = deeppavlov_bert_mult([message])

  for results, type_of_model in zip([result_from_bert_rus, result_from_bert_mult],
                                    ["BERT RUS", "Ontonotes BERT MULT"]):
    entity = ""
    delimeter = " "
    previous_type = 'O'
    for i, type_of_entity in enumerate(results[1][0]):# 1 -- list of list of type
      if type_of_entity.find('B') != -1:
        if previous_type != 'O' and\
         previous_type[2:] in convert_pavlov_type_to_keyparts.keys():
          message_keyparts[convert_pavlov_type_to_keyparts[previous_type[2:]]]\
            [type_of_model].append(entity)
        entity = results[0][0][i]
        previous_type = type_of_entity
      elif type_of_entity.find('I') != -1:
        entity = delim.join([entity, results[0][0][i]])

    if results[1][0][-1] == 'O'and previous_type != 'O':
      message_keyparts[convert_pavlov_type_to_keyparts[previous_type[2:]]]\
        [type_of_model].append(entity)

  return message_keyparts

def analyze_message(message: str) -> dict:
  '''
  Analyze message and returns dict which contains of 
  `Location`, `Person`, `Organization`, `Date`. 
  If something not found, than value will be empty.
  Currently function uses Natasha and DeepPavlov NRE.
  '''

  message_keyparts = {
      'Location' : {
          'Natasha' : [],
          'DeepPavlov' : []
      },
      'Person' : {
          'Natasha' : [],
          'DeepPavlov' : []
      },
      'Organization' : {
          'Natasha' : [],
          'DeepPavlov' : []
      },
      'Date' : {
          'DeepPavlov': []
      }
  }
  
  keyparts_by_natasha = natasha_analyze_message(message)
  keyparts_by_pavlov = {} #deeppavlov_analyze_message(message)

  for name, keyparts in zip(["Natasha", "DeepPavlov"],
                            [keyparts_by_natasha, keyparts_by_pavlov]):
    for key in keyparts.keys():
      message_keyparts[key][name] = keyparts[key]

  return message_keyparts
