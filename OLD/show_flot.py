#!/usr/local/bin/python
import sys
sys.path.append("/home/st07564/OCASIME/DEVELOPPEMENT/PYTHON/MODULES/")
sys.path.append("/home/st07564/OCASIME/DEVELOPPEMENT/PYTHON/DOWNLOAD/elementtree-1.2.6-20050316/")
from Genere_flot_xml_3 import Genere_flot_xml
from HtmlConverter import HtmlConverter
import re
import string
import time
from cElementTree import Element, ElementTree
import cElementTree as ET


#parametres
fichier_flot=sys.argv[1]
nom_modele=sys.argv[2]

# parsing du flot et creation du xml_flot
tree=Genere_flot_xml(fichier_flot)
racine=tree.getroot()



print "recherche des ports pour le modele:*"+nom_modele+"*"

canaux_prod_a_traiter=ET.Element("PROD_A_TRAITER")
canaux_conso_a_traiter=ET.Element("CONSO_A_TRAITER")

# creation de l arbre de sortie
tree_show_flot = ET.Element("SHOW_FLOT")
tree_show_flot.set("modele", nom_modele)
canaux_prod = ET.SubElement(tree_show_flot, "CANAUX_PRODUITS")
canaux_conso = ET.SubElement(tree_show_flot, "CANAUX_CONSOMMES")

# extraction de la liste des canaux produits ou consommes par le modele
for canaux in racine.findall(".//CANAL/"):
	for ports in canaux.findall(".//PRODUCTEUR"):	
		if ports.get("modele")==nom_modele:
			canaux_prod_a_traiter.append(canaux)
	for ports in canaux.findall(".//CONSOMMATEUR"):	
		if ports.get("modele")==nom_modele:
			canaux_conso_a_traiter.append(canaux)		

#ET.dump(canaux_prod_a_traiter)
#ET.dump(canaux_conso_a_traiter)		

# suppression des consommateurs n appartenant pas au modele
for canal in canaux_conso_a_traiter:
	for conso in canal.findall(".//CONSOMMATEUR"):
		if not conso.get("modele")==nom_modele:
			canal.remove(conso)

# liste des canaux produits
for canal in canaux_prod_a_traiter:
	canaux_prod.append(canal)
for canal in canaux_conso_a_traiter:
	canaux_conso.append(canal)
			
#ET.dump(tree_show_flot)
		
