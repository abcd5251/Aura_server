from fastapi import FastAPI, Request
import json
from models.model import OpenAIModel
from models.schema import InputData, QueryNews
from utils.constants import *
from prompts.summarize import summarize_prompt
from prompts.planner import planner_prompt
from prompts.qa import qa_prompt
from models.model import OpenAIModel
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

# @app.post("/defiInfo")
# async def process_simple_input(data: InputData):
#     need_info = INFORMATION
#     qa_model_instance = OpenAIModel(system_prompt="You are a helpful assistant, based on the diamond INFORMATION below, Please answer the QUESTION!", temperature=0)
#     prompt = f"INFORMATION:{need_info}\nQUESTION:{data.input_text}\nOUTPUT:"
#     output, input_token, output_token = qa_model_instance.generate_string_text(prompt)

#     print("ooo", output)
#     return {"result": output}

@app.post("/defiInfo")
async def process_simple_input(data: InputData):
    
    planner_model_instance = OpenAIModel(system_prompt=planner_prompt, temperature=0)
    prompt = f"INPUT_TEXT:{data.input_text}\nOUTPUT:"
    output, input_token, output_token = planner_model_instance.generate_text(prompt)
    intent_type = json.loads(output)["intent_type"]
    
    if intent_type == "low_risk_strategy":
        low_risk_return = """
        Here are some low risk strategies:
            1. Ankr (Flow)
            2. StakedCelo (Celo)
        """
        return {"result": f"{low_risk_return}"}
    
    elif intent_type == "high_risk_strategy":
        high_risk_return = """
        Here are some high risk strategies:
            1. Provide liquidity to Uniswap pool (Celo)
            2. Provide liquidity to StableKitty pool (Flow)
        """
        return {"result": f"{high_risk_return}" }
    
    elif intent_type == "question" or intent_type == "chat":
        system_prompt = "You are a helpful assistant. Given an INPUT_TEXT, Please answer INPUT_TEXT!"
        question_model_instance = OpenAIModel(system_prompt=system_prompt, temperature=0)
        prompt = f"INPUT_TEXT:{data.input_text}\nOUTPUT:"
        content, annotations, input_tokens_length, output_tokens_length = question_model_instance.generate_with_web_annotations(prompt)
        
        #total_information = search_from_qdrant(qclient, query_embedding, k=10)
        # need_info = ""
        # for infor in total_information:
        #     need_info += infor.payload["content"]
        #     need_info += "\n"
        
        information_all = content + "\n" + CONTENT 
        qa_model_instance = OpenAIModel(system_prompt=qa_prompt, temperature=0)
        prompt = f"INFORMATION:{information_all}\nQUESTION:{data.input_text}\nOUTPUT:"
        output, input_token, output_token = qa_model_instance.generate_string_text(prompt)
        
        return {"result": f"{output}"}
    elif intent_type == "latest_news":
        system_prompt = "You are a helpful assistant. Given an INPUT_TEXT, Please answer INPUT_TEXT!"
        question_model_instance = OpenAIModel(system_prompt=system_prompt, temperature=0)
        prompt = f"INPUT_TEXT:{data.input_text}\nOUTPUT:"
        content, annotations, input_tokens_length, output_tokens_length = question_model_instance.generate_with_web_annotations(prompt)
    
        return {"result": content}
