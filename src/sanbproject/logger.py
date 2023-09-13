import os, sys, logging

logging_str = "[%(asctime)s : %(levelname)s : %(module)s : %(lineno)s : %(message)s]"
log_dir = "logs"
log_filepath = os.path.join(log_dir,"sanb_logs.log")

os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    # filename=log_filepath
    handlers=[
        logging.FileHandler(log_filepath),
        # Prints the log in terminal
        logging.StreamHandler(sys.stdout)
    ]
)