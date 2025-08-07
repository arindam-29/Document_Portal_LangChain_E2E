import sys
from dotenv import load_dotenv
import pandas as pd
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import SummaryResponse

class DocumentComparatorLLM:
    def __init__(self):
        load_dotenv()
        self.log = CustomLogger().get_logger(__name__)
        self.loader = ModelLoader()
        self.llm = self.loader.load_llms()
        self.parser = JsonOutputParser(pydantic_object=SummaryResponse)
        self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)
        self.prompt = PROMPT_REGISTRY["document_compare"]

        self.chain = self.prompt | self.llm | self.parser
        
        self.log.info("DocumentComparatorLLM initialized", model=self.llm)

    def compare_documents(self, combined_docs: str) -> pd.DataFrame:
        """
        Compares two documents and returns the structured comparison result.
        """

        try:
            inputs = {
                "combined_docs": combined_docs,
                "format_instruction": self.parser.get_format_instructions()
            }

            self.log.info("Invoking document comparison LLM chain")
            response = self.chain.invoke(inputs)
            self.log.info("Chain for document comparison is invoked successfully", response_preview=str(response)[:200])
            return self._format_response(response)
        except Exception as e:
            self.log.error("Error in compare documents", error=str(e))
            raise DocumentPortalException("Error in compare documents", sys)

    def _format_response(self, response_parsed: list[dict]) -> pd.DataFrame: 
        """
        Formats the response from the LLM into a structured format.
        """
        try:
            df = pd.DataFrame(response_parsed)
            return df
        except Exception as e:
            self.log.error("Error formatting response into DataFrame", error=str(e))
            DocumentPortalException("Error formatting response", sys)
