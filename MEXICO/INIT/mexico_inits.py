from MEXICO.MICD.MICD import MICD
from MEXICO.MICD.MICD_port import INIT_port

class Mexico_Init_File(MICD):

    """
    Class to parse and analyze mexico inits files
    Mexico init file is a specific type of MICD with only one tab: "FUN_OUT" and with a reduced number of column
    So this class is a child of MICD class
    """
    file_structure = {
        'FUN_OUT': {
            'Header_name': [
                'Name', 'Type', 'Unit', 'Description', 'Convention', 'Dim1', 'Dim2', 'Com Format',
                'From', 'Min', 'Max','Default Value'],
            'PortObject_Attrib_Equiv': [
                'name',
                'codingtype',
                'unit',
                'description',
                'convention',
                'dim1',
                'dim2',
                'comformat',
                'fromto',
                'min',
                'max',
                'initdefaultvalue'
            ]
        }
    }

    def __init__(self, pathname,flagNewFile=False):
        print(MICD)
        MICD.__init__(self,pathname, None, None, flagNewFile)



    def createPortObj(self, rowDataFrame,sheet):

        # tab to create port Object initialization
        _portTab = []

        # define port type following sheet name
        _type = self.getPortType(sheet)

        # local array of theorical header col names in MICD
        _headerTab = self.file_structure[sheet]['Header_name']

        # dictionnary of name equivalences between configuration array content
        # i.e MICD.file_structure[sheet]['PortObject_Attrib_Equiv']
        # and real sheet header in MICD
        _dict = self._SheetAndDataFrame[sheet]['ColNameEquiv']

        # to create port obj we extract from DataFrame only corresponding fields
        # of MICD_portObjectConfigurationIN configuration tab
        for _field in self.file_structure[sheet]['PortObject_Attrib_Equiv']:

            # index of current _field in column tab
            _index = self.file_structure[sheet]['PortObject_Attrib_Equiv'].index(_field)

            # add
            _portTab.append(rowDataFrame[_dict['API2MICD'][_headerTab[int(_index)]]])

        _portObj = INIT_port(_portTab, _type, self.file_structure[sheet]['PortObject_Attrib_Equiv'])

        return _portObj