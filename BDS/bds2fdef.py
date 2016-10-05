# for Microsoft Excel reading and writing
import xlrd
import xlwt
import xlutils.copy
import time

# standard packages
import sys, string, os

#################################
## Reading functions for FWC(DIS) BDS
#################################
#returns string: bus name
def FWC_DIS_get_formated_name(sheet, line):
    return sheet.cell_value(line, 3) # Name_F column
    
#returns string: label in octal with 3 digits
def FWC_DIS_get_label(sheet, line):
    return "%03d" % int(sheet.cell_value(line, 13)) # LABEL_IN/LABEL_OUT column

#returns string: ARINC format (BNR, BCD, DIS, ISO5, HYB)
def FWC_DIS_get_label_format(sheet, line):
    return 'DIS'
    
#returns string: SDI (00, 01, 10, 11, DD, XX)
def FWC_DIS_get_sdi(sheet, line):
	if sheet.cell_value(line, 14)=="XX" or sheet.cell_value(line, 14)=="DD":
		return "%s" % sheet.cell_value(line, 14) # SDI_IN/SDI_OUT column
	else:
	    return "%02d" % int(sheet.cell_value(line, 14)) # SDI_IN/SDI_OUT column

#returns string: SSM type (status_ssm_dis, status_ssm_bnr, status_ssm_bcd, status_no_ssm)
def FWC_DIS_get_ssm_type(sheet, line):
    return 'status_ssm_dis'

#returns string: ARINC format (BNR, BCD, Discrete, Opaque)
def FWC_DIS_get_parameter_format(sheet, line):
    return 'Discrete'

#returns int: MSB assumed in a [1:32] range
def FWC_DIS_get_msb(sheet, line):
    return int(sheet.cell_value(line, 15)) # BIT_IN/BIT_OUT column

#returns string: parameter name
def FWC_DIS_get_parameter_name(sheet, line):
    return sheet.cell_value(line, 9) # PAR_DEF column

#returns string: parameter type (Float, Integer, Boolean)
def FWC_DIS_get_parameter_type(sheet, line):
    return 'Boolean'
        
#returns int: number of significant bits
def FWC_DIS_get_nb_bits(sheet, line):
    return 1
    
#returns int: 1 if the value is signed, 0 otherwise
def FWC_DIS_get_signed(sheet, line):    
    return 0
    
#returns float: actual value is raw_data * resolution
def FWC_DIS_get_resolution(sheet, line):
    return 0
    
#returns string: MICD variable name
def FWC_DIS_get_signal_name(sheet, line):
    return sheet.cell_value(line, 1) #Name_PF column

#returns string: MICD variable type
def FWC_DIS_get_signal_type(sheet, line):
    return sheet.cell_value(line, 2) #Type column

#returns string: signal unit
def FWC_DIS_get_signal_unit(sheet, line):
    return 'wu'
    
#################################
## Reading functions for FWC(BNR) BDS
#################################
#returns string: bus name
def FWC_BNR_get_formated_name(sheet, line):
    return sheet.cell_value(line, 3) # Name_F column
    
#returns string: label in octal with 3 digits
def FWC_BNR_get_label(sheet, line):
    return "%03d" % int(sheet.cell_value(line, 15)) # LABEL_IN/LABEL_OUT column

#returns string: ARINC format (BNR, BCD, DIS, ISO5, HYB)
def FWC_BNR_get_label_format(sheet, line):
    return 'BNR'

#returns string: SDI (00, 01, 10, 11, DD, XX)
def FWC_BNR_get_sdi(sheet, line):
	if sheet.cell_value(line, 16)=="XX" or sheet.cell_value(line, 16)=="DD":
		return "%s" % sheet.cell_value(line, 16) # SDI_IN/SDI_OUT column
	else:
	    return "%02d" % int(sheet.cell_value(line, 16)) # SDI_IN/SDI_OUT column

#returns string: SSM type (status_ssm_dis, status_ssm_bnr, status_ssm_bcd, status_no_ssm)
def FWC_BNR_get_ssm_type(sheet, line):
    return 'status_ssm_bnr'

#returns string: ARINC format (BNR, BCD, Discrete, Opaque)
def FWC_BNR_get_parameter_format(sheet, line):
    return 'BNR'

#returns int: MSB assumed in a [1:32] range, not including sign bit which is at MSB+1
def FWC_BNR_get_msb(sheet, line):
    return 28
#returns string: parameter name
def FWC_BNR_get_parameter_name(sheet, line):
    return sheet.cell_value(line, 13) # PAR_DEF column

#returns string: parameter type (Float, Integer, Boolean)
def FWC_BNR_get_parameter_type(sheet, line):
    return 'Float'
        
#returns int: number of significant bits
def FWC_BNR_get_nb_bits(sheet, line):
    return int(sheet.cell_value(line, 8)) # SIG_BIT column
    
#returns int: 1 if the value is signed, 0 otherwise
def FWC_BNR_get_signed(sheet, line):    
    return 1 #assumed
    
#returns float: actual value is raw_data * resolution
def FWC_BNR_get_resolution(sheet, line):
    #return float(sheet.cell_value(line, 10)) # RESOLUTION_IN/RESOLUTION_OUT column
    # Computes RESULUTION_(IN/OUT) instead of retrieving it
    if sheet.cell_value(line, 8) <> '' and sheet.cell_value(line, 9) <> '':
        _sig_bit = float(sheet.cell_value(line, 8))
        _rang_io = float(sheet.cell_value(line, 9))
        return _rang_io / (2**(_sig_bit))
    else:
        return float(sheet.cell_value(line, 10))
    
#returns string: MICD variable name
def FWC_BNR_get_signal_name(sheet, line):
    return sheet.cell_value(line, 1) #Name_PF column

#returns string: MICD variable type
def FWC_BNR_get_signal_type(sheet, line):
    return sheet.cell_value(line, 2) #Type column

#returns string: signal unit
def FWC_BNR_get_signal_unit(sheet, line):
    return sheet.cell_value(line, 11) # UNIT_OUT column
        
#################################
## Reading functions for EIS BDS
#################################
#returns string: bus name
def EIS_get_formated_name(sheet, line):
    return sheet.cell_value(line, 3) # Name_F column
    
#returns string: label in octal with 3 digits
def EIS_get_label(sheet, line):
    label_sdi = sheet.cell_value(line, 5) # CONT column
    label = string.split(label_sdi, '_')[0]
    return "%03d" % int(label)

#returns string: ARINC format (BNR, BCD, DIS, ISO5, HYB)
def EIS_get_label_format(sheet, line):
    format_label = sheet.cell_value(line, 7) # FORMAT_BLOC column
    if format_label == 'DW':
        format_label = 'DIS'
    return format_label

#returns string: SDI (00, 01, 10, 11, DD, XX)
def EIS_get_sdi(sheet, line):
    label_sdi = sheet.cell_value(line, 5) # CONT column
    sdi = string.split(label_sdi, '_')[1]
    return sdi


#returns string: SSM type (status_ssm_dis, status_ssm_bnr, status_ssm_bcd, status_no_ssm)
def EIS_get_ssm_type(sheet, line):
    format_label = EIS_get_label_format(sheet, line)
    ssm_type = sheet.cell_value(line, 9) # SSM_TYPE column
    if format_label == 'DIS':
      ssm_type = 'status_ssm_dis'
    elif format_label == 'BCD':
      ssm_type = 'status_ssm_bcd'
    elif format_label == 'BNR':
      ssm_type = 'status_ssm_bnr'
    elif format_label == 'HYB':
      if ssm_type == 'DW':
          ssm_type = 'status_ssm_dis'
      elif ssm_type == 'BCD':
          ssm_type = 'status_ssm_bcd'
      elif ssm_type == 'BNR':
          ssm_type = 'status_ssm_bnr'
      else:
          ssm_type = 'status_no_ssm'
    else:
      ssm_type = 'status_no_ssm'
    return ssm_type

#returns string: ARINC format (BNR, BCD, Discrete, Opaque)
def EIS_get_parameter_format(sheet, line):
    format_param=sheet.cell_value(line, 11) #FORMAT_PARAM column
    type_param=sheet.cell_value(line, 14) #TYPE column, after the / character
    if '/' in type_param:
        type_format_param=string.split(type_param, '/')[1] #after the / character
    else:
        type_format_param=type_param
    
    if format_param=="DW":
        format='Discrete'
        if type_format_param!='DEFDW2':
            sys.stderr.write('WAR: '+format_param+' type '+type_format_param+' unknown on '+sheet.name+':'+str(line+1)+' ('+EIS_get_signal_name(sheet, line)+')\n')
    elif format_param=="BCD":
        format='BCD'
        if type_format_param!='DEFBCD2':
            sys.stderr.write('WAR: '+format_param+' type '+type_format_param+' unknown on '+sheet.name+':'+str(line+1)+' ('+EIS_get_signal_name(sheet, line)+')\n')
    elif format_param=="BNR":
        format='BNR'
        if type_format_param!='DEFBNR1':
            sys.stderr.write('WAR: '+format_param+' type '+type_format_param+' unknown on '+sheet.name+':'+str(line+1)+' ('+EIS_get_signal_name(sheet, line)+')\n')
    elif format_param=="ISO5":
        format='Opaque'
    elif format_param=='':
        format='' # assumed as not an ARINC
    else:
        sys.stderr.write('WAR: format '+format_param+' unknown on '+sheet.name+':'+str(line+1)+' ('+EIS_get_signal_name(sheet, line)+') -> Opaque will be used\n')
        format='Opaque'
    return format

#returns int: MSB assumed in a [1:32] range, does not include sign bit (which is at MSB+1)
def EIS_get_msb(sheet, line):
    return int(sheet.cell_value(line, 15)) # POSI column

#returns string: parameter name
def EIS_get_parameter_name(sheet, line):
    return sheet.cell_value(line, 12) # LIB_PARAM column

#returns string: parameter type (Float, Integer, Boolean)
def EIS_get_parameter_type(sheet, line):
    if EIS_get_parameter_format(sheet, line)=='BNR':
        param_type='Float'
    elif EIS_get_parameter_format(sheet, line)=='BCD':
        param_type='Float'
    elif EIS_get_parameter_format(sheet, line)=='Opaque':
        param_type='Integer'
    elif EIS_get_parameter_format(sheet, line)=='Discrete':
        param_type='Boolean'
    else:
        sys.stderr.write('WAR: unknown parameter format '+ EIS_get_parameter_format(sheet, line) + '\n')
        param_type=''
    
    return param_type
        
#returns int: number of significant bits, does not include sign bit
def EIS_get_nb_bits(sheet, line):
    return int(sheet.cell_value(line, 16)) #TAIL column
    
#returns int: 1 if the value is signed, 0 otherwise
def EIS_get_signed(sheet, line):    
    sgn = sheet.cell_value(line, 17) #SGN column
    if sgn == 'O':
        signed=1
    else:
        signed=0
        
    return signed
    
#returns float: actual value is raw_data * resolution
def EIS_get_resolution(sheet, line):
    if EIS_get_parameter_format(sheet, line) == 'BNR':
        range = float(sheet.cell_value(line, 18)) # ECHEL column. The value is assumed in [-range ; range[ for signed, and [0, range[ for not-signed
        resolution = range / 2**EIS_get_nb_bits(sheet, line)
    elif EIS_get_parameter_format(sheet, line) == 'BCD':
        max_encoding=0
        remaining_bits=EIS_get_nb_bits(sheet, line)
        n_digit=0
        while remaining_bits > 3:
            max_encoding = max_encoding + 9*10**n_digit
            remaining_bits = remaining_bits-4
            n_digit=n_digit+1
        if remaining_bits==3:
            max_encoding = max_encoding + 7*10**n_digit
        elif remaining_bits==2:
            max_encoding = max_encoding + 3*10**n_digit
        elif remaining_bits==1:
            max_encoding = max_encoding + 1*10**n_digit

        range = float(sheet.cell_value(line, 18)) # ECHEL column. The value is assumed in [-range ; range[ for signed, and [0, range[ for not-signed
        resolution = range / max_encoding
    else:
        resolution=0.0 # not used if not a numeric
        
    return float(resolution)
    
#returns string: MICD variable name
def EIS_get_signal_name(sheet, line):
    return sheet.cell_value(line, 1) #Name_PF column

#returns string: MICD variable type
def EIS_get_signal_type(sheet, line):
    return sheet.cell_value(line, 2) #Type column

#returns string: signal unit
def EIS_get_signal_unit(sheet, line):
    if EIS_get_signal_type(sheet, line)=='boolean':
        type='wu'
    else:
        type=sheet.cell_value(line, 13) # UNITE column
    return type
    
#################################
## Reading functions for SDAC BDS
#################################
#returns string: bus name
def SDAC_get_formated_name(sheet, line):
    return sheet.cell_value(line, 3) # Name_F column
    
#returns string: label in octal with 3 digits
def SDAC_get_label(sheet, line):
    return "%03d" % int(sheet.cell_value(line, 10)) # label_in column

#returns string: ARINC format (BNR, BCD, DIS, ISO5, HYB)
def SDAC_get_label_format(sheet, line):
    format_label = sheet.cell_value(line, 19) # format column
    if format_label == '':
        format_label = 'DIS'
    return format_label

#returns string: SDI (00, 01, 10, 11, DD, XX) on 2 digits
def SDAC_get_sdi(sheet, line):
	if sheet.cell_value(line, 12)=="XX" or sheet.cell_value(line, 12)=="DD":
		return "%s" % sheet.cell_value(line, 12) # sdi_in column
	else:
	    return "%02d" % int(sheet.cell_value(line, 12)) # sdi_in column

#returns string: SSM type (status_ssm_dis, status_ssm_bnr, status_ssm_bcd, status_no_ssm)
def SDAC_get_ssm_type(sheet, line):
    format_label = SDAC_get_label_format(sheet, line)
    ssm_type = ''
    if format_label == 'DIS':
      ssm_type = 'status_ssm_dis'
    elif format_label == 'BCD':
      ssm_type = 'status_ssm_bcd'
    elif format_label == 'BNR':
      ssm_type = 'status_ssm_bnr'
    else:
      ssm_type = 'status_no_ssm'
    return ssm_type

#returns string: ARINC format (BNR, BCD, Discrete, Opaque)
def SDAC_get_parameter_format(sheet, line):
    format_param=sheet.cell_value(line, 9) #type column
    if format_param=="B":
        format='Discrete'
    elif format_param=="N":
        format='BNR' #assumed
    else:
        sys.stderr.write('WAR: format '+format_param+' unknown on '+sheet.name+':'+str(line+1)+' ('+SDAC_get_signal_name(sheet, line)+') -> Opaque will be used\n')
        format='Opaque'
    return format

#returns int: MSB assumed in a [1:32] range, not including sign bit which is at MSB+1
def SDAC_get_msb(sheet, line):
    if SDAC_get_parameter_format(sheet, line) == 'Discrete':
        msb=int(sheet.cell_value(line, 14)) # bit_in column
    else:
        msb=28 #assumed
    return msb

#returns string: parameter name
def SDAC_get_parameter_name(sheet, line):
    return sheet.cell_value(line, 18) # par_definition column

#returns string: parameter type (Float, Integer, Boolean)
def SDAC_get_parameter_type(sheet, line):
    if SDAC_get_parameter_format(sheet, line)=='BNR':
        param_type='Float'
    elif SDAC_get_parameter_format(sheet, line)=='Discrete':
        param_type='Boolean'
    else:
        sys.stderr.write('WAR: unknown parameter format '+ SDAC_get_parameter_format(sheet, line) + ' on '+sheet.name+':'+str(line+1)+' ('+SDAC_get_signal_name(sheet, line)+')\n')
        param_type=''
    
    return param_type
        
#returns int: number of significant bits
def SDAC_get_nb_bits(sheet, line):
    if SDAC_get_parameter_format(sheet, line)=='BNR':
        nb_bits=int(sheet.cell_value(line, 21)) #sig_bit column
    else:
        nb_bits=1 #Discrete
    return nb_bits
    
#returns int: 1 if the value is signed, 0 otherwise
def SDAC_get_signed(sheet, line):    
    return 1 #assumed
    
#returns float: actual value is raw_data * resolution
def SDAC_get_resolution(sheet, line):
    if SDAC_get_parameter_format(sheet, line) == 'BNR':
        range_str=sheet.cell_value(line, 22) # range_out column. The value is assumed in [-range ; range[ for signed, and [0, range[ for not-signed
        if range_str=='':
            sys.stderr.write('WAR: empty range on '+sheet.name+':'+str(line+1)+' ('+SDAC_get_signal_name(sheet, line)+') -> resolution=1.0 will be used\n')
            resolution=1.0
        else:
            range = float(range_str)
            resolution = range / 2**SDAC_get_nb_bits(sheet, line)
    elif SDAC_get_parameter_format(sheet, line) == 'BCD':
        max_encoding=0
        remaining_bits=SDAC_get_nb_bits(sheet, line)
        n_digit=0
        while remaining_bits > 3:
            max_encoding = max_encoding + 9*10**n_digit
            remaining_bits = remaining_bits-4
            n_digit=n_digit+1
        if remaining_bits==3:
            max_encoding = max_encoding + 7*10**n_digit
        elif remaining_bits==2:
            max_encoding = max_encoding + 3*10**n_digit
        elif remaining_bits==1:
            max_encoding = max_encoding + 1*10**n_digit

        range = float(sheet.cell_value(line, 22)) # range_out column. The value is assumed in [-range ; range[ for signed, and [0, range[ for not-signed
        resolution = range / max_encoding
    else:
        resolution=0 # not used if not a numeric
        
    return float(resolution)
    
#returns string: MICD variable name
def SDAC_get_signal_name(sheet, line):
    return sheet.cell_value(line, 1) #Name_PF column

#returns string: MICD variable type
def SDAC_get_signal_type(sheet, line):
    return sheet.cell_value(line, 2) #Type column

#returns string: signal unit
def SDAC_get_signal_type(sheet, line):
    return sheet.cell_value(line, 2) #Type column

#returns string: signal unit
def SDAC_get_signal_unit(sheet, line):
    if SDAC_get_signal_type(sheet, line)=='boolean':
        type='wu'
    else:
        type='' #no information in the BDS
    return type
    
###############################
## BDS reading function
###############################
def read_bds_sheet(ARINC_format_labels, ARINC_deformat_labels, bds_sheet_name, bds_formating, bds_format):
    if bds_format == 'EIS':
        BDS_get_formated_name=EIS_get_formated_name
        BDS_get_label=EIS_get_label
        BDS_get_label_format=EIS_get_label_format
        BDS_get_sdi=EIS_get_sdi
        BDS_get_ssm_type=EIS_get_ssm_type
        BDS_get_parameter_format=EIS_get_parameter_format
        BDS_get_msb=EIS_get_msb
        BDS_get_parameter_name=EIS_get_parameter_name
        BDS_get_parameter_type=EIS_get_parameter_type
        BDS_get_nb_bits=EIS_get_nb_bits
        BDS_get_signed=EIS_get_signed
        BDS_get_resolution=EIS_get_resolution
        BDS_get_signal_name=EIS_get_signal_name
        BDS_get_signal_type=EIS_get_signal_type
        BDS_get_signal_unit=EIS_get_signal_unit
    elif bds_format == 'FWC_DIS':
        BDS_get_formated_name=FWC_DIS_get_formated_name
        BDS_get_label=FWC_DIS_get_label
        BDS_get_label_format=FWC_DIS_get_label_format
        BDS_get_sdi=FWC_DIS_get_sdi
        BDS_get_ssm_type=FWC_DIS_get_ssm_type
        BDS_get_parameter_format=FWC_DIS_get_parameter_format
        BDS_get_msb=FWC_DIS_get_msb
        BDS_get_parameter_name=FWC_DIS_get_parameter_name
        BDS_get_parameter_type=FWC_DIS_get_parameter_type
        BDS_get_nb_bits=FWC_DIS_get_nb_bits
        BDS_get_signed=FWC_DIS_get_signed
        BDS_get_resolution=FWC_DIS_get_resolution
        BDS_get_signal_name=FWC_DIS_get_signal_name
        BDS_get_signal_type=FWC_DIS_get_signal_type
        BDS_get_signal_unit=FWC_DIS_get_signal_unit
    elif bds_format == 'FWC_BNR':
        BDS_get_formated_name=FWC_BNR_get_formated_name
        BDS_get_label=FWC_BNR_get_label
        BDS_get_label_format=FWC_BNR_get_label_format
        BDS_get_sdi=FWC_BNR_get_sdi
        BDS_get_ssm_type=FWC_BNR_get_ssm_type
        BDS_get_parameter_format=FWC_BNR_get_parameter_format
        BDS_get_msb=FWC_BNR_get_msb
        BDS_get_parameter_name=FWC_BNR_get_parameter_name
        BDS_get_parameter_type=FWC_BNR_get_parameter_type
        BDS_get_nb_bits=FWC_BNR_get_nb_bits
        BDS_get_signed=FWC_BNR_get_signed
        BDS_get_resolution=FWC_BNR_get_resolution
        BDS_get_signal_name=FWC_BNR_get_signal_name
        BDS_get_signal_type=FWC_BNR_get_signal_type
        BDS_get_signal_unit=FWC_BNR_get_signal_unit
    elif bds_format == 'SDAC':
        BDS_get_formated_name=SDAC_get_formated_name
        BDS_get_label=SDAC_get_label
        BDS_get_label_format=SDAC_get_label_format
        BDS_get_sdi=SDAC_get_sdi
        BDS_get_ssm_type=SDAC_get_ssm_type
        BDS_get_parameter_format=SDAC_get_parameter_format
        BDS_get_msb=SDAC_get_msb
        BDS_get_parameter_name=SDAC_get_parameter_name
        BDS_get_parameter_type=SDAC_get_parameter_type
        BDS_get_nb_bits=SDAC_get_nb_bits
        BDS_get_signed=SDAC_get_signed
        BDS_get_resolution=SDAC_get_resolution
        BDS_get_signal_name=SDAC_get_signal_name
        BDS_get_signal_type=SDAC_get_signal_type
        BDS_get_signal_unit=SDAC_get_signal_unit
    else:
        sys.stderr.write('ERR: sheet '++' is of unknown format '+bds_type)
        exit(1)
    
    bdssheet=bdsfile.sheet_by_name(bds_sheet_name)
    for line_index in range(1, bdssheet.nrows):
        # the '#' character indicates a line to ignore
        if bdssheet.cell_value(line_index, 0)=='' or  bdssheet.cell_value(line_index, 0)[0] <> '#':
            if BDS_get_parameter_format(bdssheet, line_index) <> '':
                if BDS_get_signal_name(bdssheet, line_index) <> '':
                    label_name=BDS_get_formated_name(bdssheet, line_index)
                    parameter={}
                    parameter['name']=BDS_get_parameter_name(bdssheet, line_index)
                    parameter['format']=BDS_get_parameter_format(bdssheet, line_index)
                    parameter['type']=BDS_get_parameter_type(bdssheet, line_index)
                    parameter['signal_name']=BDS_get_signal_name(bdssheet, line_index)
                    parameter['signal_type']=BDS_get_signal_type(bdssheet, line_index)
                    parameter['nb_bits']=BDS_get_nb_bits(bdssheet, line_index)
                    parameter['msb']=BDS_get_msb(bdssheet, line_index)
                    parameter['resolution']=BDS_get_resolution(bdssheet, line_index)
                    parameter['signal_unit']=BDS_get_signal_unit(bdssheet, line_index)
                    parameter['signed']=BDS_get_signed(bdssheet, line_index)
                    
                    if bds_formating:
                        #Initialization of new empty label
                        if not ARINC_format_labels.has_key(label_name):
                            ARINC_format_labels[label_name]=['', '', '', '', '', []]
                            
                        #Filling label attributes
                        ARINC_format_labels[label_name][0]=label_name
                        ARINC_format_labels[label_name][1]=BDS_get_label_format(bdssheet, line_index)
                        ARINC_format_labels[label_name][2]=BDS_get_label(bdssheet, line_index)
                        ARINC_format_labels[label_name][3]=BDS_get_sdi(bdssheet, line_index)
                        ARINC_format_labels[label_name][4]=BDS_get_ssm_type(bdssheet, line_index)
                        
                        ARINC_format_labels[label_name][5].append(parameter)
                    else:
                        #Initialization of new empty label
                        if not ARINC_deformat_labels.has_key(label_name):
                            ARINC_deformat_labels[label_name]=['', '', '', '', '', []]
                            
                        #Filling label attributes
                        ARINC_deformat_labels[label_name][0]=label_name
                        ARINC_deformat_labels[label_name][1]=BDS_get_label_format(bdssheet, line_index)
                        ARINC_deformat_labels[label_name][2]=BDS_get_label(bdssheet, line_index)
                        ARINC_deformat_labels[label_name][3]=BDS_get_sdi(bdssheet, line_index)
                        ARINC_deformat_labels[label_name][4]=BDS_get_ssm_type(bdssheet, line_index)
                        
                        ARINC_deformat_labels[label_name][5].append(parameter)
                else:
                    sys.stderr.write('WAR: no signal name on '+bdssheet.name+':'+str(line_index+1)+' -> ignored\n')
                
    return [ARINC_format_labels, ARINC_deformat_labels]
    
###############################
## MAIN function
###############################
#Check command line
if len(sys.argv) <> 4:
    sys.stderr.write('usage: '+sys.argv[0]+' <bds2fdef file> <output directory> <model name>\n')
    sys.exit(1)
    
#read command line arguments
bds_file=sys.argv[1]
output_directory=sys.argv[2]
model_name=sys.argv[3]

#key=label_name, value=[name, type, number, sdi, [[param_name, param_format, param_type, sig_name, sig_type, nbbit, msb, resolution, unit], ...]]
ARINC_format_labels={}
ARINC_deformat_labels={}

# open BDS xls file
try:
    bdsfile = xlrd.open_workbook(filename=bds_file, logfile=sys.stdout, verbosity=0)
except:
    sys.stderr.write('ERR: cannot open '+ bds_file + '\n')
    sys.exit(1)

#Read selected worksheets. The Sheet name corresponds to a certain formating/deformatin attribute and a certain BDS format mode
for [bds_sheet_name, bds_formating, bds_format] in [['toEIS', True, 'EIS'], ['fromEIS', False, 'EIS'],
                                                    ['toFWC(DIS)', True, 'FWC_DIS'], ['fromFWC(DIS)', False, 'FWC_DIS'],
                                                    ['toFWC(BNR)', True, 'FWC_BNR'], ['fromFWC(BNR)', False, 'FWC_BNR'],
                                                    ['toSDAC', True, 'SDAC']]:
    [ARINC_format_labels, ARINC_deformat_labels] = read_bds_sheet(ARINC_format_labels, ARINC_deformat_labels, bds_sheet_name, bds_formating, bds_format)

#Open Excel MICD template file for writing
appdir = os.path.dirname(sys.argv[0])
if appdir == '':
    appdir = '.'

MICD_template_file=xlrd.open_workbook(filename=appdir+'/ICD_template.xls', formatting_info=True, logfile=sys.stdout, verbosity=0)
MICD_file=xlutils.copy.copy(MICD_template_file)

MICD_title_style=xlwt.XFStyle()
MICD_title_style.font=xlwt.Font()
MICD_title_style.font.bold=True
MICD_title_style.pattern=xlwt.Pattern()
MICD_title_style.pattern.pattern=xlwt.Pattern.SOLID_PATTERN
MICD_title_style.pattern.pattern_fore_colour=7
MICD_title_style.alignment=xlwt.Alignment()
MICD_title_style.alignment.wrap=True
MICD_title_style.alignment.vert=0

#Create basic FUN_IN and the title line
MICD_fun_in_titles=['Name', 'Type', 'Unit', 'Description', 'Convention', 'Dim1', 'Dim2', 'Com Format',
                        'Com Mode', 'From', 'Refresh\nRate', 'Min', 'Max', 'Enum', 'Consumed\nIf', 'Aircraft Signal\nName',
                        'Interface\nLevel', 'Status (SSM/FS/Refresh)', 'Simulation\nLevel [1]', 'Init\nValue',
                        'Custom', 'Comment', 'Last Modification']
MICD_fun_in=MICD_file.add_sheet('FUN_IN')
for title in MICD_fun_in_titles:
    MICD_fun_in.write(0, MICD_fun_in_titles.index(title), title, MICD_title_style)

#Create basic FUN_OUT and the title line
MICD_fun_out_titles=['Name', 'Type', 'Unit', 'Description', 'Convention', 'Dim1', 'Dim2', 'Com Format',
                        'Com Mode', 'To', 'Refresh\nRate', 'Min', 'Max', 'Enum', 'Produced\nIf', 'Aircraft Signal\nName',
                        'Interface\nLevel', 'Status (SSM/FS/Refresh)', 'Simulation\nLevel [1]', 'Comment',
                        'Not Simulated Data', 'Default Value', 'Last Modification']
MICD_fun_out=MICD_file.add_sheet('FUN_OUT')
for title in MICD_fun_out_titles:
    MICD_fun_out.write(0, MICD_fun_out_titles.index(title), title, MICD_title_style)

for [xml_filename, ARINC_labels, MICD_format_worksheet, MICD_preformat_worksheet] in [['A429_prod_'+model_name+'.xml', ARINC_format_labels, MICD_fun_out, MICD_fun_in], ['A429_conso_'+model_name+'.xml', ARINC_deformat_labels, MICD_fun_in, MICD_fun_out]]:
    #Create dictionnary to store ports writen and prevent duplications
    dict_ports = {}
    #Create xml directory if it does not exist
    xml_dir_path = output_directory+'/xml'
    if not os.path.exists(xml_dir_path):
        os.makedirs(xml_dir_path)

    
    #Open FDEF XML file for writing
    ARINC_file=open(xml_dir_path+'/'+xml_filename, 'w')

    #Write head of file
    ARINC_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    DT = time.strftime("%d/%m/%Y %Hh%Mm",time.localtime())
    ARINC_file.write('<configurationTable type="A429" generationDate="'+DT+'" generationTool="BDS2FDEF">\n')
    #ARINC_file.write('<configurationTable>\n')
    ARINC_file.write('\t<configurationSources>\n')
    ARINC_file.write('\t\t<sourceFile type="'+bds_format+' BDS" pathname="'+os.path.abspath(bds_file)+'"/>\n')
    ARINC_file.write('\t</configurationSources>\n')
    ARINC_file.write('\t<configurationEntity>\n')
    
    ARINC_label_keys=ARINC_labels.keys()
    ARINC_label_keys.sort()
    for label_key in ARINC_label_keys:
        label=ARINC_labels[label_key]
        label_names=string.split(label[0], ':')
        # Remove duplicates entries in label_names
        label_names = list(set(label_names))
        parameters_already_declared=False
        for label_name in label_names:
            if not label_name in dict_ports:
                dict_ports[label_name] = None

                #The refreshRate attribute is mandatory but it is not read if not using the /REFRESH_RETA_COEFF of fdef's GAC
                ARINC_file.write('\t\t<A429Label name="'+label_name+'" type="'+label[1]+'" labelNumber="'+label[2]+'" sdi="'+label[3]+'">\n')
            
                #get MICD new row index
                MICD_format_new_row=len(MICD_format_worksheet.get_rows())
            
                #add formated ARINC
                MICD_format_worksheet.write(MICD_format_new_row, 0, label_name)
                MICD_format_worksheet.write(MICD_format_new_row, 1, 'int')
                MICD_format_worksheet.write(MICD_format_new_row, 2, 'wu')
                MICD_format_worksheet.write(MICD_format_new_row, 5, '1')
                MICD_format_worksheet.write(MICD_format_new_row, 6, '1')
                MICD_format_worksheet.write(MICD_format_new_row, 7, 'ARINC')
                MICD_format_worksheet.write(MICD_format_new_row, 8, 'S')
                MICD_format_worksheet.write(MICD_format_new_row, 13, 'False/True')
                MICD_format_worksheet.write(MICD_format_new_row, 15, '/not_available/')
                MICD_format_worksheet.write(MICD_format_new_row, 16, 'Format')
                MICD_format_worksheet.write(MICD_format_new_row, 17, 'False')
                
                if not (label_name+'_R') in dict_ports:
                    dict_ports[label_name+'_R'] = None

                    #add formated ARINC status
                    MICD_format_worksheet.write(MICD_format_new_row+1, 0, label_name+'_R')
                    MICD_format_worksheet.write(MICD_format_new_row+1, 1, 'boolean')
                    MICD_format_worksheet.write(MICD_format_new_row+1, 2, 'wu')
                    MICD_format_worksheet.write(MICD_format_new_row+1, 5, '1')
                    MICD_format_worksheet.write(MICD_format_new_row+1, 6, '1')
                    MICD_format_worksheet.write(MICD_format_new_row+1, 7, 'ARINC')
                    MICD_format_worksheet.write(MICD_format_new_row+1, 8, 'S')
                    MICD_format_worksheet.write(MICD_format_new_row+1, 13, 'False/True')
                    MICD_format_worksheet.write(MICD_format_new_row+1, 15, '/not_available/')
                    MICD_format_worksheet.write(MICD_format_new_row+1, 16, 'Format')
                    MICD_format_worksheet.write(MICD_format_new_row+1, 17, 'True')
                
            
                    #creates SSM if there is more than 1 parameter
                    if len(label[5]) > 0:
                        ARINC_file.write('\t\t\t<ssm type="'+label[4]+'">\n');
                        ARINC_file.write('\t\t\t\t<parameter name="'+label_name+'_SSM" type="status" comment="'+label[1]+' SSM LABEL '+label_name+'">\n')
                        ARINC_file.write('\t\t\t\t\t<signal name="'+label_name+'_SSM"/>\n')
                        ARINC_file.write('\t\t\t\t</parameter>\n')
                        ARINC_file.write('\t\t\t</ssm>\n');

                    #loop for each parameter in the ARINC label
                    for parameter in label[5]:                    
                        ARINC_file.write('\t\t\t<parameter name="'+parameter['name']+'" type="'+parameter['type']+'">\n')
                        ARINC_file.write('\t\t\t\t<signal name="'+parameter['signal_name']+'" type="'+parameter['signal_type']+'" nbBit="'+str(parameter['nb_bits'])+'" lsb="'+str(parameter['msb']-parameter['nb_bits']+1)+'" msb="'+str(parameter['msb'])+'" signed="'+str(parameter['signed'])+'">\n')
                        if parameter['format'] in ['BNR', 'BCD']:
                            ARINC_file.write('\t\t\t\t\t<float floatResolution="'+str(parameter['resolution'])+'" floatCodingType="'+parameter['format']+'"/>\n')
                        ARINC_file.write('\t\t\t\t</signal>\n')
                        ARINC_file.write('\t\t\t</parameter>\n')
                        
                     #   if not parameters_already_declared: # to prevent double declaration due of the "for label_name" loop
                            #get MICD new row index
                        MICD_preformat_new_row=len(MICD_preformat_worksheet.get_rows())
                    
                    
                        #add SSM
                        if not (label_name+'_SSM') in dict_ports:
                            dict_ports[label_name+'_SSM'] = None

                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 0, label_name+'_SSM')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 1, 'int')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 2, 'wu')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 4, '0="NO"/2="NE"/4="NCD"/8="FW"/16="FT"')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 5, '1')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 6, '1')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 7, 'ARINC')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 8, 'S')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 13, 'False/True')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 15, '/not_available/')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 16, 'Preformat')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 17, 'True')
                            MICD_preformat_new_row+=1

                        #add preformated data in MICD
                        if not (parameter['signal_name']) in dict_ports:
                            dict_ports[parameter['signal_name']] = None
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 0, parameter['signal_name'])
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 1, parameter['signal_type'])
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 2, parameter['signal_unit'])
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 3, parameter['name'])
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 5, '1')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 6, '1')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 7, 'ARINC')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 8, 'S')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 15, '/not_available/')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 16, 'Preformat')
                            MICD_preformat_worksheet.write(MICD_preformat_new_row, 17, 'False')
                            
                    #parameters_already_declared=True

                    ARINC_file.write('\t\t</A429Label>\n')

    #Write end of file
    ARINC_file.write('\t</configurationEntity>\n')
    ARINC_file.write('</configurationTable>\n')

    #close file
    ARINC_file.close()

# close MICD file
MICD_file.save(output_directory+'/ICD_'+model_name+'.xls')
