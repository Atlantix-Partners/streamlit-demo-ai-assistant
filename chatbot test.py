
import os
import base64
from openai import AzureOpenAI
from IPython.display import display, HTML
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

endpoint = os.getenv("ENDPOINT_URL")
deployment = os.getenv("DEPLOYMENT_NAME")
search_endpoint = os.getenv("SEARCH_ENDPOINT")
search_key = os.getenv("SEARCH_KEY")
search_index = os.getenv("SEARCH_INDEX_NAME")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

print("AZURE_OPENAI_API_KEY")


# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

# Prepare the chat prompt
chat_prompt = [
    {
        "role": "system",
        "content": "You are an AI assistant that helps people find information."
    },
    {
        "role": "assistant",
        "content": "Hello! How can I assist you today?"
    },
    {
        "role": "user",
        "content": "how many PTO do we have"
    }
]

print()
print("Hello! How can I assist you today?")

# Include speech result if speech is enabled
messages = chat_prompt


while True:
    prompt= input("User: ")

    messages.append({"role": "user", "content": prompt})

    # Generate the completion
    completion = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=6553,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False,
        extra_body={
        "data_sources": [{
            "type": "azure_search",
            "parameters": {
                "endpoint": f"{search_endpoint}",
                "index_name": "hr-test",
                "semantic_configuration": "hr-test-semantic-configuration",
                "query_type": "semantic",
                "fields_mapping": {},
                "in_scope": True,
                "filter": None,
                "strictness": 3,
                "top_n_documents": 5,
                "authentication": {
                "type": "api_key",
                "key": f"{search_key}"
                }
            }
            }]
        }
    )

    answer = completion.to_dict()
    print(f"AI: {answer['choices'][0]['message']['content']}")
    messages.append({"role": "assistant", "content": answer['choices'][0]['message']['content']})
    print()