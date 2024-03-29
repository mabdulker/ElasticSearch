from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch, helpers
from app.config import es_config, Document
from dotenv import load_dotenv
import os
from typing import List
import uuid
from openai import OpenAI

app = FastAPI()
es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.get("/")
def read_root():
    return {"message": "Welcome to MyDocuments API"}


@app.put("/mydocuments/")
async def index_settings():
    try:
        response = es.indices.create(index="mydocuments", body=es_config)
        return {
            "acknowledged": response["acknowledged"],
            "index": response["index"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


###
# * Method for posting documents to elasticsearch
# TODO - add convenient way to upload from computer e.g. text file folder
###
@app.post("/bulk-upload/")
async def add_document(documents: List[Document]):
    docs = [
        {
            "_index": "mydocuments",
            # Moving id generation to the client side for bulk upload
            "_id": str(uuid.uuid4()),
            "_source": {"title": doc.title, "content": doc.content},
        }
        for doc in documents
    ]
    try:
        successes, errors = helpers.bulk(es, docs, raise_on_error=False)
        return {
            "doc_ids": [doc["_id"] for doc in docs],
            "successes": successes,
            "errors": errors,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


###
# * Method for retreiving document content from elasticsearch
###
@app.get("/mydocuments/{document_id}")
async def get_document(document_id: str):
    try:
        response = es.get(index="mydocuments", id=document_id)
        return response["_source"]
    except Exception as e:
        raise HTTPException(
            status_code=404, detail=f"Document not found ({e})"
        )


###
# * Method for searching documents in elasticsearch
###
@app.get("/search/")
def query_document(query: str):
    try:
        response = es.search(
            index="mydocuments",
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^2", "content"],
                    }
                },
                "size": 3,
            },
        )
        if response["hits"]["total"]["value"] == 0:
            return {False: "No document relevant to your query found."}
        hit_ids = [hit["_id"] for hit in response["hits"]["hits"]]
        return {True: hit_ids}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


###
# * LLM powered reply
###
@app.get("/llm_search/")
async def llm_search(query: str):
    documents = query_document(query)
    # Checking if relevant documents exist
    if True in documents:
        content = []
        for doc_id in documents[True]:
            doc = await get_document(doc_id)
            content.append(str(doc))
    else:
        return documents[False]

    content = "\n".join(content)
    prompt = f"{content}\n\n{query}\n\nAnswer:"

    try:
        response = client.chat.completions.create(
            # response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that gives concise \
                      responses based on the content that you're given only",
                },
                {"role": "user", "content": prompt},
            ],
        )
        answer = response.choices[0].message.content
        return {"answer": answer, "documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
