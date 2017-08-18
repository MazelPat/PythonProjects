import wget
import os
import datetime
import sh
import sys

# maps label to attribute name and types
label_attr_map = {
    "path_to_file:": ["path_to_file", str],
    "base_url:": [ "base_url", str],
    "extension:": [ "extension", str],
    "extension_csv:": [ "extension_csv", str],
    "annee_min:": [ "annee_min", int]
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

print('parameter file : ', sys.argv[1])

params = Params(sys.argv[1])

print('params.path_to_file :', params.path_to_file)
print('params.base_url :', params.base_url)
print('params.extension :', params.extension)
print('params.extension_csv :', params.extension_csv)
print('params.annee_min :', params.annee_min)

path = params.path_to_file
base_url = params.base_url
extension = params.extension
extension_csv = params.extension_csv
annee_min = params.annee_min

now = datetime.datetime.now()
annee_en_cours = now.year
mois_en_cours = now.month

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
        sh.gunzip(destination)

