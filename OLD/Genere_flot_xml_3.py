#!/usr/local/bin/python
import sys
sys.path.append("/home/st07564/OCASIME/DEVELOPPEMENT/PYTHON/MODULES/")
sys.path.append("/home/st07564/OCASIME/DEVELOPPEMENT/PYTHON/MODULES/Elementtree-1.2.6/")
from Parse_initflot import parse_init
import re
import string
import time
from cElementTree import Element, ElementTree

# import main module under an alias
import cElementTree as ET

# Ce module permet de generer un arbre XML a partir d un flot


def Genere_flot_xml(fichier_flot):

	# definition des patterns pour parsing du flot
	pattern_canal=re.compile("^Canal:\s(\w*)")
	pattern_producteur=re.compile("^Port producteur:\s(\w+)")
	pattern_consommateur=re.compile("^Ports consommateurs:\s(\w+)")
	pattern_modele=re.compile("(?:\s)(\w+)\/(\d+)\/(\w+)\s(\w+)?\s?((?:\[|\])\d;\d(?:\[|\]))?\s?,?")
	
	# ouverture du fichier
	try:
		flot=open(fichier_flot,'r')
	except IOError:
		print '[Genere_flot_xml]: Impossible d ouvrir le fichier flot ' + fichier_flot
		sys.exit(0)
	
	# creation de l arbre XML
	racine = ET.Element("FLOT")
	racine.set("origine", fichier_flot)
	racine.set("date_creation", time.strftime('%X %x %Z'))
	
	# flag pour fichier init
	flag=0
	inits={}
	
	ligne=flot.readline()
	
	while ligne !="":
	
		# recherche un fichier d'init
		if re.match("^Fichier:\s(.)+",ligne):
			
			fichier_init=re.split("\s",ligne)[1]
			#print fichier_init
			inits=parse_init(fichier_init)
			if (not inits):
				print '[Genere_flot_xml]: => pas d inits dans le flot xml genere'
			else:
				flag=1
			
		# lecture de la ligne courante
		ligne=flot.readline()
			
		if pattern_canal.match(ligne):
			
			canal=pattern_canal.split(ligne)[1]
			
			# nom du canal
			element_canal = ET.SubElement(racine, "CANAL")	
			element_canal.set("nom", canal)
			
			
			# canal initialise ?
			if(flag==1):
				if canal in inits.keys():
					element_canal.set("valeur_init", inits[canal])
	
			ligne=flot.readline()
			
			if (pattern_producteur.match(ligne) or pattern_consommateur.match(ligne)):
			
				if pattern_producteur.match(ligne):
						
					infos_producteur=pattern_modele.findall(ligne)
		 
					element_producteur=ET.SubElement(element_canal,"PRODUCTEUR")
					element_producteur.set("port", infos_producteur[0][2])
					if infos_producteur[0][3] != "":
						element_producteur.set("operateur", infos_producteur[0][3])
					if (infos_producteur[0][4] != ""):
						element_producteur.set("tableau", infos_producteur[0][4])				
					
					element_producteur.set("modele", infos_producteur[0][0])
					element_producteur.set("occurence", infos_producteur[0][1])
						
					ligne=flot.readline()
						
				if pattern_consommateur.match(ligne):
					
					infos_consommateurs=pattern_modele.findall(ligne)
					
					for conso in infos_consommateurs[:]:
						element_consommateur=ET.SubElement(element_canal,"CONSOMMATEUR")
						element_consommateur.set("port", conso[2])
						if conso[3] != "":
							element_consommateur.set("operateur", conso[3])
						if (conso[4] != ""):
							element_consommateur.set("tableau", conso[4])
						
						element_consommateur.set("modele", conso[0])
						element_consommateur.set("occurence", conso[1])
							
					ligne=flot.readline()
			else:
				print '[Genere_flot_xml]: Probleme lors du parsing du flot pour le canal: ' + canal
				sys.exit(0)				
	#fermeture des fichiers
	flot.close()
	doc = ET.ElementTree(racine)
		
	return doc
