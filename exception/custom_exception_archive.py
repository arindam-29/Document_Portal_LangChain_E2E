import sys
import traceback
from logger.custom_logger import CustomLogger

# Define Custom Exception:
class DocumentPortalException(Exception):
    def __init__(self, error_message, error_details:sys):

        _,_,exe_tb=error_details.exc_info()
        self.file_name = exe_tb.tb_frame.f_code.co_filename 
        self.line_num = exe_tb.tb_lineno
        self.error_message = str(error_message)
        self.traceback_str = ''.join(traceback.format_exception(*error_details.exc_info()))
        
    def __str__(self):
        return f"""
            Error File: [{self.file_name}], Line Number: [{self.line_num}]
            Error Message: {self.error_message}
            Error Traceback: {self.traceback_str}
            """

# Testing Cell:
if __name__ == "__main__":
    # Initialize custom logger and pass the file name:
    logger=CustomLogger().get_logger(__file__)
    try:
        a = 10/0
        print(a)

    except Exception as e:
        app_excp=DocumentPortalException(e, sys)
        logger.error(app_excp)
        raise app_excp
        