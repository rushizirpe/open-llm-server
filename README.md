
# FastAPI Embed API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python)
![Transformers](https://img.shields.io/badge/Transformers-FFD700?style=flat&logo=transformers)

This repository contains a FastAPI application for generating text embeddings and chat completions using models from Hugging Face's Transformers library and the LLaMA model from Meta AI.

## Overview

The FastAPI application provides endpoints for:
- Generating embeddings for input texts.
- Generating chat completions based on conversation history.

The application leverages pre-trained models from Hugging Face and the LLaMA model for these tasks.

## Setup

### Prerequisites

- Docker
- Git

### Clone the Repository

```sh
git clone https://github.com/rushizirpe/open-llm-server.git
cd open-llm-server
```

### Build the Docker Image

```sh
docker build -t open-llm-server .
```

### Run the Docker Container

```sh
docker run -it -p 8888:8888 open-llm-server:latest
```

## Endpoints

### Health Check

- **URL**: `/`
- **Method**: `GET`
- **Description**: Check the status of the API and the availability of a GPU.

**Example Response**:
```json
{
    "status": "I am ALIVE!",
    "gpu": "Available"
}
```

### Generate Embeddings

- **URL**: `/v1/embeddings`
- **Method**: `POST`
- **Description**: Generate embeddings for a list of input texts using a specified model.

**Request Body**:
```json
{
    "input": ["Hello world", "How are you?"],
    "model": "bert-base-uncased"
}
```

**Example Response**:
```json
{
    "object": "list",
    "data": [
        {"embedding": [...], "index": 0},
        {"embedding": [...], "index": 1}
    ],
    "model": "bert-base-uncased",
    "usage": {"total_tokens": 5}
}
```

### Generate Chat Completions

- **URL**: `/v1/chat/completions`
- **Method**: `POST`
- **Description**: Generate chat completions based on conversation history using a specified model.

**Request Body**:
```json
{
    "model": "gpt-2",
    "messages": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there! How can I help you today?"}
    ],
    "max_tokens": 150,
    "temperature": 1.0,
    "top_p": 1.0,
    "n": 1,
    "stop": null
}
```

**Example Response**:
```json
{
    "choices": [
        {"index": 0, "text": "I can help you with a variety of tasks, such as ..."}
    ]
}
```

## Development

### Install Dependencies

Create a virtual environment and install the dependencies:

```sh
conda create --name endpoints-api python=3.10
conda activate endpoints-api
pip install -r requirements.txt
```

### Run Locally

```sh
uvicorn app:app --host 0.0.0.0 --port 8888
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any inquiries or support, please contact [me](mailto:zirperishi@gmail.com).
