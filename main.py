from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch, helpers
from config import es_config, Document
from typing import List
import uuid

app = FastAPI()
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


@app.put("/mydocuments/")
async def index_settings(): 
  try:
    response = es.indices.create(index="mydocuments", body=es_config)
    return {"acknowledged": response["acknowledged"], "index": response["index"]}
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))


###
# * Method for posting documents to elasticsearch
###
@app.post("/bulk-upload/")
async def add_document(documents: List[Document]):
  docs = [
    {
      "_index": "mydocuments",
      # Moving id generation to the client side for bulk upload
      "_id": str(uuid.uuid4()),
      "_source": {
        "title": doc.title,
        "content": doc.content
      }
    }
    for doc in documents
  ]
  
  try:
    successes, errors = helpers.bulk(es, docs, raise_on_error=False)
    return {"doc_ids": [doc["_id"] for doc in docs], "successes": successes, "errors": errors}
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e)) 
 
  
###
# * Method for retreiving document content from elasticsearch 
###
@app.get("/mycoduments/{document_id}")
def get_document(document_id: str):
  try:
    response = es.get(index="mydocuments", id=document_id)
    return response["_source"]
  except Exception as e:
    raise HTTPException(status_code=404, detail="Document not found")
  

###
# * Method for searching documents in elasticsearch
###
@app.get("/mydocuments/")
def search_documents(query: str):
  try:
    response = es.search(
      index="mydocuments", 
      body={
        "query": {
          "match": {
            "content": query
            }
          },
        "size": 3
        }
      )
    if response["hits"]["total"]["value"] == 0:
      return {"No document relevant to your query found."}
    hit_ids = [hit['_id'] for hit in response["hits"]["hits"]]
    return hit_ids
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))