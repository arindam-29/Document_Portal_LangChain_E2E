import logging
import os
from datetime import datetime

class CustomLogger:
    def __init__(self, log_dir="logs"):
        # Ensure "logs" directory exsist:
        self.log_dir=os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.log_dir, exist_ok=True)

        # Create timestamped log file name format:
        log_file=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        log_file_path=os.path.join(self.log_dir, log_file)

        # Config Logging:
        logging.basicConfig(
            filename=log_file_path,
            format="[ %(asctime)s ] %(levelname)s %(name)s (line:%(lineno)d) - %(message)s",
            level=logging.INFO
            )

    def get_logger(self, name=__file__):
        return logging.getLogger(os.path.basename(name))
    

if __name__=="__main__":
    logger=CustomLogger()
    logger=logger.get_logger(__file__)
    logger.info("Custome logger Testing..")