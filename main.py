from io import BytesIO
import tempfile
import threading
import os
import csv
from unittest import result
import schedule
from flask import Flask, Response, abort, jsonify, logging, request, send_file
from calcul_average import *
# from models import *
#from model_updated import *
from data_handling import *
from chatbot import ChatBotApp
from image_classification import *
from flask_cors import CORS
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials, storage, initialize_app, db
from geopy.geocoders import Nominatim
from power_calc import simulate_real_time_processing as smp   # import ca pour calul val eff avec cycles 
from energy_calc import simulate_real_time_processing_energy as ener
from calcul_val_eff import process_and_store_data
from notifications import monitor_csv_files, notifications
from remove_data import remove_csv_content
import functools
# Charger les informations d'identification Firebase
cred = credentials.Certificate("E:/4ina_Technologie/Backend_flask/credentials.json")

# Initialiser l'application Firebase avec le nom du bucket et l'URL de la base de données
firebase_app = firebase_admin.initialize_app(cred
                                             
                                             , {
    # 'storageBucket': 'dashboard-energy-7fae9.firebasestorage.app',  # Nom du bucket de stockage Firebase
    'databaseURL': 'https://dashboard-energy-7fae9-default-rtdb.europe-west1.firebasedatabase.app/'  # URL de la base de données Firebase
})
print('ok' ,firebase_app)
# Obtenir une instance du bucket de stockage Firebase
# bucket = storage.bucket()

app = Flask(__name__)
CORS(app)
# Configuration des autorisations CORS pour permettre l'accès depuis n'importe quelle origine
cors = CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST"]}})

# Instancier l'application ChatBot
chatbot_app = ChatBotApp()

############################# Fonction pour recevoir les données et les pousser dans Firebase Realtime ###########################
print("ref")

# Référence à la base de données Firebase Realtime Database pour stocker les données
ref = db.reference('/data', app=firebase_app)
#########################################################




@app.route('/receive_data', methods=['POST'])
def receive_data():
    """
    Endpoint pour recevoir des données JSON via une requête POST et les enregistrer dans les fichiers CSV.
    :return: Réponse JSON indiquant le succès ou l'échec de l'enregistrement des données.
    """
    data = request.json
    if isinstance(data, list):
        # Utiliser un thread pour écrire les données dans les fichiers CSV afin de ne pas bloquer le serveur
        def write_data():
            write_to_csv(data)
            write_to_csv1(data)      
        thread = threading.Thread(target=write_data)
        thread.start()
        thread.join()   
        return jsonify({'status': 'success', 'message': 'Données reçues et enregistrées'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Format de données invalide'}), 400


####################  receive / get Data ###################################
# Route pour récupérer les données du fichier CSV principal
@app.route('/get_csv_data', methods=['GET'])
def get_csv_data():
    """
    Endpoint pour récupérer les données du fichier CSV principal.
    :return: Données au format JSON ou message d'erreur en cas de problème.
    """
    try:
        with open("temporal_data/min_data.csv", 'r') as file:
        # with open("clean.csv", 'r') as file:
            csv_reader = csv.DictReader(file)
            data = list(csv_reader)  # Lire toutes les lignes du fichier CSV
            return jsonify(data)  # Retourner les données en format JSON
    except FileNotFoundError:
        return 'Fichier CSV non trouvé', 404  # Erreur si le fichier n'existe pas
    except Exception as e:
        return f'Erreur lors de la lecture du fichier CSV : {e}', 500  # Autres erreurs

# Chemin vers le fichier CSV contenant les données de batch temporaire
CSV_FILE_PATH_temp = 'files_csv/maps_temp_data.csv'
# Route pour récupérer les données du fichier CSV temporaire
@app.route('/get_csv_data_temp', methods=['GET'])
def get_csv_data_temp():
    """
    Endpoint pour récupérer les données du fichier CSV temporaire.
    :return: Données au format JSON ou message d'erreur en cas de problème.
    """
    try:
        with open(CSV_FILE_PATH_temp, 'r') as file:
            csv_reader = csv.DictReader(file)
            data = list(csv_reader)  # Lire toutes les lignes du fichier CSV
            return jsonify(data)  # Retourner les données en format JSON
    except FileNotFoundError:
        return 'Fichier CSV non trouvé', 404  # Erreur si le fichier n'existe pas
    except Exception as e:
        return f'Errrreur lors de la lecture du fichier CSV : {e}', 500  # Autres erreurs

######################################  get data for gauges  ###################################

# Chemin vers le fichier CSV contenant les données moyennes
AVERAGE_CSV_FILE_PATH = 'files_csv/data_average.csv'
VAL_EFF_DATA = 'stockage_data/data_efficace.csv'
energy_data = 'stockage_data/accumulated_energy_per_phase_1.csv'
# Route pour récupérer les données moyennes du fichier CSV
@app.route('/get_csv_data_moyenne', methods=['GET'])
def get_csv_data_moyenne():
    """
    Endpoint pour récupérer les données moyennes à partir du fichier CSV.
    :return: Données au format JSON ou message d'erreur en cas de problème.
    """
    try:
        with open(AVERAGE_CSV_FILE_PATH, 'r') as file:
            csv_reader = csv.DictReader(file)
            data = list(csv_reader)  # Lire toutes les lignes du fichier CSV
            return jsonify(data)  # Retourner les données en format JSON
    except FileNotFoundError:
        return 'Fichier CSV des données moyennes non trouvé', 404  # Erreur si le fichier n'existe pas
    except Exception as e:
        return f'Erreur lors de la lecture du fichier CSV des données moyennes : {e}', 500  # Autres erreurs
    
# Route pour récupérer les données efficaces du fichier CSV
@app.route('/get_csv_val_eff', methods=['GET'])
def get_csv_val_eff():
    """
    Endpoint pour récupérer les données efficaces à partir du fichier CSV.
    :return: Données au format JSON ou message d'erreur en cas de problème.
    """
    try:
        with open(VAL_EFF_DATA, 'r') as file:
            csv_reader = csv.DictReader(file)
            data = list(csv_reader)  # Lire toutes les lignes du fichier CSV
            return jsonify(data)  # Retourner les données en format JSON
    except FileNotFoundError:
        return 'Fichier CSV des données efficaces non trouvé', 404  # Erreur si le fichier n'existe pas
    except Exception as e:
        return f'Erreur lors de la lecture du fichier CSV des données efficaces : {e}', 500  # Autres erreurs
    
# Route pour récupérer les données d'énergie à partir du fichier CSV
@app.route('/get_energy', methods=['GET'])
def get_energy():
    """
    Endpoint pour récupérer les données d'énergie à partir du fichier CSV.
    :return: Données au format JSON ou message d'erreur en cas de problème.
    """
    try:
        with open(energy_data, 'r') as file:
            csv_reader = csv.DictReader(file)
            data = list(csv_reader)  # Lire toutes les lignes du fichier CSV
            return jsonify(data)  # Retourner les données en format JSON
    except FileNotFoundError:
        return 'Fichier CSV des données d\'énergie non trouvé', 404  # Erreur si le fichier n'existe pas
    except Exception as e:
        return f'Erreur lors de la lecture du fichier CSV des données d\'énergie : {e}', 500  # Autres erreurs

######################## post location get long/lat ##########################
# '''
@app.route('/get_coordinates', methods=['POST'])
def get_coordinates():
    """
    Endpoint pour obtenir les coordonnées géographiques (latitude et longitude) d'une localisation.
    :return: Coordonnées en format JSON ou message d'erreur en cas de problème.
    """
    try:
        # Récupérer le nom de la localisation à partir de la requête POST
        location_name = request.form.get('location')
        print("Location name:", location_name)

        # Utiliser Geopy pour obtenir les coordonnées de latitude et de longitude de la localisation
        geolocator = Nominatim(user_agent="GetLoc")
        location = geolocator.geocode(location_name)

        if location:
            latitude = location.latitude
            longitude = location.longitude
            print("Latitude:", latitude, "Longitude:", longitude)

            # Retourner les coordonnées de latitude et de longitude sous forme de réponse JSON
            return jsonify({'latitude': latitude, 'longitude': longitude}), 200
        else:
            # Retourner une erreur si la localisation n'a pas été trouvée
            print("Location not found")
            return jsonify({'error': 'Location not found'}), 404
    except Exception as e:
        # Retourner une erreur en cas d'exception
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

        # '''
######################################################## envoeir ordre ~#########################
# Dictionnaires pour stocker les dernières valeurs reçues et les temps des courants
# latest_received_values = {i: None for i in range(1, 10)}
# last_courant_over_time = {i: None for i in range(1, 10)}
# def monitor_csv_files():
#     global latest_received_values, last_courant_over_time
#     while True:
#         try:
#             Charger les dernières données des fichiers CSV
#             data = pd.read_csv('files_csv/data_courant_tension.csv').tail(1)  # Obtenir la dernière ligne
     
#             data_temp = pd.read_csv('files_csv/maps_temp_data.csv').tail(1)   # Obtenir la dernière ligne
            
#             for i in range(1, 4):
#                 Extraire les valeurs de courant, tension, et température
#                 courant = data[f'courant{i}'].values[0]
#                 tension = data[f'tension{i}'].values[0]
#                 temp = data_temp[f'temperature{i}'].values[0]
                
#                 Mettre à jour les dernières valeurs reçues
#                 latest_received_values[i] = {
#                     'courant': courant,
#                     'tension': tension,
#                     'temperature': temp,
#                     'message': None  # Initialiser le message à None
#                 }
                
#                 Vérifier les conditions pour les messages
#                 if courant > 5.34 or courant < -5.34:
#                     if tension > 280 or tension < -280 and temp > 40 or temp < 10:  # Valeurs seuil pour la tension et la température
#                         latest_received_values[i]['message'] = 'Value received successfully due to condition 1'
#                         last_courant_over_time[i] = None  # Réinitialiser le temporisateur
#                     else:
#                         if last_courant_over_time[i] is None:
#                             last_courant_over_time[i] = time.time()
#                         elif time.time() - last_courant_over_time[i] >= 10:
#                             latest_received_values[i]['message'] = 'Value received successfully due to condition 2'
#                             last_courant_over_time[i] = None
#                 else:
#                     last_courant_over_time[i] = None

#                 if tension > 0:
#                     latest_received_values[i]['message'] = 'Value received successfully due to condition 3'
#                 else:
#                     latest_received_values[i]['message'] = 'Value received successfully due to condition 4'
                
#                 if temp > 40 or temp < 10:
#                     latest_received_values[i]['message'] = 'Value received successfully due to condition 5'
#                 else:
#                     latest_received_values[i]['message'] = 'Value received successfully due to condition 6'
                    
#             time.sleep(1)  # Vérifier chaque seconde
#         except Exception as e:
#             print(f"Error readimmng CSV files: {e}")
#             time.sleep(1)  # Attendre en cas d'erreur
@app.route('/send_data_ordre', methods=['GET'])
def get_received_data():
    global latest_received_values
    # Créer un résultat binaire basé sur les valeurs reçues
    result = ''.join(str(0 if latest_received_values[i] else 1) for i in range(1, 10))
    return jsonify({'result': result, 'data': latest_received_values}), 200
'''
@app.route('/get_notifications', methods=['GET'])
def get_notifications():
    try:
        return jsonify({'notifications': notifications}), 200
    except Exception as e:
        print(f"Error in get_notifications: {e}")
        return jsonify({'error': str(e)}), 500
'''
@app.route('/get_notifications', methods=['GET'])
def get_notifications():
    try:
        return jsonify({'notifications': notifications}), 200
    except Exception as e:
       
        return jsonify({'error': str(e)}), 500

#################### page reporting #####################

@app.route('/list-files', methods=['GET'])
def list_files():
    # Lister les fichiers dans le bucket Firebase Storage
    blobs = bucket.list_blobs(prefix='excel_files/')
    file_names = [blob.name[len('excel_files/'):] for blob in blobs if not blob.name.endswith('/')]
    return jsonify(file_names)

@app.route('/download-file/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # Télécharger un fichier du bucket Firebase Storage
        blob = bucket.blob(f'excel_files/{filename}')
        if not blob.exists():
            print(f"File {filename} does not exist in Firebase Storage.")
            return abort(404, description="Resource not found")

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            blob.download_to_filename(temp_file.name)
            temp_file_path = temp_file.name
            print(f"File {filename} downloaded to temporary location {temp_file_path}")

        return send_file(temp_file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return abort(500, description=f"An error occurred: {str(e)}")

####################################save file to storage firebase ###################################

def upload_file(local_path, blob_name):
    try:
        # Télécharger un fichier local vers Firebase Storage
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(local_path, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        print(f'{os.path.basename(local_path)} uploaded successfully.')
    except Exception as e:
        print(f"Failed to upload {os.path.basename(local_path)}. Error: {e}")

def convert_csv_to_excel(csv_path, excel_path):
    try:
        # Lire le fichier CSV et le convertir en fichier Excel
        df = pd.read_csv(csv_path)
        df.to_excel(excel_path, index=False)
        print(f'Converted {os.path.basename(csv_path)} to {os.path.basename(excel_path)}.')
    except Exception as e:
        print(f"Failed to convert {os.path.basename(csv_path)} to Excel. Error: {e}")

def upload_files_to_firebase():
    try:
        local_folder = 'C:/Users/4InA Technologie-01/Desktop/final_codes_application/Backend_flask/stockage_data/'
        current_date = datetime.datetime.now().strftime('%d-%m-%Y')
        print(f"Current date for upload folder: {current_date}")

        if not os.path.exists(local_folder):
            print(f"Folder '{local_folder}' does not exist.")
            return

        for filename in os.listdir(local_folder):
            if filename.endswith('.csv'):
                csv_path = os.path.join(local_folder, filename)
                if not os.path.isfile(csv_path):
                    print(f"File '{csv_path}' does not exist.")
                    continue

                excel_filename = f'{os.path.splitext(filename)[0]}.xlsx'
                excel_path = os.path.join(local_folder, excel_filename)

                print(f"Preparing to convert and upload file: {csv_path}")

                # Convertir le fichier CSV en fichier Excel
                convert_csv_to_excel(csv_path, excel_path)

                # Créer un blob dans le dossier spécifique
                blob_name = f'excel_files/{excel_filename}'

                # Réessayer jusqu'à 3 fois en cas d'échec
                retries = 2
                for attempt in range(retries):
                    try:
                        upload_file(excel_path, blob_name)
                        break  # Sortir de la boucle si le téléchargement réussit
                    except Exception as e:
                        print(f"Attempt {attempt + 1} failed. Error: {e}")
                        time.sleep(5)  # Attendre avant de réessayer
                else:
                    print(f"Failed to upload {excel_filename} after {retries} attempts.")
    except Exception as e:
        print(f"Error uploading files to Firebase Storage: {e}")
# //////////////////
def convert_csv_to_json(csv_path):
    data = []
    with open(csv_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data

def upload_json_to_realtime_database(json_data, blob_name):
    try:
        ref = db.reference(blob_name)  # Référence à un nœud dans la base de données
        ref.set(json_data)  # Téléverser les données JSON
        print(f"Data uploaded to Realtime Database at {blob_name}")
    except Exception as e:
        print(f"Error uploading to Realtime Database: {e}")

# def upload_Minutes_file_to_firebase():
#     try:
#         local_folder = 'E:/4ina_Technologie/Backend_flask/Dates_data/'
#         current_date = datetime.datetime.now().strftime('%d-%m-%Y')
#         print(f"Current date for upload folder 2: {current_date}")

#         if not os.path.exists(local_folder):
#             print(f"Folder '{local_folder}' does not exist.")
#             return

#         for filename in os.listdir(local_folder):
#             if filename.endswith('.csv'):
#                 csv_path = os.path.join(local_folder, filename)
#                 if not os.path.isfile(csv_path):
#                     print(f"File '{csv_path}' does not exist.")
#                     continue

#                 excel_filename = f'{os.path.splitext(filename)[0]}.xlsx'
#                 excel_path = os.path.join(local_folder, excel_filename)

#                 print(f"Preparing to convert and upload file: {csv_path}")

#                 # Convertir le fichier CSV en fichier Excel
#                 convert_csv_to_excel(csv_path, excel_path)

#                 # Créer un blob dans le dossier spécifique
#                 blob_name = f'excel_files/{excel_filename}'

#                 # Réessayer jusqu'à 3 fois en cas d'échec
#                 retries = 2
#                 for attempt in range(retries):
#                     try:
#                         upload_file(excel_path, blob_name)
#                         break  # Sortir de la boucle si le téléchargement réussit
#                     except Exception as e:
#                         print(f"Attempt {attempt + 1} failed. Error: {e}")
#                         time.sleep(5)  # Attendre avant de réessayer
#                 else:
#                     print(f"Failed to upload {excel_filename} after {retries} attempts.")
#     except Exception as e:
#         print(f"Error uploading files to Firebase Storage: {e}")
def upload_Minutes_file_to_firebase():
    try:
         # Définir le chemin du dossier local contenant les fichiers CSV
        local_folder = 'E:/4ina_Technologie/Backend_flask/Dates_data/'
         # Obtenir la date actuelle au format "jj-mm-aaaa"
        current_date = datetime.datetime.now().strftime('%d-%m-%Y')
        print(f"Current date for upload folder: {current_date}")
  # Vérifier si le dossier existe
        if not os.path.exists(local_folder):
            print(f"Folder '{local_folder}' does not exist.")
            return # Quitter la fonction si le dossier n'existe pas
 # Parcourir tous les fichiers du dossier
        for filename in os.listdir(local_folder):
             # Vérifier si le fichier a une extension .csv
            if filename.endswith('.csv'):
                csv_path = os.path.join(local_folder, filename)
                 # Vérifier si le fichier existe bien
                if not os.path.isfile(csv_path):
                    print(f"File '{csv_path}' does not exist.")
                    continue # Passer au fichier suivant si celui-ci n'existe pas

                print(f"Preparing to convert and upload file: {csv_path}")

                # Convertir le fichier CSV en JSON
                json_data = convert_csv_to_json(csv_path)

                # Créer un chemin dans la base de données
                blob_name = f'excel_files/{os.path.splitext(filename)[0]}'

                # Téléverser les données JSON dans Realtime Database
                upload_json_to_realtime_database(json_data, blob_name)
    except Exception as e:
        print(f"Error uploading files to Realtime Database: {e}")
def upload_csv_to_realtime_database(local_file_path, db_path):
    try:
       
      
        with open(local_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            print('ok')
            data = [row for row in csv_reader]
           
        ref.set(data)
        print(f"CSV file '{local_file_path}' uploaded successfully to '{db_path}'.")
    except Exception as e:
        print(f"Error uploading CSV to Realtime Database: {e}")

# upload_csv_to_realtime_database('E:/4ina_Technologie/Backend_flask/Dates_data/hour_data_moy.csv', 'realtime_db_path')
def delete_data_from_firebase(data_path):
    try:
        ref = db.reference(data_path)
        ref.delete()
        print(f"Data at '{data_path}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting data from Firebase: {e}")

# delete_data_from_firebase('excel_files')
############################################### schedule tasks ##############################################################
# input_file ="temporal_data/min_data.csv"
header = ['Date','tension1','tension2','tension3','courant1','courant2','courant3','temp','cosphi']  # Assurez-vous que cet en-tête correspond à vos données

# def update_min() :
#      with open(input_file, 'w') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(header)
#                 print("File updated.")
     
def schedule_tasks():
    # Planifier les tâches
    # Use functools.partial to create a callable with arguments
    job_func = functools.partial(upload_csv_to_realtime_database, 'E:/4ina_Technologie/Backend_flask/Dates_data/sec_data_moy.csv', 'realtime_db_path')
    # job_func = functools.partial(upload_csv_to_realtime_database, 'E:/4ina_Technologie/Backend_flask/temporal_data/sec_data_moy.csv', 'realtime_db_path')
    schedule.every(10).seconds.do(job_func)
    schedule.every(1).minutes.do(calculate_minute_averages)
    # schedule.every(1).seconds.do(calculate_seconde_averages)
    # schedule.every(10).seconds.do(upload_csv_to_realtime_database('E:/4ina_Technologie/Backend_flask/Dates_data/hour_data_moy.csv', 'realtime_db_path'),calculate_minute_averages)
    schedule.every(1).hours.do(calculate_hour_averages)
    schedule.every().day.at("00:00").do(calculate_day_averages)

    # schedule.every(60).seconds.do(update_min)

    # Planifier la tâche de téléchargement de fichiers tous les 24 heures
    schedule.every(24).hours.do(upload_files_to_firebase)
    # schedule.every(1).minute.do(upload_Minutes_file_to_firebase)

    while True:
        schedule.run_pending()
        time.sleep(4)  # Attendre avant de vérifier à nouveau

def run_calculate_average():
    while True:
        # calculate_average()  # Calculer les moyennes
        # Fonction pour exécuter le calcul des moyennes à intervalles réguliers

        # calculate_minute_averages()
        # calculate_seconde_averages()
        #calculate_hour_averages()
        #calculate_day_averages()
        #calculate_week_averages()
        #calculate_month_averages()
        #calculate_year_averages()
        time.sleep(3)  # Attendre 20 secondes avant la prochaine exécution


def run_scheduler_v_eff():
    while True:
        process_and_store_data()  # Traiter et stocker les données
        time.sleep(1)  # Attendre 2 secondes avant la prochaine exécution


####################  Chatbot ###################################
# Définition de la route Flask pour le chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Vérifier si la clé 'message' est présente dans la requête JSON
    if 'message' not in request.json:
        return jsonify({'error': 'No message provided'}), 400

    # Extraire le message de la requête
    user_input = request.json['message']

    # Vérifier si le message est vide
    if not user_input:
        return jsonify({'error': 'Empty message provided'}), 400

    # Appeler la méthode predict_cause_and_solution pour traiter le message
    response = chatbot_app.predict_cause_and_solution(user_input)

    # Retourner la réponse au format JSON
    return jsonify({'response': response})

# ####################  Image ###################################
# Route pour la classification d'image
save_folder = "C:/Users/4InA Technologie-01/Flutter_projects/Backend_flask/images/"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)  # Créer le dossier de sauvegarde s'il n'existe pas

@app.route('/classify_image_mobile', methods=['POST'])
def classify_image_route_mobile():
    # Vérifier si l'image est présente dans la requête
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    # Sauvegarder l'image téléchargée
    image_file = request.files['image']
    image_path = save_folder + image_file.filename
    image_file.save(image_path)
    
    # Classifier l'image et obtenir les résultats
    label, confidence = classify_image_mobile(image_path)
    
    # Supprimer le fichier image temporaire
    os.remove(image_path)
    
    # Retourner les résultats au format JSON
    return jsonify({'label': label, 'confidence': confidence})

@app.route('/classify_image_web', methods=['POST'])
def classify_image_route_web():
    # Vérifier si l'image est présente dans la requête
    if 'image' not in request.form:
        return jsonify({'error': 'No image uploaded'}), 400

    # Extraire les données d'image base64 du corps de la requête
    image_data = request.form['image']

    # Classer l'image et obtenir les résultats
    label, confidence = classify_image_web(image_data)

    # Retourner les résultats au format JSON
    return jsonify({'label': label, 'confidence': confidence})

########################################### get long lat maps ################################################

# Définir les en-têtes pour les données de température
header_temp = ['Date', 'latitude', 'longitude', 'temperature1','temperature2','temperature3','temperature4','temperature5','temperature6']
CSV_FILE_PATH_map_temp = 'files_csv/maps_temp_data.csv'

@app.route('/update_location', methods=['GET'])
def update_location():
    # Récupérer la latitude, longitude et les températures des paramètres de la requête
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    temp1 = request.args.get('temp1')
    temp2 = request.args.get('temp2')
    temp3 = request.args.get('temp3')
    temp4 = request.args.get('temp4')
    temp5 = request.args.get('temp5')
    temp6 = request.args.get('temp6')
    
    # Afficher les données de localisation reçues
    print("Received location data - Latitude:", lat, "Longitude:", lng)

    # Écrire les données dans un fichier CSV
    with open(CSV_FILE_PATH_map_temp, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Écrire l'en-tête si le fichier est vide
        if os.stat(CSV_FILE_PATH_map_temp).st_size == 0:
            writer.writerow(header_temp)
        # Formater la date et l'heure actuelle
        formatted_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        # Écrire les données dans le fichier CSV
        writer.writerow([formatted_now, lat, lng, temp1, temp2, temp3, temp4, temp5, temp6])

    # Renvoyer uniquement les coordonnées de latitude et de longitude au format JSON
    return jsonify({"latitude": lat, "longitude": lng})

'''
# Route pour renvoyer les dernières coordonnées enregistrées sous forme de JSON
@app.route('/get_last_location', methods=['GET'])
def get_last_location():
    # Lire le fichier CSV et récupérer la dernière ligne
    with open(CSV_FILE_PATH_map_temp, mode='r') as file:
        csv_reader = csv.reader(file)
        last_row = None
        for row in csv_reader:
            last_row = row
        if last_row:
            # Si la dernière ligne existe, extraire la longitude et la latitude des colonnes appropriées
            longitude = last_row[1]  # Index 1 pour la longitude
            latitude = last_row[2]   # Index 2 pour la latitude
            return jsonify({"latitude": latitude, "longitude": longitude})
        else:
            # Si le fichier est vide ou s'il n'y a pas de données, renvoyer None
            return jsonify({"latitude": None, "longitude": None})
'''
############################################ envoeir notification #####################################################






if __name__ == '__main__':
    

    # Démarrer le thread pour obtenir les données CSV
    #thread_get_data_csv = threading.Thread(target=receive_data)
    #thread_get_data_csv.start()
    
    # Démarrer le thread pour obtenir les données CSV
    #thread_get_data_csv = threading.Thread(target=get_csv_data)
    #thread_get_data_csv.start()

    # Démarrer le thread pour obtenir les données de température
    #thread_get_data_temp = threading.Thread(target=get_csv_data_temp)
    #thread_get_data_temp.start()
    #thread_get_data = threading.Thread(target=get_database_data)
    #thread_get_data.start()
    # Démarrer la prédiction de la tension
    #############
    # thread_prediction_tension = threading.Thread(target=predict_courant_tension_2)
    # thread_prediction_tension.start()
#############
    # Démarrer la prédiction de la température
    #thread_prediction_temp = threading.Thread(target=predict_temp_1)
    #thread_prediction_temp.start()

    # Démarrer le thread pour supprimer le contenu de data.csv périodiquement
#############

    # thread_remove_csv_content = threading.Thread(target=remove_csv_content)
    # thread_remove_csv_content.start()
#############

    # Démarrer le thread pour supprimer le contenu de data.csv après 10 secondes
    #thread_remove_csv_content_10 = threading.Thread(target=remove_csv_content_10)
    #thread_remove_csv_content_10.start()

    # Démarrer le thread pour calculer la moyenne
    thread_calculate_average = threading.Thread(target=run_calculate_average)
    thread_calculate_average.start()

    scheduler_thread = threading.Thread(target=run_scheduler_v_eff)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    thread_run_scheduler_upload = threading.Thread(target=schedule_tasks)
    thread_run_scheduler_upload.start()

    # Démarrer le thread pour surveiller les fichiers CSV
    thread_monitor_csv = threading.Thread(target=monitor_csv_files)
    thread_monitor_csv.daemon = True  # Définir en tant que daemon si nécessaire
    thread_monitor_csv.start()
    # Attendre que tous les threads se terminent (pas nécessaire pour les threads daemon)
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)

