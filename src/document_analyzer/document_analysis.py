import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import LLMMetadata

from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from prompt.prompt_library import PROMPT_REGISTRY

class DocumentAnalyzer:
    """
    Analyzes documents using a pre-trained model.
    """
    def __init__(self):
        self.log = CustomLogger().get_logger(__name__)
        try:
            self.loader = ModelLoader()
            self.llm = self.loader.load_llms()
            self.prompt = PROMPT_REGISTRY["document_analysis"]

            # Initialize the output parser
            self.parser = JsonOutputParser(pydantic_object=LLMMetadata)
            self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)

            self.log.info("DocumentAnalyzer initialized successfully!")

        except Exception as e:
            self.log.error(f"Error initializing DocumentAnalyzer: {e}")
            raise DocumentPortalException(f"Error in DocumentAnalyzer Initialization:", sys)

    def analyze_document(self, document_text: str) -> dict:
        """
        Analyzes a document and returns the metadata and summary.
        """
        try:
            chain = self.prompt | self.llm | self.fixing_parser
            
            self.log.info("Starting document analysis...")

            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "document_text": document_text
            })

            self.log.info("Document analysis completed successfully.", keys=list(response.keys()))

            return response

        except Exception as e:
            self.log.error(f"Error during document analysis: {e}")
            raise DocumentPortalException(f"Error in DocumentAnalyzer Analysis:", sys)


if __name__ == "__main__":
    analyzer = DocumentAnalyzer()
    # Example usage
    example_text = "This is a sample document text for analysis."
    result = analyzer.analyze_document(example_text)
    print(result)
    # Expected output: Metadata and summary of the document in JSON format