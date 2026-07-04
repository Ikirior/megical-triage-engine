from fastapi import FastAPI
from http import HTTPStatus
from pydantic import BaseModel
from langchain_ollama import OllamaLLM

app = FastAPI()

# uvicorn api:app --host 0.0.0.0 --port 80 # PS.: needs root to be able to bind to port 80

OLLAMA_MODEL = 'medgemma-q6-limitado'
OLLAMA_BASE_URL = 'http://localhost:11434'

class CloudLLMRequest(BaseModel):
    prompt: str = None

class CloudLLMResponse(BaseModel):
    response: str = None


@app.post("/", response_model = CloudLLMResponse, status_code = HTTPStatus.OK)
async def cloud_llm(req: CloudLLMRequest):
    """
    Runs a model, receives a prompt and returns its response.

    Args:
        prompt: a string with a prompt.

    Returns:
        An object with a 'response' key which contains the LLM response.

    """

    llm = OllamaLLM(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.1
    )
    
    res = await llm.ainvoke(req.prompt)
    
    return {"response": res}