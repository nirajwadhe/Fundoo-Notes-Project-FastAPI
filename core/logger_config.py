import logging

USER_LOG = "user/fundoo.log"
NOTE_LOG = "notes/fundoo.log"

def logger_config(path):
    logging.basicConfig(
        level=logging.DEBUG,
        filename=path,
        filemode='a', 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger = logging.getLogger(__name__)
    return logger
