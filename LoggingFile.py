import logging.config


class LoggingFile:
    def logVal(self):
        logging.config.fileConfig('logger.config')
        logger = logging.getLogger('Admin_Client')
        return logger
