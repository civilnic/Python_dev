from BDS.BDS import BDS
from BDS.BDS_FWC import BDS_FWC


class BDS_SDAC(BDS_FWC):
    """
    Class to defined BDS data file
    """
    ConnectorMap = dict()
    ConfigXMLPath = "/MSP_ATA31/SDAC/connector_map/input"

    def __init__(self, pathname, connectormapfile):
        """
        Attributes are:
        _ path name of the file
        """

        super().__init__(pathname,connectormapfile)