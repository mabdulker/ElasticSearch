from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch
from pydantic import BaseModel

app = FastAPI()
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

@app.get("/")
def read_root():
  return {"Hello": "World"}

class Document(BaseModel):
  title: str
  content: str


###
# * Method for posting documents to elasticsearch
# TODO - Add bulk upload 
###
@app.post("/mydocuments/")
def add_document(doc: Document):
  try:
    response = es.index(index="mydocuments", body=doc.dict())
    return {"document_id": response["_id"]}
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