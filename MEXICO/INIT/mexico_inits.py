from MEXICO.MICD.MICD import MICD

class Mexico_Init_File(MICD):

    """
    Class to parse and analyze mexico inits files
    Mexico init file is a specific type of MICD with only one tab: "FUN_OUT" and with a reduced number of column
    So this class is a child of MICD class
    """
    Init_file_structure = {
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
        MICD.file_structure = Mexico_Init_File.Init_file_structure
        MICD.__init__(self,pathname, None, None, flagNewFile)



