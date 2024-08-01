# Introduction

Deploy a Large Language Model (LLM) and host an API for multiple users.

Load the LLM using: transformer or llama-cpp

Build the API using: Flask or FastAPI

## Detailed Description

1. **Deploying the Large Language Model (LLM):**
   - **Transformer:** Use the `transformers` library by Hugging Face to load and deploy the language model. This library supports many advanced models such as GPT-3, BERT, and more, making it easy to apply to natural language processing tasks.
   - **Llama-cpp:** Use `llama-cpp` to deploy the language model. This powerful tool optimizes the processing and deployment of large language models with high performance and accuracy.

2. **Building the API:**
   - **Flask:** A lightweight and flexible microframework suitable for building simple and quick APIs. Flask provides the necessary tools to develop web applications without overloading with unnecessary features.
   - **FastAPI:** A modern and fast framework designed to easily build high-performance APIs. FastAPI uses advanced Python features like type hints to create clean, readable, and maintainable code.

## Installation
1. Clone the vedastr repository.

```shell
git clone https://github.com/cvQuan28/build_llm_api.git
cd build_llm_api
```

2. Install dependencies.

```shell
pip install -r requirements.txt
```
## Quick start
1. **Run server**

- Use Flask to build the API endpoints:
```shell
python app.py
```
- Alternatively, use FastAPI to build high-performance API endpoints:
```shell
python fast_api.py
```

2. Test API

- Test multiple requests sent to the server at the same time.

```shell
python user_test.py
```

- Test with chat ui:

```shell
python web_app_streamlit.py
```

## Features
- **Optimize serving and increase processing performance.**
   
- **Build docker** 
