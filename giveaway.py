import bot_settings as settings

class Giveaway():
    '''
    Subclass for commands to handle giveaway logic
    '''
    def __init__(self, logger):
        # Log setup
        self.logger = logger
        # Set initial state to not live
        self.live = False
        # Set properties to default
        self.name = settings.GIVEAWAY_DEFAULT_NAME
        self.description = settings.GIVEAWAY_DEFAULT_DESCRIPTION
        # Initialize stats
        self.stats = {
            'participants': [],
            'entries': 0
        }

    # Returns success: T/F for starting a new giveaway
    def start(self, name, description):
        if self.live:
            return False, settings.GIVEAWAY_ALREADY_LIVE.format(name)

        self.name = name
        self.description = description
        # Start giveaway
        self.live = True
        self.logger.info("Giveaway {0}: {1} started".format(name, description))
        return True, settings.GIVEAWAY_STATUS_LIVE.format(name, description)

    # Returns success: T/F for closing a giveaway
    def close(self):
        if not self.live:
            return False, settings.GIVEAWAY_STATUS_OFF
        
        name = self.name
        # Clear giveaway data
        self._clear()
        self.live = False
        return True, settings.GIVEAWAY_CLOSED.format(name)

    def _clear(self):
        self.name = settings.GIVEAWAY_DEFAULT_NAME
        self.description = settings.GIVEAWAY_DEFAULT_DESCRIPTION
        self.stats = {
            'participants': [],
            'entries': 0
        }
    
    def statistics(self):
        if self.live:
            return True, settings.GIVEAWAY_STATS.format(self.name, 
                    self.stats['entries'], ', '.join(self.stats['participants']))
        else:
            return False, settings.GIVEAWAY_STATUS_OFF

    def info(self):
        if self.live:
            return True, settings.GIVEAWAY_INFO.format(self.name, self.description)
        else:
            return False, settings.GIVEAWAY_STATUS_OFF
        
    # Returns success: T/F for entering giveaway
    def enter(self, username):
        if not self.live:
            return False, settings.GIVEAWAY_STATUS_OFF
        
        if username in self.stats['participants']:
            return False, settings.GIVEAWAY_ALREADY_REGISTERED.format(self.name)

        self.stats['participants'].append(username)
        self.stats['entries'] += 1

        self._record(username)

        self.logger.info("{0} joined giveaway {1}".format(username, self.name))
        return True, settings.GIVEAWAY_NEW_ENTRY.format(self.name)

    # TODO: !!! WIRE TO MONGO !!!
    def _record(self, entry):
        # temporarily record entries to a file
        f = open('../temp_giveaway', 'a')
        f.write("Giveaway <{0}> | new entry: {1}\n".format(self.name, entry))
    