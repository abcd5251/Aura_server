from fastapi import FastAPI, Request
import json
#from crawl4ai import *
from embedding import get_client, get_embedding, search_from_qdrant
from models.model import OpenAIModel
from models.schema import InputData, QueryNews
from prompts.summarize import summarize_prompt
from prompts.planner import planner_prompt
from prompts.qa import qa_prompt
from models.model import OpenAIModel
from utils.constants import INFORMATION
from fastapi.middleware.cors import CORSMiddleware
# Initialize FastAPI app
app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/defiInfo")
async def process_simple_input(data: InputData):
    need_info = INFORMATION
    qa_model_instance = OpenAIModel(system_prompt="You are a helpful assistant, based on the diamond INFORMATION below, Please answer the QUESTION!", temperature=0)
    prompt = f"INFORMATION:{need_info}\nQUESTION:{data.input_text}\nOUTPUT:"
    output, input_token, output_token = qa_model_instance.generate_string_text(prompt)

    print("ooo", output)
    return {"result": output}


