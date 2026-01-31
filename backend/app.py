from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def first():
    return {"msg": "hi"}