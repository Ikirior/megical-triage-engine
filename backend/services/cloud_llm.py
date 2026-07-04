from langchain_core.language_models import LLM
from requests import post
import os
import logging
from contracts import CloudLLMResponse

cloud_llm_logger = logging.Logger('CloudLLM')
CLOUD_MODEL_URL = os.getenv('CLOUD_MODEL_URL', None)

class CloudLLM(LLM):

    @property
    def _llm_type(self):
        return "LLM model to be running on a separate server."

    def _call(self, prompt, stop = None, run_manager = None, **kwargs):
        try:
            resObj = post(CLOUD_MODEL_URL, json={
                "prompt": prompt
            }, headers={
                'Content-Type': 'application/json'
            })
            resJson:CloudLLMResponse = resObj.json()
            return resJson['response']
        except:
            return 'CloudLLM ran into an exception and could not process the request.'
    
    @property
    def _identifying_params(self):
        return super()._identifying_params