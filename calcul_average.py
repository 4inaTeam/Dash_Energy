import pandas as pd
import os
import csv
from data_handling import CSV_FILE_PATH_MIN, header

###########################################################
# Fonction pour calculer les moyennes des températures
###########################################################
# def calculate_average():
#     try:
#         # Lire le fichier CSV contenant les données de température
#         data_temp = pd.read_csv('files_csv/maps_temp_data.csv')
        
#         # Calculer la moyenne des colonnes de température
#         averages = {
#             'Average_temp_int1': abs(data_temp['temperature1'].mean()),
#             'Average_temp_int2': abs(data_temp['temperature2'].mean()),
#             'Average_temp_int3': abs(data_temp['temperature3'].mean())
#         }
        
#         # Créer un DataFrame pour stocker les moyennes
#         average_data = pd.DataFrame(averages, index=[0])
        
#         # Écrire les moyennes calculées dans un fichier CSV
#         if not os.path.exists('files_csv/data_average.csv'):
#             average_data.to_csv('files_csv/data_average.csv', index=False)
#         else:
#             average_data.to_csv('files_csv/data_average.csv', mode='a', header=False, index=False)
            
#     except Exception as e:
#         print(f"An error occurred during average calculation: {e}")

# Chemins des fichiers CSV
CSV_FILE_PATH_MIN = 'stockage_data/min_data.csv'
# CSV_FILE_PATH_MIN = 'clean.csv'
sec_data_moy_path = 'Dates_data/sec_data_moy.csv'
sec_data_moy_path_temp = 'temporal_data/sec_data_moy.csv'
min_data_moy_path = 'Dates_data/min_data_moy.csv'
min_data_moy_path_temp = 'temporal_data/min_data_moy.csv'
hour_data_moy_path = 'Dates_data/hour_data_moy.csv'
hour_data_moy_path_temp = 'temporal_data/hour_data_moy.csv'
day_data_moy_path = 'Dates_data/day_data_moy.csv'
day_data_moy_path_temp = 'temporal_data/day_data_moy.csv'
week_data_moy_path = 'Dates_data/week_data_moy.csv'
week_data_moy_path_temp = 'temporal_data/week_data_moy.csv'
month_data_moy_path = 'Dates_data/month_data_moy.csv'
month_data_moy_path_temp = 'temporal_data/month_data_moy.csv'
year_data_moy_path = 'Dates_data/year_data_moy.csv'
year_data_moy_path_temp = 'temporal_data/year_data_moy.csv'
CSV_FILE_PATH_TEMP = 'temporal_data/min_data.csv'
# Référence à la base de données Firebase Realtime Database pour stocker les données

header = ['Date','tension1','tension2','tension3','courant1','courant2','courant3','temp','cosphi']  # Assurez-vous que cet en-tête correspond à vos données
# def calculate_seconde_averages():

#     try:
#         if os.path.exists(CSV_FILE_PATH_TEMP):
#             data = pd.read_csv(CSV_FILE_PATH_TEMP)
#             if data.empty :
#                 print("Le fichier est vide2.")
#                 return
#             if  len(data) < 4:
#                 print("Le fichier ne contient pas suffisamment de données.")
#                 return
            
#             data['Date'] = pd.to_datetime(data['Date'])
#             data.set_index('Date', inplace=True)
#             seconde_averages = data.resample('1s').mean()
       
#             if not os.path.exists(sec_data_moy_path):
#                 seconde_averages.to_csv(sec_data_moy_path)
#             else:
#                 seconde_averages.to_csv(sec_data_moy_path, mode='a', header=False)
#             if not os.path.exists(sec_data_moy_path_temp):
#                 seconde_averages.to_csv(sec_data_moy_path_temp)
#             else:
#                 seconde_averages.to_csv(sec_data_moy_path_temp, mode='a', header=False)
#             # with open(CSV_FILE_PATH_TEMP, 'w') as file:
#             #     writer = csv.writer(file)
#             #     writer.writerow(header)
#             print("Moyennes calculées et sauvegardées. Données originales supprimées.")
#         else:
#             print(f"Le fichier {CSV_FILE_PATH_TEMP} n'existe pas.")
#     except Exception as e:
#         print(f"An error occurred during the calculation of seconde averages: {e}")



# def calculate_seconde_averages():
#     try:
#         if os.path.exists(CSV_FILE_PATH_MIN):
#             data = pd.read_csv(CSV_FILE_PATH_MIN)

#             if data.empty:
#                 print("Le fichier est vide.")
#                 return

#             if len(data) < 4:
#                 print("Le fichier ne contient pas suffisamment de données.")
#                 return

#             # Supprimer les lignes où toutes les valeurs sont NaN sauf la colonne "Date"
#             data = data.dropna(how='all', subset=['tension1', 'tension2', 'tension3', 'courant1', 'courant2', 'courant3', 'temp', 'cosphi'])

#             print('Début de la sauvegarde Excel')

#             # Vérifier si le fichier Excel existe
#             if not os.path.exists(Backup_data_file):
#                 print('Création du fichier Excel...')
#                 data.to_excel(Backup_data_file, index=False, engine='openpyxl')
#                 print("Le fichier Excel a été créé.")
#             else:
#                 # Charger le fichier Excel existant
#                 existing_data = pd.read_excel(Backup_data_file, sheet_name='Sheet1')

#                 # Fusionner les nouvelles données avec les existantes
#                 updated_data = pd.concat([existing_data, data], ignore_index=True)

#             #     # Réécriture du fichier Excel avec les nouvelles données
#             #     with pd.ExcelWriter(Backup_data_file, engine='openpyxl') as writer:
#             #         updated_data.to_excel(writer, index=False, sheet_name='Sheet1')

#             #     # Vérification de la dernière ligne
#             #     wb = openpyxl.load_workbook(Backup_data_file)
#             #     sheet = wb.active
#             #     derniere_ligne = sheet.max_row
#             #     print(f"derniere_ligne : {derniere_ligne}")
#             #   # Obtenir la dernière ligne sous forme de liste
#             #     last_row = [cell.value for cell in sheet[derniere_ligne]]

#             #     # Afficher la dernière ligne
#             #     print(f"Dernière ligne (numéro {derniere_ligne}) : {last_row}")
#             #     print("Les nouvelles données ont été ajoutées à la feuille existante.")

#             # Conversion de la colonne "Date" en format datetime
#             data['Date'] = pd.to_datetime(data['Date'])
#             data.set_index('Date', inplace=True)

#             # Calcul des moyennes par seconde
#             seconde_averages = data.resample('1s').mean()

#             # Sauvegarde dans un fichier CSV
#             if not os.path.exists(sec_data_moy_path):
#                 seconde_averages.to_csv(sec_data_moy_path)
#             else:
#                 seconde_averages.to_csv(sec_data_moy_path, mode='a', header=False)

#             # Suppression des données du fichier CSV d'origine après la sauvegarde
#             with open(CSV_FILE_PATH_MIN, 'w', newline='') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(header)  # Réécrire uniquement l'en-tête

#             print("Moyennes calculées et sauvegardées. Données originales supprimées.")

#         else:
#             print(f"Le fichier {CSV_FILE_PATH_MIN} n'existe pas.")

#     except Exception as e:
#         print(f"Une erreur est survenue lors du calcul des moyennes secondes : {e}")


# Fonction pour calculer les moyennes par minute

# def upload_csv_to_realtime_database(local_file_path, db_path):
#     try:
#         with open(local_file_path, mode='r', encoding='utf-8') as file:
#             csv_reader = csv.DictReader(file)
#             print('ok')
#             data = [row for row in csv_reader]          
#         ref.set(data)
#         print(f"CSV file '{local_file_path}' uploaded successfully to '{db_path}'.")
#     except Exception as e:
#         print(f"Error uploading CSV to Realtime Database: {e}")


# Assuming ref is initialized with the Firebase database reference


# def upload_csv_to_realtime_database(local_file_path, db_path):
#     try:
       
      
#         with open(local_file_path, mode='r', encoding='utf-8') as file:
#             csv_reader = csv.DictReader(file)
#             print('ok')
#             data = [row for row in csv_reader]
           
#         ref.set(data)
#         print(f"CSV file '{local_file_path}' uploaded successfully to '{db_path}'.")
#     except Exception as e:
#         print(f"Error uploading CSV to Realtime Database: {e}")

def calculate_minute_averages():

    try:
        if os.path.exists(sec_data_moy_path_temp):
            data = pd.read_csv(sec_data_moy_path_temp)
            if data.empty :
                print("Le fichier est vide3.")
                return
            if  len(data) < 4:
                print("Le fichier ne contient pas suffisamment de données.")
                return
                    
           
            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)
            minute_averages = data.resample('1min').mean()
        
            if not os.path.exists(min_data_moy_path):
                minute_averages.to_csv(min_data_moy_path)
            else:
                minute_averages.to_csv(min_data_moy_path, mode='a', header=False)
            if not os.path.exists(min_data_moy_path_temp):
                minute_averages.to_csv(min_data_moy_path_temp)
            else:
                minute_averages.to_csv(min_data_moy_path_temp, mode='a', header=False)
            try :
                # upload_csv_to_realtime_database('E:/4ina_Technologie/Backend_flask/Dates_data/hour_data_moy.csv', 'realtime_db_path')
                with open(sec_data_moy_path_temp, 'w') as file:
                 writer = csv.writer(file)
                 writer.writerow(header)
            except:
                print(f"An error occurred during the calculation of minute averages: {e}")
               
            print("Moyennes sec calculées et sauvegardées. Données sec originales supprimées.")
        else:
            print(f"Le fichier {CSV_FILE_PATH_MIN} n'existe pas.")
    except Exception as e:
        print(f"An error occurred during the calculation of minute averages: {e}")
# calculate_minute_averages()
# Fonction pour calculer les moyennes par heure
def calculate_hour_averages():
    try:
        if os.path.exists(min_data_moy_path_temp):
            data = pd.read_csv(min_data_moy_path_temp)
            if data.empty or len(data) < 4:
                print("Le fichier est vide ou ne contient pas suffisamment de données.")
                return
            data['Date'] = pd.to_datetime(data['Date'])
            print('hi1')
            data.set_index('Date', inplace=True)
            print('hi2')
            numeric_columns = data.select_dtypes(include='number').columns
#             print(f'Numeric columns: {numeric_columns}')
            hour_averages = data[numeric_columns].resample('1h').mean()
#             hour_averages = data.resample('1min').mean()
            print('hi3')
            if not os.path.exists(hour_data_moy_path):
                hour_averages.to_csv(hour_data_moy_path)
            else:
                hour_averages.to_csv(hour_data_moy_path, mode='a', header=False)
            if not os.path.exists(hour_data_moy_path_temp):
                hour_averages.to_csv(hour_data_moy_path_temp)
            else:
                hour_averages.to_csv(hour_data_moy_path_temp, mode='a', header=False)
            with open(min_data_moy_path_temp, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(header)
            print("Moyennes min calculées et sauvegardées. ")
        else:
            print(f"Le fichier {min_data_moy_path_temp} n'existe pas.")
    except Exception as e:
        print(f"An error occurred during the calculation of hour averages: {e}")
# def calculate_hour_averages():
#     try:
#         if os.path.exists(min_data_moy_path):
#             # Read the CSV data
#             data = pd.read_csv(min_data_moy_path)
            
#             # Check if the data is empty or has less than 4 rows
#             if data.empty or len(data) < 4:
#                 print("Le fichier est vide ou ne contient pas suffisamment de données.")
#                 return

#             # Convert the 'Date' column to datetime format
#             data['Date'] = pd.to_datetime(data['Date'])
            

#             # Set 'Date' as the index of the DataFrame
#             data.set_index('Date', inplace=True)
           

#             # Select only the numeric columns for resampling
#             numeric_columns = data.select_dtypes(include='number').columns
#             print(f'Numeric columns: {numeric_columns}')

#             # Perform resampling and calculate the mean for numeric columns
#             hour_averages = data[numeric_columns].resample('1h').mean()
            

#             # Save the hourly averages to the file
#             if not os.path.exists(hour_data_moy_path):
#                 hour_averages.to_csv(hour_data_moy_path)  # Write with header if file doesn't exist
#             else:
#                 hour_averages.to_csv(hour_data_moy_path, mode='a', header=False)  # Append without header

#             with open(min_data_moy_path, 'w') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(header)

#             print("Moyennes horaires calculées et sauvegardées.")
        
#         else:
#             print(f"Le fichier {min_data_moy_path} n'existe pas.")
    
#     except Exception as e:
#         print(f"An error occurred during the calculation of hour averages: {e}")

# calculate_hour_averages()
# Fonction pour calculer les moyennes par jour
def calculate_day_averages():
    try:
        if os.path.exists(hour_data_moy_path_temp):
            data = pd.read_csv(hour_data_moy_path_temp)
            if data.empty or len(data) < 4:
                print("Le fichier est vide ou ne contient pas suffisamment de données.")
                return
            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)
            day_averages = data.resample('D').mean()

            if not os.path.exists(day_data_moy_path):
                day_averages.to_csv(day_data_moy_path)
            else:
                day_averages.to_csv(day_data_moy_path, mode='a', header=False)
            if not os.path.exists(day_data_moy_path_temp):
                day_averages.to_csv(day_data_moy_path_temp)
            else:
                day_averages.to_csv(day_data_moy_path_temp, mode='a', header=False)
            with open(hour_data_moy_path_temp, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(header)
            print("Moyennes calculées et sauvegardées. Données originales supprimées.")
        else:
            print(f"Le fichier {hour_data_moy_path_temp} n'existe pas.")
    except Exception as e:
        print(f"An error occurred during the calculation of day averages: {e}")
# Fonction pour calculer les moyennes par semaine
def calculate_week_averages():
    try:
        if os.path.exists(day_data_moy_path_temp):
            data = pd.read_csv(day_data_moy_path_temp)
            if data.empty :
                print("Le fichier est vide4.")
                return
            if len(data) < 4:
                print("Le fichier ne contient pas suffisamment de données.")
                return

            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)
            week_averages = data.resample('W').mean()

            if not os.path.exists(week_data_moy_path):
                week_averages.to_csv(week_data_moy_path)
            else:
                week_averages.to_csv(week_data_moy_path, mode='a', header=False)
            if not os.path.exists(week_data_moy_path_temp):
                week_averages.to_csv(week_data_moy_path_temp)
            else:
                week_averages.to_csv(week_data_moy_path_temp, mode='a', header=False)

            with open(day_data_moy_path_temp, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(header)

            print("Moyennes calculées et sauvegardées. Données originales supprimées.")
        else:
            print(f"Le fichier {day_data_moy_path_temp} n'existe pas.")
    except Exception as e:
        print(f"An error occurred during the calculation of week averages: {e}")

# Fonction pour calculer les moyennes par mois
def calculate_month_averages():
    try:
        if os.path.exists(week_data_moy_path_temp):
            data = pd.read_csv(week_data_moy_path_temp)
            if data.empty or len(data) < 4:
                print("Le fichier est vide ou ne contient pas suffisamment de données.")
                return

            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)
            month_averages = data.resample('M').mean()

            if not os.path.exists(month_data_moy_path):
                month_averages.to_csv(month_data_moy_path)
            else:
                month_averages.to_csv(month_data_moy_path, mode='a', header=False)
            if not os.path.exists(month_data_moy_path_temp):
                month_averages.to_csv(month_data_moy_path_temp)
            else:
                month_averages.to_csv(month_data_moy_path_temp, mode='a', header=False)
            with open(week_data_moy_path_temp, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(header)

            print("Moyennes calculées et sauvegardées. Données originales supprimées.")
        else:
            print(f"Le fichier {week_data_moy_path_temp} n'existe pas.")
    except Exception as e:
        print(f"An error occurred during the calculation of month averages: {e}")

# Fonction pour calculer les moyennes par année
def calculate_year_averages():
    try:
        if os.path.exists(month_data_moy_path_temp):
            data = pd.read_csv(month_data_moy_path_temp)
            if data.empty or len(data) < 4:
                print("Le fichier est vide ou ne contient pas suffisamment de données.")
                return

            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)
            year_averages = data.resample('Y').mean()

            if not os.path.exists(year_data_moy_path):
                year_averages.to_csv(year_data_moy_path)
            else:
                year_averages.to_csv(year_data_moy_path, mode='a', header=False)
            if not os.path.exists(year_data_moy_path_temp):
                year_averages.to_csv(year_data_moy_path_temp)
            else:
                year_averages.to_csv(year_data_moy_path_temp, mode='a', header=False)

            with open(month_data_moy_path_temp, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(header)

            print("Moyennes calculées et sauvegardées. Données originales supprimées.")
        else:
            print(f"Le fichier {month_data_moy_path_temp} n'existe pas.")
    except Exception as e:
        print(f"An error occurred during the calculation of year averages: {e}")




'''
###########################################################
# Fonction pour calculer les moyennes par minute
###########################################################
min_data_moy_path = 'Dates_data/min_data_moy.csv'

def calculate_minute_averages():
    try:
        if os.path.exists(CSV_FILE_PATH_MIN):
            # Lire les données depuis le fichier CSV
            data = pd.read_csv(CSV_FILE_PATH_MIN)
            
            # Vérifier si le fichier contient suffisamment de données
            if data.empty or len(data) < 4:
                print("Le fichier est vide ou ne contient pas suffisamment de données.")
                return

            # Convertir la colonne 'Date' en datetime
            data['Date'] = pd.to_datetime(data['Date'])

            # Grouper les données par minute et calculer les moyennes
            data.set_index('Date', inplace=True)
            minute_averages = data.resample('T').mean()

            # Ajouter les moyennes calculées dans le fichier min_data_moy.csv
            if not os.path.exists(min_data_moy_path):
                minute_averages.to_csv(min_data_moy_path)
            else:
                minute_averages.to_csv(min_data_moy_path, mode='a', header=False)

            # Vider le fichier min_data.csv après le calcul
            with open(CSV_FILE_PATH_MIN, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(header)

            print("Moyennes calculées et sauvegardées. Données originales supprimées.")
        else:
            print(f"Le fichier {CSV_FILE_PATH_MIN} n'existe pas.")
    except Exception as e:
        print(f"An error occurred during the calculation of minute averages: {e}")

###########################################################
# Fonction pour calculer les moyennes par heure
###########################################################
hour_data_moy_path = 'Dates_data/hour_data_moy.csv'

def calculate_hour_averages():
    try:
        if os.path.exists(min_data_moy_path):
            # Lire les données depuis le fichier min_data_moy.csv
            data = pd.read_csv(min_data_moy_path)
            
            # Vérifier si le fichier contient suffisamment de données
            if data.empty or len(data) < 4:
                print("Le fichier est vide ou ne contient pas suffisamment de données.")
                return

            # Convertir la colonne 'Date' en datetime
            data['Date'] = pd.to_datetime(data['Date'])

            # Grouper les données par heure et calculer les moyennes
            data.set_index('Date', inplace=True)
            hour_averages = data.resample('H').mean()

            # Ajouter les moyennes calculées dans le fichier hour_data_moy.csv
            if not os.path.exists(hour_data_moy_path):
                hour_averages.to_csv(hour_data_moy_path)
            else:
                hour_averages.to_csv(hour_data_moy_path, mode='a', header=False)

            # Vider le fichier min_data_moy.csv après le calcul
            with open(min_data_moy_path, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(header)

            print("Moyennes calculées et sauvegardées. Données originales supprimées.")
        else:
            print(f"Le fichier {min_data_moy_path} n'existe pas.")
    except Exception as e:
        print(f"An error occurred during the calculation of hour averages: {e}")

###########################################################
# Fonction pour calculer les moyennes par jour
###########################################################
Day_data_moy_path = 'Dates_data/Day_data_moy.csv'

def calculate_day_averages():
    try:
        if os.path.exists(hour_data_moy_path):
            # Lire les données depuis le fichier hour_data_moy.csv
            data = pd.read_csv(hour_data_moy_path)
            
            # Vérifier si le fichier contient suffisamment de données
            if data.empty or len(data) < 4:
                print("Le fichier est vide ou ne contient pas suffisamment de données.")
                return

            # Convertir la colonne 'Date' en datetime
            data['Date'] = pd.to_datetime(data['Date'])

            # Grouper les données par jour et calculer les moyennes
            data.set_index('Date', inplace=True)
            day_averages = data.resample('D').mean()

            # Ajouter les moyennes calculées dans le fichier Day_data_moy.csv
            if not os.path.exists(Day_data_moy_path):
                day_averages.to_csv(Day_data_moy_path)
            else:
                day_averages.to_csv(Day_data_moy_path, mode='a', header=False)

            # Vider le fichier hour_data_moy.csv après le calcul
            with open(hour_data_moy_path, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(header)

            print("Moyennes calculées et sauvegardées. Données originales supprimées.")
        else:
            print(f"Le fichier {hour_data_moy_path} n'existe pas.")
    except Exception as e:
        print(f"An error occurred during the calculation of day averages: {e}")


# Fonction pour calculer les moyennes par week
###########################################################
week_data_moy_path = 'Dates_data/week_data_moy.csv'

def calculate_day_averages():
    try:
        if os.path.exists(Day_data_moy_path):
            # Lire les données depuis le fichier hour_data_moy.csv
            data = pd.read_csv(Day_data_moy_path)
            
            # Vérifier si le fichier contient suffisamment de données
            if data.empty or len(data) < 4:
                print("Le fichier est vide ou ne contient pas suffisamment de données.")
                return

            # Convertir la colonne 'Date' en datetime
            data['Date'] = pd.to_datetime(data['Date'])

            # Grouper les données par jour et calculer les moyennes
            data.set_index('Date', inplace=True)
            day_averages = data.resample('w').mean()

            # Ajouter les moyennes calculées dans le fichier Day_data_moy.csv
            if not os.path.exists(week_data_moy_path):
                day_averages.to_csv(week_data_moy_path)
            else:
                day_averages.to_csv(week_data_moy_path, mode='a', header=False)

            # Vider le fichier hour_data_moy.csv après le calcul
            with open(Day_data_moy_path, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(header)

            print("Moyennes calculées et sauvegardées. Données originales supprimées.")
        else:
            print(f"Le fichier {Day_data_moy_path} n'existe pas.")
    except Exception as e:
        print(f"An error occurred during the calculation of day averages: {e}")


# Fonction pour calculer les moyennes par month
###########################################################
month_data_moy_path = 'Dates_data/month_data_moy.csv'

def calculate_day_averages():
    try:
        if os.path.exists(Day_data_moy_path):
            # Lire les données depuis le fichier hour_data_moy.csv
            data = pd.read_csv(Day_data_moy_path)
            
            # Vérifier si le fichier contient suffisamment de données
            if data.empty or len(data) < 4:
                print("Le fichier est vide ou ne contient pas suffisamment de données.")
                return

            # Convertir la colonne 'Date' en datetime
            data['Date'] = pd.to_datetime(data['Date'])

            # Grouper les données par mois et calculer les moyennes
            data.set_index('Date', inplace=True)
            day_averages = data.resample('M').mean()

            # Ajouter les moyennes calculées dans le fichier Day_data_moy.csv
            if not os.path.exists(month_data_moy_path):
                day_averages.to_csv(month_data_moy_path)
            else:
                day_averages.to_csv(month_data_moy_path, mode='a', header=False)

            # Vider le fichier day_data_moy.csv après le calcul
            with open(Day_data_moy_path, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(header)

            print("Moyennes calculées et sauvegardées. Données originales supprimées.")
        else:
            print(f"Le fichier {Day_data_moy_path} n'existe pas.")
    except Exception as e:
        print(f"An error occurred during the calculation of day averages: {e}")


# Fonction pour calculer les moyennes par year
###########################################################
year_data_moy_path = 'Dates_data/year_data_moy.csv'

def calculate_day_averages():
    try:
        if os.path.exists(month_data_moy_path):
            # Lire les données depuis le fichier hour_data_moy.csv
            data = pd.read_csv(month_data_moy_path)
            
            # Vérifier si le fichier contient suffisamment de données
            if data.empty or len(data) < 4:
                print("Le fichier est vide ou ne contient pas suffisamment de données.")
                return

            # Convertir la colonne 'Date' en datetime
            data['Date'] = pd.to_datetime(data['Date'])

            # Grouper les données par year et calculer les moyennes
            data.set_index('Date', inplace=True)
            day_averages = data.resample('y').mean()

            # Ajouter les moyennes calculées dans le fichier Day_data_moy.csv
            if not os.path.exists(year_data_moy_path):
                day_averages.to_csv(year_data_moy_path)
            else:
                day_averages.to_csv(year_data_moy_path, mode='a', header=False)

            # Vider le fichier month_data_moy.csv après le calcul
            with open(month_data_moy_path, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(header)

            print("Moyennes calculées et sauvegardées. Données originales supprimées.")
        else:
            print(f"Le fichier {month_data_moy_path} n'existe pas.")
    except Exception as e:
        print(f"An error occurred during the calculation of day averages: {e}")
'''