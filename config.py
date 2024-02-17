from pydantic import BaseModel

# Shcema for the document
# TODO - Add more fields (e.g. date, author, etc.)
class Document(BaseModel):
  title: str
  content: str

# Configuration file for elasticsearch
es_config = {
  "settings": {
    "analysis": {
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "stemmer", "asciifolding"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
        "title": {"type": "text", "analyzer": "my_analyzer"},
        "content": {"type": "text", "analyzer": "english"}
    }
  }
}