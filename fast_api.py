'''
- run in cmd: fastapi run .\fast_api.py
'''

from typing import Any
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import torch
from model.hg_inference import HuggingfaceInference

app = FastAPI()
model = HuggingfaceInference(
    model_path=r"E:\Model\llama3.1")
stt, msg = model.load_model()


# # Tải mô hình và tokenizer
# model_name = r"E:\Model\llama3.1"
# model = Model(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model, tokenizer = setup_chat_format(model.model, tokenizer)
# # Đặt mô hình vào chế độ đánh giá
# model.eval()


def process_request(input_text):
    try:
        if not input_text:
            return
        if stt:
            output_text = model.infer(input_text)
            return output_text
        else:
            return
    except Exception as e:
        return


# This defines the data json format expected for the endpoint, change as needed
class TextInput(BaseModel):
    inputs: str
    parameters: dict[str, Any] | None


@app.get("/")
def status_gpu_check() -> dict[str, str]:
    gpu_msg = "Available" if torch.cuda.is_available() else "Unavailable"
    return {
        "status": "I am ALIVE!",
        "gpu": gpu_msg
    }


@app.post("/generate/")
async def generate_text(data: TextInput) -> dict[str, str]:
    try:
        # print(type(data))
        # print(data)
        params = data.parameters or {}
        # response = model(prompt=data.inputs, **params)
        response = process_request(data.inputs)
        # model_out = response['choices'][0]['text']
        return {"generated_text": response}
    except Exception as e:
        # print(type(data))
        # print(data)
        raise HTTPException(status_code=500, detail=len(str(e)))
