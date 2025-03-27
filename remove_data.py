import os
import time

from data_handling import CSV_FILE_PATH

##############################
# Fonction pour supprimer les 400 premières lignes du fichier CSV périodiquement
##############################
def remove_csv_content():
    while True:
        try:
            # Vérifier si le fichier CSV existe
            if os.path.exists(CSV_FILE_PATH):
                # Lire toutes les lignes du fichier CSV
                with open(CSV_FILE_PATH, 'r') as file:
                    lines = file.readlines()
                
                # Si le fichier contient plus de 801 lignes (header + 800 données)
                if len(lines) > 801:
                    # Réécrire le fichier en supprimant les 400 premières lignes
                    with open(CSV_FILE_PATH, 'w') as file:
                        # Conserver la première ligne (header)
                        file.write(lines[0])
                        # Écrire les lignes à partir de la 401e ligne jusqu'à la fin
                        file.writelines(lines[801:])
                        print("400 premières lignes de data.csv ont été supprimées.")
        except Exception as e:
            # Capturer et afficher les erreurs potentielles
            print(f"An error occurred while removing first 400 lines of data.csv: {e}")
        
        # Attendre 1 seconde avant de répéter la suppression
        time.sleep(1)  # Ajuster l'intervalle selon les besoins

##############################
# Fonction pour supprimer les 600 premières lignes du fichier CSV périodiquement (commentée)
##############################
'''
def remove_csv_content():
    while True:
        try:
            # Vérifier si le fichier CSV existe
            if os.path.exists(CSV_FILE_PATH):
                # Lire toutes les lignes du fichier CSV
                with open(CSV_FILE_PATH, 'r') as file:
                    lines = file.readlines()
                
                # Réécrire le fichier en supprimant les 600 premières lignes
                with open(CSV_FILE_PATH, 'w') as file:
                    # Conserver la première ligne (header)
                    file.write(lines[0])
                    # Écrire les lignes à partir de la 601e ligne jusqu'à la fin
                    file.writelines(lines[400:])
                    print("300 premières lignes de data.csv ont été supprimées.")
        except Exception as e:
            # Capturer et afficher les erreurs potentielles
            print(f"An error occurred while removing first 600 lines of data.csv: {e}")
        
        # Attendre 2 secondes avant de répéter la suppression
        time.sleep(2)  # Ajuster l'intervalle selon les besoins


CSV_FILE_PATH_10 = 'data_predites.csv'

##############################
# Fonction pour supprimer les 1000 premières lignes du fichier CSV périodiquement
##############################
def remove_csv_content_10():
    while True:
        try:
            # Vérifier si le fichier CSV existe
            if os.path.exists(CSV_FILE_PATH_10):
                # Lire toutes les lignes du fichier CSV
                with open(CSV_FILE_PATH_10, 'r') as file:
                    lines = file.readlines()
                
                # Réécrire le fichier en supprimant les 1000 premières lignes
                with open(CSV_FILE_PATH_10, 'w') as file:
                    # Conserver la première ligne (header)
                    file.write(lines[0])
                    # Écrire les lignes à partir de la 1001e ligne jusqu'à la fin
                    file.writelines(lines[1000:])
                    print("1000 premières lignes de data_predites.csv ont été supprimées.")
        except Exception as e:
            # Capturer et afficher les erreurs potentielles
            print(f"An error occurred while removing first 1000 lines of data_predites.csv: {e}")
        
        # Attendre 60 secondes avant de répéter la suppression
        time.sleep(60)  # Ajuster l'intervalle selon les besoins
'''