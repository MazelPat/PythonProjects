# Import général
import wget
import os
import datetime
import sh
import sys

# Import pour les logs
import logging

from logging.handlers import RotatingFileHandler

# maps label to attribute name and types
label_attr_map = {
    "path_to_file:": [ "path_to_file", str],
    "base_url:": [ "base_url", str],
    "extension:": [ "extension", str],
    "extension_csv:": [ "extension_csv", str],
    "annee_min:": [ "annee_min", int],
    "screen:": [ "screen", int]
}

class Params(object):
    def __init__(self, input_file_name):
        with open(input_file_name, 'r') as input_file:
            for line in input_file:
                row = line.split()
                label = row[0]
                data = row[1:]  # rest of row is data list

                attr = label_attr_map[label][0]
                datatypes = label_attr_map[label][1:]

                values = [(datatypes[i](data[i])) for i in range(len(data))]
                self.__dict__[attr] = values if len(values) > 1 else values[0]

# Début du script

params = Params(sys.argv[1])

now = datetime.datetime.now()
annee_en_cours = now.year
mois_en_cours = now.month
jour_en_cours = now.day

file_to_log = sys.argv[2] + 'get_meteo_' + str(annee_en_cours) + '_' + ("00" + str(mois_en_cours))[-2:] + '_' + ("00" + str(jour_en_cours))[-2:] + '.log'

# Parametrage des logs

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.INFO)

# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
# création d'un handler qui va rediriger une écriture du log vers
# un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
file_handler = RotatingFileHandler(file_to_log, 'a', 1024 * 1024 * 1, 1)
# on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
# créé précédement et on ajoute ce handler au logger
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# création d'un second handler qui va rediriger chaque écriture de log
# sur la console
if params.screen == 1:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

logger.info('Start Import Meteo Files')

logger.info('parameter file : %s' %sys.argv[1])
logger.info('log file       : %s' %file_to_log)

logger.info('params.path_to_file : %s' %params.path_to_file)
logger.info('params.base_url : %s' %params.base_url)
logger.info('params.extension : %s' %params.extension)
logger.info('params.extension_csv : %s'  %params.extension_csv)
logger.info('params.annee_min : %s' %str(params.annee_min))

path = params.path_to_file
base_url = params.base_url
extension = params.extension
extension_csv = params.extension_csv
annee_min = params.annee_min

# Détermination de l'année maximale
if mois_en_cours == 12 :
    annee_max = annee_en_cours - 1
else:
    annee_max = annee_en_cours

# Boucle sur les années et les mois
for annee_iter in range(annee_min, annee_max + 1):
    logger.info("Traitement Année = %s" %annee_iter)

    # determination du mois maximum
    if annee_iter == annee_en_cours:
        mois_max = mois_en_cours - 1
    else:
        mois_max = 12

    logger.info("Mois Maximum : %s" %str(mois_max))

    for mois_iter in range(0,mois_max):
        logger.info("-- Mois = %s" %str(mois_iter+1))
        # Creation nom url
        mois_iter_str = ("00" + str(mois_iter+1))[-2:]
        url = base_url + str(annee_iter) + mois_iter_str + extension
        logger.info("-- -- URL : %s" %url)
        # Nom du fichier destination
        file_name = url.split('/')[-1]
        destination = path + '/' + file_name
        destination_csv = path + '/' + 'synop.' + str(annee_iter) + mois_iter_str + extension_csv

        logger.info("-- -- Nom Fichier     : %s" %(file_name))
        logger.info("-- -- Destination gz  : %s" %(destination))
        logger.info("-- -- Destination csv : %s" %(destination_csv))

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
        sh.gunzip(destination)

logger.info('End Import Meteo Files')