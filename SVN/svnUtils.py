#!/home/dpmgr/tools/PYTHON/2.3.3/solaris2.8/bin/python
# -*- coding: iso-8859-1 -*-

#-------------------- Header/Title block ---------------------------
# . svnUtils
# . Command line arguments
# . Script inputs/outputs
# . Return code
# . Script execution conditions
# . Script general description
#--------------------------------------------------------------------
# . Configuration and modification management
#--------------------------------------------------------------------
__version__ = "1.0"
__date__ = "09/03/17"
__author__ = "SHT (N.BONNET)"
# + history if possible
#   09/03/17 - Module creation
#-------------------- Instruction 'IMPORT' --------------------------
# Declaration of imported modules
#--------------------------------------------------------------------

import sys
import httplib

#---------------------- Implementation ------------------------------
# Implementation of functions/classes/methods/main
#--------------------------------------------------------------------

class URL_STATUS:
    UNKNOWN = 0
    OK = 1
    KO = -1

class svnRepo:

    def __init__(self, url):

        self._url = url
        self._urlValidity = URL_STATUS.UNKNOWN

    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, url):
        self._urlValidity = URL_STATUS.UNKNOWN
        self._url = url



    def export(self, dest):
        pass

    def info(self,dest):
        pass

    def checkAccessRights(self, user):
        pass

    def testUrl(self):

        c = httplib.HTTPConnection(self.url)
        c.request("HEAD", '')
        if c.getresponse().status == 200:
            print('SVN url exists')
        pass
