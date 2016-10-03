#!/usr/local/bin/python
import sys
import re
import string


# Prend en parametre le nom d un fichier initflot
# et renvoi un dictionnaire des valeurs d inits de la forme tab[canal]=init
def parse_init(file):
	
	#dictionnaire vide
	tab_init={}
	
	#pattern pour parsing
	pattern_init_canal=re.compile("^Canal:\s(\w*)")
	#pattern_init_valeur=re.compile("^\s*(?!Canal:)[^#]+$\n")
	pattern_init_valeur=re.compile("^\s*(?!Canal:)([^#]+$)\n")
	
	#ouverture du fichier
	try:
		fichier=open(file,'r')
	except IOError:
		print 'Impossible d ouvrir le fichier: ' + file
		return tab_init
		
	#lecture du fichier
	ligne_init=fichier.readline()
	
	#compteur de lignes
	compteur=1
	while ligne_init != "":
		if pattern_init_canal.match(ligne_init):
		
			# nom du canal
			canal=pattern_init_canal.findall(ligne_init)[0]

			# lecture d'une ligne supplementaire
			ligne_init=fichier.readline()
			compteur+=1

			# si la ligne ne comporte pas de valeur d init
			if (not pattern_init_valeur.match(ligne_init)):

				# on passe a la ligne suivante tant que il n y a pas de valeur d init
				while (not pattern_init_valeur.match(ligne_init) and (not pattern_init_canal.match(ligne_init)) ):
					ligne_init=fichier.readline()
					compteur+=1
				
				# si on retombe sur un nouveau canal => pas d  init pour le canal precedent
				if(pattern_init_canal.match(ligne_init)):
					print "[Parse_init.py] Warning dans le fichier initflot, "
					print "[Parse_init.py] le canal "+canal+" a la ligne %d n a pas de valeur d init !" % compteur
					init=""
					continue
				# si on tombe sur une valeur d init => OK
				else:
					init=pattern_init_valeur.findall(ligne_init)[0]	
			# cas nominal => valeur d init
			else:
				init=pattern_init_valeur.findall(ligne_init)[0]
			
			tab_init[canal]=init

		ligne_init=fichier.readline()
		compteur+=1
	fichier.close()
	return tab_init
		
