import os
import sys
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from utils.config_loader import load_config
from config.constants import EMBEDDING_MODEL, LLM_MODEL #Model Selection

log = CustomLogger().get_logger(__name__)

class ModelLoader:
    """
    An utility class to load Embeddings and LLM Modles.
    """
    
    def __init__(self):
        load_dotenv()
        self.__validate_env()
        self.config=load_config()
        log.info("Configuration Loadded Successfully!", config_keys=list(self.config.keys()))

    def __validate_env(self):
        """
        Validate Environments and API Keys.
        """

        env_variables = ["GOOGLE_API_KEY", "GROQ_API_KEY", "OPENAI_API_KEY"]
        self.api_keys = {key:os.getenv(key) for key in env_variables}
        
        missing_keys = [k for k, v in self.api_keys.items() if not v]
        if missing_keys:
            log.error("Missing API Key for Environement Variable in .env file! ", missing_keys=missing_keys)
            raise DocumentPortalException("Missing API Key for Environement Variable in .env file! ", sys)

        log.info("Environment Variables Validated", available_keys=[k for k in self.api_keys if self.api_keys[k]])

    def load_embeddings(self):
        """
        Load Embedding Models.
        """
        embed_block = self.config["embedding_model"]
        log.info("Loading Embedding Model...")

        if EMBEDDING_MODEL not in embed_block:
            log.error(f"Embedding Model '{EMBEDDING_MODEL}' details found in config file!", provider_key=EMBEDDING_MODEL)
            raise ValueError(f"Embedding Model '{EMBEDDING_MODEL}' details found in config file!")

        embed_config = embed_block[EMBEDDING_MODEL]
        provider = embed_config.get("provider")
        model_name = embed_config.get("model_name")

        log.info("Embedding model to be loaded", provider=provider, model=model_name)

        try:
            if provider == "google":
                return GoogleGenerativeAIEmbeddings(model=model_name)
            elif provider == "openai":
                return OpenAIEmbeddings(model=model_name)
            else:
                log.error("Unsupported Embedding Model provider", provider=provider)
                raise ValueError(f"Unsupported Embedding Model provider: {provider}")
        
        except Exception as e:
            log.error(f"Error in loading Embedding Model '{provider}'! ", error=str(e))
            raise DocumentPortalException(f"Error in loading Embedding Model '{provider}'! ", sys)

    def load_llms(self):
        """
        Load LLM Model based on the provider in config file.
        """

        llm_block = self.config["llm"]

        log.info("Loading LLM Model...")
        
        if LLM_MODEL not in llm_block:
            log.error(f"LLM Model '{LLM_MODEL}' details found in config file!", provider_key=LLM_MODEL)
            raise ValueError(f"LLM Model '{LLM_MODEL}' details found in config file!")

        llm_config = llm_block[LLM_MODEL]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature", 0.2)
        max_tokens = llm_config.get("max_output_tokens", 2048)
        
        log.info("LLM to be loaded", provider=provider, model=model_name, temperature=temperature, max_tokens=max_tokens)

        if provider == "google":
            llm=ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            return llm

        elif provider == "groq":
            llm=ChatGroq(
                model=model_name,
                api_key=self.api_keys["GROQ_API_KEY"],
                temperature=temperature,
            )
            return llm
            
        elif provider == "openai":
            return ChatOpenAI(
                model=model_name,
                api_key=self.api_keys["OPENAI_API_KEY"],
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            log.error("Unsupported LLM provider", provider=provider)
            raise ValueError(f"Unsupported LLM provider: {provider}")

# Testing cell:
if __name__ == "__main__":
    loader = ModelLoader()
    
    # Test embedding model loading
    embeddings = loader.load_embeddings()
    print(f"Embedding Model Loaded: {embeddings}")
    
    # Test the ModelLoader
    result=embeddings.embed_query("Hello, how are you?")
    print(f"Embedding Result: {result}")
    
    # Test LLM loading based on YAML config
    llm = loader.load_llms()
    print(f"LLM Loaded: {llm}")
    
    # Test the ModelLoader
    result=llm.invoke("Hello, how are you?")
    print(f"LLM Result: {result.content}")