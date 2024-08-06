

![Docker](https://img.shields.io/badge/Docker-ffffff?style=for-the-badge&logo=docker)&nbsp;&nbsp;
![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)&nbsp;&nbsp;
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)&nbsp;&nbsp;
![Git](https://img.shields.io/badge/Git-grey?style=for-the-badge&logo=git)&nbsp;&nbsp;
![Licence](https://img.shields.io/github/license/rushizirpe/open-llm-server?style=for-the-badge&)&nbsp;&nbsp;
![Issues](https://img.shields.io/github/issues/rushizirpe/open-llm-server?style=for-the-badge&)&nbsp;&nbsp;

# Open LLM

This Open LLM Framework serves as a powerful and flexible tool for generating text embeddings and chat completions using state-of-the-art and open source language models. By leveraging models Transformers, this enables various natural language processing (NLP) tasks to be performed via simple HTTP endpoints similar to openai endpoints.


### 

- Provides an easy-to-use API interface to leverage powerful NLP models locally without needing deep expertise in machine learning.

- {TD - Allow integration with various applications, including chatbots, content creation tools, and recommendation systems.}
- Supports multiple models from Transformers library, enabling diverse NLP tasks.
- Utilizes GPU acceleration when available to enhance processing speed and efficiency.
- Tunneling to give access to other endpoints
- Reduces dependency on external APIs, potentially lowering operational costs.
- Enables control over the computational resources used, optimizing for cost and performance.

&zwj;
# **Notebooks**
For GraphRAG:  
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1uhFDnih1WKrSRQHisU-L6xw6coapgR51?usp=sharing.)
- More Coming Soon...
# **Usage**
- ### Prerequisites

    - Python >= 3.10
    - Docker >= 23.0.3

-  ### Source

```sh
# Clone the Repository
git clone https://github.com/rushizirpe/open-llm-server.git

# Install Dependencies
cd open-llm-server
pip install -r requirements.txt

#  Launch server
python src/launch.py start --host 127.0.0.1 --port 8888 --reload
```

-  ### DockerHub

```sh
# Pull Docker Image
docker pull thisisrishi/open-llm-server
```

```sh
# Run Docker
docker run -it -p 8888:8888 thisisrishi/open-llm-server:latest
```
OR
```sh
# Run on Custom Port
docker run -e PORT=8000 -p 8000:8000 thisisrishi/open-llm-server:latest
```
OR
```sh
# Create and Start Container
docker compose up
```
&zwj;
# **Endpoints**

- ## **Health Check**

    - **URL**: `/`
    - **Method**: `GET`
    - **Description**: Check the status of the API and the availability of a GPU.

- **Usage**
```sh
curl http://localhost:8888/
```
- **Response**:
```json
{
    "status": "System Status: Operational",
    "gpu": "Available",
    "gpu_details": {
        "GPU 0": {
            "compute_capability": "(8, 9)",
            "device_name": "NVIDIA L4"
            }
    }
}

```

- ## **Embeddings**

    - **URL**: `/v1/embeddings`
    - **Method**: `POST`
    - **Description**: Generate embeddings for a list of input texts using a specified model.

- **Usage**
```sh
curl http://localhost:8888/v1/embeddings \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer DUMMY_KEY"  \
    -d '{"input": "the quick brown fox", "model": "nomic-ai/nomic-embed-text-v1.5"}' 
```

- **Response**:
```json
{
    "object": "list",
    "data": [
        {"embedding": [0.56324344, 0.25775233, -0.123355], "index": 0},
        {"embedding": [0.30823462, -0.23636326, 0.543345], "index": 1}
    ],
    "model": "nomic-ai/nomic-embed-text-v1.5",
    "usage": {"total_tokens": 5}
}
```

- ## **Chat Completions**

    - **URL**: `/v1/chat/completions`
    - **Method**: `POST`
    - **Description**: Generate chat completions based on conversation history using a specified model.


- **Request Body**:
```json
{
    "model": "openai-community/gpt2",
    "messages": [
        {"role": "user", "content": "Hi!"},
        {"role": "assistant", "content": "Hi there! How can I help you today?"}
    ],
    "max_tokens": 150,
    "temperature": 0.7,
    "top_p": 1.0,
    "n": 1,
    "stop": null
}
```

- **Usage**
```sh
curl http://localhost:8888/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer DUMMY_KEY" \
    -d '{"model": "openai-community/gpt2","messages": [{"role": "user", "content": "Hi!"}],"max_tokens": 150,"temperature": 0.7}'
```

- **Response**:
```json
{
    "choices": [
        {"index": 0, "text": "Hello, I can help you with a variety of tasks, such as ..."}
    ]
}
```

## License

&nbsp;&nbsp; This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

&nbsp;&nbsp;Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

&nbsp;&nbsp;For any inquiries or support, please [contact me](mailto:zirperishi@gmail.com).
