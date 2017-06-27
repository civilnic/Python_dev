#!/usr/bin/env python
# coding: utf-8

import socket
import threading
import os
import sys

Commands = dict()
Commands["SEND_ME_STATUS"] = "I'M_OK"
Commands["START_LIST_DATA_SENDING"] = "HERE_IS_LIST_STATUS_SENDING"
Commands["SEND_ME_LIST_STATUS_SENDING"] = "HERE_IS_LIST_STATUS_SENDING"
Commands["SEND_ME_LISTED_PARAM_INFO"] = "HERE_IS_LISTED_PARAM_INFO"
Commands["SEND_ME_TEST_LABEL"] = "HERE_IS_TEST_LABEL"

Answer = dict()
Answer["I'M_OK"] = None
Answer["HERE_IS_LIST_STATUS_SENDING"] = ["%s\t%u\t%s\t%s\t%u\t%u\t%u"]
Answer["HERE_IS_LISTED_PARAM_INFO"] = ["%s\t%u","\t%u\t%s\t%u\t%u\t%s\t%u\t%u\t%u\t%u"]
Answer["HERE_IS_TEST_LABEL"] = ["%s\t%s\t%s\t%s\t%s\t%s"]

SEPARATOR = '\t'

class DataServer:

    def __init__(self, dataservFile):

        self.version = None
        self.list = dict()

        try:
            _myDataServerFile = open(dataservFile, 'r')
        except FileNotFoundError:
            print("Cannot open Parameter attributes files: "+dataservFile)
            exit(1)

        for _line in _myDataServerFile:
            _line = _line.rstrip('\n\r\t')
            _field = _line.split('=')
            if _field[0] == "VERSION":
                self.version = int(_field[1])
            if _field[0] == "LISTE":

                # creation du nom du fichier specifique pour les attributs des parametres
                _fileName, _fileExtension = os.path.splitext(_field[1])
                _paramSpecFileName = _fileName+"_PARAM_SPEC"+_fileExtension

                # data list object creation
                _mydatalistObj = DataList(_field[1], _paramSpecFileName)

                # list name => List Object
                self.list[_mydatalistObj.listName] = _mydatalistObj

    def get_list(self, listname):
        if listname in self.list.keys():
            listObj = self.list[listname]
            # return application name
            return listObj
        else:
            return None

class Param:
    def __init__(self, tab, index):
        self.name = tab[0]
        self.ident = index
        self.type = tab[1]
        self.size = tab[2]
        self.unit = tab[3]
        self.freq = tab[4]
        self.offset = tab[5]
        self.msb = tab[6]
        self.lenght = tab[7]

    def get_sprintf_values(self):
        return (int(self.ident), str(self.name), int(self.type), int(self.size), str(self.unit), int(self.freq), int(self.offset), int(self.msb), int(self.lenght))

class DataList:

    def __init__(self, datalistFile, paramSpecFile):

        self.version = None
        self.ident = None
        self.clientName = None
        self.listName = None
        self.freq = None
        self.mode = None
        self.param = list()
        self.paramSpec = dict()

        try:
            _myParamFile = open(paramSpecFile,'r')
        except FileNotFoundError:
            print("Cannot open Parameter attributes files: "+paramSpecFile)

        _cmpt = 0
        for _line in _myParamFile:
            _line = _line.rstrip('\n\r\t')
            _field = _line.split(',')

            self.paramSpec[_field[0]] = Param(_field, _cmpt)
            _cmpt += 1


        try:
            _myFile = open(datalistFile, "r")
        except FileNotFoundError:
            print("Cannot open Data List file: "+datalistFile)

        for _line in _myFile:

            _line = _line.rstrip('\n\r\t')

            _field = _line.split('=')

            if _field[0] == "VERSION":
                self.version = int(_field[1])
            if _field[0] == "IDENT_LISTE":
                self.ident = int(_field[1])
            if _field[0] == "NOM_CLIENT":
                self.clientName = _field[1]
            if _field[0] == "NOM_LISTE":
                self.listName = _field[1]
            if _field[0] == "CAD_EMISSION":
                self.freq = int(_field[1])
            if _field[0] == "MOD_ECHANT":
                if _field[1] == "ALL_SAMPLE":
                    self.mode = 2
                if _field[1] == "ONE_SAMPLE":
                    self.mode = 1

            if _field[0] == "PARAM":
                if _field[1] not in self.paramSpec.keys():
                    print("Missing parameter in paramSpec file: "+_field[1])
                    exit(1)
                else:
                    self.param.append(_field[1])

    def get_paramNumber(self):
        return len(self.paramSpec.keys())

    def get_paramList(self):
        return self.param

    def get_paramObj(self,paramName):
        if paramName in self.paramSpec.keys():
            return self.paramSpec[paramName]
        else:
            return None


class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket, dataservobj,IPMulticast):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        self.multicastIP = IPMulticast
        self.dataServObj = dataservobj
        self.running = False

        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self):

        self.running = True
        print("Connection de %s %s" % (self.ip, self.port,))

        while self.running is True:

            # initialise empty buffer
            _headerBuffer = bytearray(50)


            #
            # wait to SEND ME STATUS command from client
            #
            r = self.clientsocket.recv_into(_headerBuffer, 50)
            print("Commande reçue: ", _headerBuffer, "...")

            # Convert bytearray back into a string.
            _header = _headerBuffer.decode("ascii")

            # remove null character
            _header = _header.rstrip('\0')

            # split command /t body_size
            _tmp = _header.split('\t')

            _command = _tmp[0]
            _body_size = _tmp[1]

            print("_command decodee: ", _command, "...")
            print("_body_size decodee: ", _body_size, "...")

            if _command not in Commands.keys():
                print("Unknown command: "+_command)
                print("Client déconnecté...")
                self.running = False
                break

            _bodyContent = ()

            if int(_body_size) > 0:

                # initialise body buffer
                _bodyBuffer = bytearray(int(_body_size))

                # receive body frame
                r = self.clientsocket.recv_into(_bodyBuffer, int(_body_size))
                print("Body reçu: ", _bodyBuffer, "...")

                # Convert bytearray back into a string.
                _body = _bodyBuffer.decode("ascii")

                # remove null character
                _body = _body.rstrip('\0')

                # split command /t body_size
                _bodyContent = _body.split('\t')
                print("_bodyContent: ", _bodyContent, "...")

            # prepare answer
            _Hanswer,_Banswer,_flag = self.answer(_command, _bodyContent,self.dataServObj,self.multicastIP )

            if _Hanswer is None:
                print("ERROR ...")
                print("Client déconnecté...")
                self.running = False
                break
            # send header
            self.clientsocket.send(_Hanswer)


            if _Banswer is not None:
                # send body
                self.clientsocket.send(_Banswer)


            if _flag == "END_OF_CONNEXION":
                print("END_OF_CONNEXION: Client déconnecté...")

                self.running = False
                break

    def stop(self):
        self.running = False



    def answer(self,commandName ,BodyListContent,dataServObj,IPMulticast):

        if commandName in Commands.keys():

            if commandName == "SEND_ME_LIST_STATUS_SENDING":
                listStatus = 0
                SendingComment = "WAIT_FOR_START"
                multicastAddress = "0.0.0.0"
            else:
                listStatus = 1
                SendingComment = "OK_SENDING"
                #multicastAddress = "225.0.0.1"
                multicastAddress = IPMulticast

            # get answer to send
            _answerName = Commands[commandName]

            print("_answerName: "+_answerName)
            # default body size is null
            _bodySize = 0
            _body = ""

            # get answer body format:
            if Answer[_answerName] is not None:

                _format = Answer[_answerName]

                print(_format)

                # HERE_IS_LISTED_PARAM_INFO case
                if len(_format) > 1:

                    print("BodyListContent[1]: " + BodyListContent[1])
                    # check application name compared to dataserver information
                    _listObj = dataServObj.get_list(BodyListContent[1])

                    if _listObj is None:
                        print("List name: "+BodyListContent[1]+" is not referenced on dataserver")
                        return (None,None,None)

                    else:
                        if _listObj.clientName != BodyListContent[0]:
                            print("Application name: " + BodyListContent[0] + " does correspond to list: " /
                                                                        BodyListContent[1] + " on dataserver")
                            return (None, None, None)

                    _body = BodyListContent[1] + SEPARATOR
                    print("get_paramNumber: "+ str(_listObj.get_paramNumber()))
                    _body += str(_listObj.get_paramNumber())

                    for _paramName in _listObj.get_paramList():
                        _paramObj = _listObj.get_paramObj(_paramName)
                        if _paramObj is not None:
                            print(_paramObj.get_sprintf_values())
                            print(_format[1])
                            _body += _format[1] % _paramObj.get_sprintf_values()

                    print("body: " + _body)

                # HERE_IS_LIST_STATUS_SENDING case
                else:
                    print("BodyListContent[1]: " + BodyListContent[1])
                    # check application name compared to dataserver information
                    _listObj = dataServObj.get_list(BodyListContent[1])

                    if _listObj is None:
                        print("List name: "+BodyListContent[1]+" is not referenced on dataserver")
                        return (None,None,None)
                    else:
                        if _listObj.clientName != BodyListContent[0]:
                            print("Application name: " + BodyListContent[0] + " does correspond to list: " /
                                                                        BodyListContent[1] + " on dataserver")
                            return (None, None, None)

                    _body = BodyListContent[1]+SEPARATOR+str(listStatus)+SEPARATOR+SendingComment+SEPARATOR +\
                          multicastAddress+SEPARATOR+str(_listObj.ident)+SEPARATOR+str(_listObj.mode)+SEPARATOR + \
                          str(_listObj.freq)
                    print("body: "+_body)

            else:
                _body = ''

            # body size computation
            _bodySize = len(_body)

            # headercomputation
            _header = _answerName+SEPARATOR+str(_bodySize)

            # add null character to have an header size of 50 carac

            _header += (50-len(_header)) * '\0'

            print("header: " +  _header)

            if _body != '':
                if _answerName == "HERE_IS_LISTED_PARAM_INFO":
                    return( bytearray(_header, 'ascii'), bytearray(_body, 'ascii'),'END_OF_CONNEXION' )
                else:
                    return( bytearray(_header, 'ascii'), bytearray(_body, 'ascii'), None )
            else:
                return (bytearray(_header, 'ascii'), None, None)

if __name__ == '__main__':

    _myDataServerObj = DataServer(sys.argv[1])
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind(("", int(sys.argv[2])))

    _multicastAddress = sys.argv[3]

    while True:
        tcpsock.listen(10)
        print("Serveur actif ...\nEn écoute...")
        (clientsocket, (ip, port)) = tcpsock.accept()
        print("AdresssIP: "+str(ip)+"  Port: "+str(port))
        newthread = ClientThread(ip, port, clientsocket,_myDataServerObj,_multicastAddress)
        newthread.start()