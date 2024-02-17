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