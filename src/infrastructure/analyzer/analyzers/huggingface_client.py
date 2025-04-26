import os
from typing import Optional

from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer, Pipeline, pipeline

from src.infrastructure.analyzer.analyzers.base_client import BaseLLMClient

load_dotenv()


class HuggingFaceClient(BaseLLMClient):
    """
    Client for interacting with Hugging Face models.
    Loads the model and tokenizer, and exposes a text-generation pipeline.
    """

    def __init__(self):
        """
        Parameters:
            model_name: the HF model identifier, e.g. "gpt2", "bigscience/bloom-560m", etc.
        """
        self.model_name = os.environ.get("HUGGINGFACE_MODEL_NAME")

        # download tokenizer & model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

        # create a simple text-generation pipeline
        self.pipeline: Pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
        )

    def get_client(self) -> Pipeline:
        """
        Returns the HF text-generation pipeline. You can call:
            client("Once upon a time", max_length=50, do_sample=True)
        """
        return self.pipeline

    def get_model(self) -> Optional[str]:
        """
        Returns the model identifier that was loaded.
        """
        return self.model_name
