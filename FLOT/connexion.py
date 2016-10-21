class connexion:
    """
    Class to represent connexion in ASPIC, MEXICO or DSS data flot
    """


    def __init__(self, producer, channel, consummer):
        """
        Attributes are:
        _ path name of the file
        """
        self.producer = producer
        self.channel = channel
        self.consummer = consummer

    @property
    def producer(self):
        return self.producer

    @producer.setter
    def producer(self, producer):
        self.producer = producer

    @property
    def channel(self):
        return self.channel

    @channel.setter
    def channel(self, channel):
        self.channel = channel

    @property
    def consummer(self):
        return self.consummer

    @consummer.setter
    def consummer(self, consummer):
        self.consummer = consummer
