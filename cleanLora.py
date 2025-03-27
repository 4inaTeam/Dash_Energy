import csv
import os
import re
import time
from datetime import datetime
# Fichier source et fichier nettoyé
input_file = "donnees.csv"
output_file = "clean.csv"
output_file2 = "temporal_data/min_data.csv"
index_file = "index.txt"
# Ordre des paramètres à extraire
fields_order = ['Date', 'tension1', 'tension2', 'tension3', 'courant1', 'courant2', 'courant3', 'temp', 'cosphi']
# Fonction pour extraire la valeur numérique
pattern = re.compile(r"('Date', 'tension1', 'tension2', 'tension3', 'courant1', 'courant2', 'courant3', 'temp', 'cosphi'):\s*([-\d\.]+)")
def extract_value(line):
    match = pattern.search(line)
    if match:
        key, value = match.groups()
        if key == "cosphi":
            key = "Cosphi"  # Normalisation du champ Cosphi
        return key, value
    return None, None
# Vérifier si le fichier de sortie existe et s'il contient déjà un en-tête
write_header = not os.path.exists(output_file) or os.stat(output_file).st_size == 0

# Lire l'index sauvegardé
if os.path.exists(index_file):
    with open(index_file, "r") as f:
        last_index = int(f.read().strip())
else:
    last_index = 0
data_rows = []
current_data = {key: "" for key in fields_order}
found_voltage1 = False
while True:
    with open(input_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()
    new_lines = lines[last_index:]
    last_index = len(lines)  # Mettre à jour l'index après lecture
    for line in new_lines:
        key, value = extract_value(line)
        if key == "Voltage1":
            found_voltage1 = True  # Détection de la première occurrence de Voltage1
        if found_voltage1 and key in current_data:
            current_data[key] = value
        if found_voltage1 and all(current_data[key] != "" for key in fields_order[1:]):  # Vérifie que toutes les valeurs (sauf Date) sont présentes
            current_data["Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Ajout de la date actuelle
            data_rows.append([current_data[field] for field in fields_order])
            current_data = {key: "" for key in fields_order}  # Réinitialisation
            found_voltage1 = False  # Réinitialisation pour la prochaine séquence complète
    # Écriture dans le fichier clean.csv
    if data_rows:
        with open(output_file, "a", newline="", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)
            if write_header:
                writer.writerow(fields_order)
                write_header = False  # Ne pas réécrire l'en-tête
            writer.writerows(data_rows)
        
        print(f"{len(data_rows)} nouvelles entrées ajoutées à {output_file}")
     
        data_rows = []
    # Sauvegarde de l'index traité
    with open(index_file, "w") as f:
        f.write(str(last_index))
    time.sleep(1)  # Pause avant de relire les nouvelles données