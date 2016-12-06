from optparse import OptionParser
from MEXICO.CFG.mexico_cfg import mexicoConfig

if __name__ == "__main__":

    # command line treatment
    parser = OptionParser("usage: %prog --csv <csvFile> --mexico <mexicoCfgFile>")
    parser.add_option("-c","--csv", dest="csvFile", help="CSV file containing connexions/inits to integer",
                      type="string", metavar="FILE")
    parser.add_option("-x","--mexico", dest="mexicoCfgFile", help="Mexico configuration file (.xml)",
                      type="string", metavar="FILE")

    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.error("incorrect number of arguments")

    csvFile = options.csvFile
    mexicoCfgFile = options.mexicoCfgFile
    print("_csvFile: "+csvFile)
    print("_mexicoCfgFile: "+mexicoCfgFile)
    #
    # mexico cfg parsing
    #   Extract informations about MEXICO base.
    #   Informations used here:
    #       _ MEXICO flow file  => allow to set available model list
    #                           => I/O of each of them

    _mexicoCfgObj = mexicoConfig(mexicoCfgFile)

    _mexicoFlowFile = _mexicoCfgObj.getFlowFile()

    print("_mexicoFlowFile: "+_mexicoFlowFile)
    #
    # csv parsing
    #  this function will parse CSV File
    #
    # column number are variable, the CSV file can have the following header
    # MODOCC_PROD;PORT_PROD;SIGNAL;MODOCC_CONSO;PORT_CONSUM;
    # MODOCC_PROD;PORT_PROD;SIGNAL;INIT;MODOCC_CONSO;PORT_CONSUM
    # MODOCC_PROD;PORT_PROD;MODOCC_CONSO;PORT_CONSUM;
    # MODOCC_PROD;PORT_PROD;OP_PROD;SIGNAL;INIT;MODOCC_CONSO;PORT_CONSUM;;OP_CONS
    # MODOCC_PROD;PORT_PROD;OP_PROD;TAB_PROD;SIGNAL;INIT;MODOCC_CONSO;PORT_CONSUM;OP_CONS;TAB_PROD





