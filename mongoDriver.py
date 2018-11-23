import bot_settings as settings
import logging
import pymongo

class MongoDriver:
    def __init__(self):
        # Setup
        self._log_setup()
        self._connect()

    def _log_setup(self):
        self.logger = logging.getLogger('mongo')
        log_f = logging.FileHandler(settings.DB_LOG_FILE)
        log_s = logging.StreamHandler()

        if (settings.DEBUG):
            self.logger.setLevel(logging.DEBUG)
            log_f.setLevel(logging.DEBUG)
            log_s.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(settings.LOG_FORMATTER)
        log_f.setFormatter(formatter)
        log_s.setFormatter(formatter)

        self.logger.addHandler(log_f)
        self.logger.addHandler(log_s)
    
    def _connect(self):
        # initialize client instance
        self.client = pymongo.MongoClient(settings.DB_CONNECTION_STRING.format(
            settings.DB_USERNAME, settings.DB_PASSWORD
        ))
        # setup collections
        try:
            self.giveaway = self.client.codex.giveaway
            self.logger.info("Successfully loaded database")
        except:
            self.logger.error("Couldn't load database")
            exit()

    def record_giveaway_entry(self, entry):
        self.giveaway.insert_one(entry)
        self.logger.info("Inserted entry: {0} into <giveaway>".format(str(entry)))


