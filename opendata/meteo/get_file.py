import wget
import os
import datetime
from sh import gunzip

path = "/home/patricemazel/opendata/data/meteo"
base_url = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/synop."
extension = ".csv.gz"
extension_csv = ".csv"

now = datetime.datetime.now()
annee_en_cours = now.year
mois_en_cours = now.month

annee_min = 1996

# Détermination de l'année maximale
if mois_en_cours == 12 :
    annee_max = annee_en_cours - 1
else:
    annee_max = annee_en_cours

# Boucle sur les années et les mois
for annee_iter in range(annee_min, annee_max + 1):
    print("Traitement Année = %s" %annee_iter)

    # determination du mois maximum
    if annee_iter == annee_en_cours:
        mois_max = mois_en_cours - 1
    else:
        mois_max = 12

    print("Mois Maximum : %s" %str(mois_max))

    for mois_iter in range(0,mois_max):
        print("-- Mois = %s" %str(mois_iter+1))
        # Creation nom url
        mois_iter_str = ("00" + str(mois_iter+1))[-2:]
        url = base_url + str(annee_iter) + mois_iter_str + extension
        print("-- -- URL : %s" %url)
        # Nom du fichier destination
        file_name = url.split('/')[-1]
        destination = path + '/' + file_name
        destination_csv = path + '/' + 'synop.' + str(annee_iter) + mois_iter_str + extension_csv

        print("-- -- Nom Fichier     : %s" %(file_name))
        print("-- -- Destination gz  : %s" %(destination))
        print("-- -- Destination csv : %s" %(destination_csv))

        # Suppression du fichier gz
        try:
            os.remove(destination)
        except OSError:
            pass

        # Suppression du fichier csv
        try:
            os.remove(destination_csv)
        except OSError:
            pass

        # Recuperation du fichier
        wget.download(url, destination)
        # Decompression du fichier
        gunzip(destination)

