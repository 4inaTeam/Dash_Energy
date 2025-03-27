import pandas as pd
import csv
import datetime
import time
import os
import math
import numpy as np
################################# SAVE DATA TO CSV FIL ########################################
# Chemin vers le fichier CSV contenant les données de batch
# CSV_FILE_PATH = 'files_csv/data_courant_tension.csv'
CSV_FILE_PATH = 'files_csv/data_courant_tension.csv'
CSV_FILE_PATH_MIN = 'stockage_data/min_data.csv'
# En-têtes pour les données CSV
header = ['Date', 'courant1', 'courant2', 'courant3', 'tension1', 'tension2', 'tension3']
def write_to_csv(data):
    """
    Fonction pour écrire les données dans le fichier CSV principal.
    :param data: Liste de données à écrire dans le fichier CSV.
    """
    file_exists = os.path.isfile(CSV_FILE_PATH)
    with open(CSV_FILE_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)  # Écrire les en-têtes si le fichier est nouveau
        for entry in data:
            writer.writerow([
                entry.get('Date', ''),
                entry.get('courant1', ''),
                entry.get('courant2', ''),
                entry.get('courant3', ''),
                entry.get('tension1', ''),
                entry.get('tension2', ''),
                entry.get('tension3', '')
            ])
def write_to_csv1(data):
    """
    Fonction pour écrire les données dans un fichier CSV secondaire.
    :param data: Liste de données à écrire dans le fichier CSV.
    """
    file_exists = os.path.isfile(CSV_FILE_PATH_MIN)
    with open(CSV_FILE_PATH_MIN, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)  # Écrire les en-têtes si le fichier est nouveau
        for entry in data:
            writer.writerow([
                entry.get('Date', ''),
                entry.get('courant1', ''),
                entry.get('courant2', ''),
                entry.get('courant3', ''),
                entry.get('tension1', ''),
                entry.get('tension2', ''),
                entry.get('tension3', '')
            ])
#################### code updated pour factory ########################################
'''
# Chemin vers le fichier CSV contenant les données de batch
CSV_FILE_PATH = 'files_csv/data_courant_tension.csv'
CSV_FILE_PATH_MIN = 'stockage_data/min_data.csv'
# En-têtes pour les données CSV
header = ['Date', 'courant1', 'courant2', 'courant3', 
          'courant4', 'courant5', 'courant6', 
          'tension1', 'tension2', 'tension3',
          'tension4', 'tension5', 'tension6']

def write_to_csv(data):
    """
    Fonction pour écrire les données dans le fichier CSV principal.
    :param data: Liste de données à écrire dans le fichier CSV.
    """
    file_exists = os.path.isfile(CSV_FILE_PATH)
    with open(CSV_FILE_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)  # Écrire les en-têtes si le fichier est nouveau
        for entry in data:
            writer.writerow([
                entry.get('Date', ''),
                entry.get('courant1', ''),
                entry.get('courant2', ''),
                entry.get('courant3', ''),
                entry.get('courant4', ''),
                entry.get('courant5', ''),
                entry.get('courant6', ''),
                entry.get('tension1', ''),
                entry.get('tension2', ''),
                entry.get('tension4', ''),
                entry.get('tension5', ''),
                entry.get('tension6', '')
            ])

def write_to_csv1(data):
    """
    Fonction pour écrire les données dans un fichier CSV secondaire.
    :param data: Liste de données à écrire dans le fichier CSV.
    """
    file_exists = os.path.isfile(CSV_FILE_PATH_MIN)
    with open(CSV_FILE_PATH_MIN, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)  # Écrire les en-têtes si le fichier est nouveau
        for entry in data:
            writer.writerow([
                entry.get('Date', ''),
                entry.get('courant1', ''),
                entry.get('courant2', ''),
                entry.get('courant3', ''),
                entry.get('courant4', ''),
                entry.get('courant5', ''),
                entry.get('courant6', ''),
                entry.get('tension1', ''),
                entry.get('tension2', ''),
                entry.get('tension4', ''),
                entry.get('tension5', ''),
                entry.get('tension6', '')
            ])

'''