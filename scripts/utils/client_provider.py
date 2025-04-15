import os
from openai import OpenAI
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
import boto3
from dotenv import load_dotenv

load_dotenv()
class ClientProvider:
    _openai_client = None
    _qdrant_client = None
    _embeddings = None
    _s3_client = None

    @classmethod
    def get_openai_client(cls):
        if cls._openai_client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            cls._openai_client = OpenAI(api_key=api_key)
        return cls._openai_client

    @classmethod
    def get_qdrant_client(cls):
        if cls._qdrant_client is None:
            url = os.getenv("QDRANT_URL")
            api_key = os.getenv("QDRANT_API_KEY")
            if not url or not api_key:
                raise ValueError("QDRANT_URL or QDRANT_API_KEY environment variables not set")
            cls._qdrant_client = QdrantClient(url=url, api_key=api_key)
        return cls._qdrant_client
    
    @classmethod
    def get_embeddings(cls):
        if cls._embeddings is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            cls._embeddings = OpenAIEmbeddings(api_key=api_key)
        return cls._embeddings
    
    @classmethod
    def get_s3_client(cls):
        if cls._s3_client is None:
            aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
            aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

            if not aws_access_key_id or not aws_secret_access_key:
                raise ValueError("AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY not set")

            cls._s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
        return cls._s3_client