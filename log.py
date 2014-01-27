import logging, os, datetime, sys


class CachelessFormatter(logging.Formatter):
    # I came up with that after reading the answers to
    #     http://stackoverflow.com/questions/5875225/
    # which pointed me to
    #     http://bugs.python.org/issue6435
    # I still think Vinay Sajip has a bit of an attitude :p.
    def format(self, record):
        # Disable the caching of the exception text.
        backup = record.exc_text
        record.exc_text = None
        s = logging.Formatter.format(self, record)
        record.exc_test = backup
        return s

class ConsoleFormatter(CachelessFormatter):
    def formatException(self, exc_info):
        return "EXCEPTION %s: %s" % exc_info[:2]

class NoExceptionFormatter(logging.Formatter):
    def format(self, record):
        record.exc_text = '' # ensure formatException gets called
        super(NoExceptionFormatter, self).format(record)

    def formatException(self, record):
        return ''

class configuration(object):

    PREFIX = "informi"
    def __init__(self, name, logFolder, logLevel):
        self.name = name
        self.format = CachelessFormatter('%(asctime)s - %(levelname)s - %(name)s.%(module)s - %(message)s')
        dateTag = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
        self.logLevel = logLevel

        self.logFilename = os.path.join(logFolder, '%s.%s.%s.log' % (self.PREFIX, name, dateTag))
        try:
            if not os.path.exists(logFolder):
                os.makedirs(logFolder)
        except Exception, exception:
            raise exception


    def create(self):
        logger = logging.getLogger('%s.%s' % (self.PREFIX, self.name))
        logger.info("Logging initialized")
        logger.setLevel(self.logLevel)
 
        # create the logging file handler
        fh = logging.FileHandler(self.logFilename)
        fh.setFormatter(self.format)
        fh.setLevel(self.logLevel)

        # create the logging console handler
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.INFO)
        consoleHandler.setFormatter(ConsoleFormatter("%(levelname)-8s - %(message)s"))

        # add handler to logger objects
        logger.addHandler(consoleHandler)
        logger.addHandler(fh)
                
        logger.info("Logging initialized")
        logger.debug("Debug enabled")
        
        return logger


