import logging

USER_LOG = "user/fundoo.log"
NOTE_LOG = "notes/fundoo.log"

def logger_config(path):
    logging.basicConfig(
        level=logging.INFO,
        filename=path,
        filemode='a', 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # Set the logging level for watchfiles module to WARNING
    watchfiles_logger = logging.getLogger('watchfiles')
    watchfiles_logger.setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    return logger
