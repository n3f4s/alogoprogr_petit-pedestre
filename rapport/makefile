#### TODO : refaire pour un nombre de .tex indeterminer : cf wikibook gros fichiers

#### Définition des cibles particulières
.PHONY: clean, mrproper

#### Désactivation des règles implicites
.SUFFIXES:

#### Variables :
## Listage des .mp
TMP=$(wildcard *.mp)
## Lsitage des .1 en remplaçant les .mp par des .1 dans les noms de fichiers
MP= $(TMP:.mp=.1)

#### Rêgles

## Création du pdf, le pdf est compilé deux fois pour la re-génération de la table des matières
all: pdf

## Création des fichiers UML
%.1:%.mp
	@mpost $<

## Etapes de compilation
# Création du .dvi a partir du .tex
dvi: 
	latex rapport.tex

# Création .ps à partir du .dvi
ps: dvi
	dvips rapport.dvi

# Création du pdf a partir du .ps
pdf: ps
	ps2pdf rapport.ps

