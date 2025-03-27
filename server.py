# import http.server
# import socketserver
# import pandas as pd
# import time
# from datetime import datetime
# PORT = 80
# BATCH_SIZE = 100  # Nombre d'entrées avant d'écrire dans le CSV
# # Variable globale pour stocker le dernier temps de réception
# last_reception_time = None
# class MyHandler(http.server.SimpleHTTPRequestHandler):
#     data_list = []
#     def do_POST(self):
#         global last_reception_time
#         # Mesure du temps de début
#         current_time = time.time()
#         # Calcul du temps entre les réceptions si ce n'est pas la première requête
#         if last_reception_time is not None:
#             interval = current_time - last_reception_time
#             print("Temps écoulé depuis la dernière réception :", f"{interval:.6f} secondes")
#         else:
#             print("Première réception de données.")
#         # Met à jour le dernier temps de réception
#         last_reception_time = current_time
#         # Récupère la longueur et le contenu des données
#         content_length = int(self.headers['Content-Length'])
#         post_data = self.rfile.read(content_length)
#         # Affiche la longueur des données et le temps de réception
#         print("Longueur des données reçues :", content_length)
#         print("Données brutes reçues :", post_data)
#         try:
#             # Décode et nettoie les données entrantes
#             data_str = post_data.decode('utf-8').strip('[]')
#             readable_time = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
#             # Divise les données en éléments (séparés par des virgules)
#             pairs = data_str.split(',')
#             for pair in pairs:
#                 if ':' in pair:  # Si le pair contient ":", le traite normalement
#                     try:
#                         chaine, value = pair.split(':')
#                         chaine = int(chaine)
#                         value = float(value)
#                         processed_value = 0 if value == 0 else value
#                         MyHandler.data_list.append({
#                             'time': readable_time,
#                             'chaine': chaine,
#                             'value': processed_value,
#                             'error': None
#                         })
#                     except (ValueError, IndexError) as e:
#                         error_message = f"Erreur de formatage dans le pair '{pair}': {e}"
#                         print(error_message)
#                         MyHandler.data_list.append({
#                             'time': readable_time,
#                             'chaine': None,
#                             'value': None,
#                             'error': error_message
#                         })
#                         self.write_to_csv()
#                         self.send_error(400, f"Erreur de formatage: {pair}")
#                         return
#                 else:  # Si le pair ne contient pas ":", le traite comme une valeur indépendante
#                     try:
#                         value = float(pair)
#                         MyHandler.data_list.append({
#                             'time': readable_time,
#                             'chaine': None,
#                             'value': value,
#                             'error': None
#                         })
#                     except ValueError as e:
#                         error_message = f"Erreur de formatage dans le pair '{pair}': {e}"
#                         print(error_message)
#                         MyHandler.data_list.append({
#                             'time': readable_time,
#                             'chaine': None,
#                             'value': None,
#                             'error': error_message
#                         })
#                         self.write_to_csv()
#                         self.send_error(400, f"Erreur de formatage: {pair}")
#                         return
#             # Écrit dans le CSV si le lot est complet
#             if len(MyHandler.data_list) >= BATCH_SIZE:
#                 self.write_to_csv()
#         except (ValueError, IndexError) as e:
#             error_message = f"Erreur lors de la conversion des données : {e}"
#             print(error_message)
#             self.send_error(400, error_message)
#             return
#     def write_to_csv(self):
#         try:
#             df = pd.DataFrame(MyHandler.data_list)
#             df.to_csv('output.csv', mode='a', index=False, header=not pd.io.common.file_exists('output.csv'))
#             MyHandler.data_list.clear()
#             print("Données enregistrées dans le fichier CSV.")
#         except Exception as e:
#             print("Erreur lors de l'enregistrement dans le fichier CSV :", e)
# # Démarre le serveur
# with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
#     print(f"Serveur en écoute sur le port {PORT}")
#     httpd.serve_forever()
# 22222
import http.server
import socketserver
import pandas as pd
import numpy as np
import time
from datetime import datetime
PORT = 80
BATCH_SIZE = 100  # Nombre d'entrées avant d'écrire dans le CSV
LOT_SIZE = 500 # Nombre de valeurs avant de calculer RMS
# Variable globale pour stocker le dernier temps de réception
last_reception_time = None
class MyHandler(http.server.SimpleHTTPRequestHandler):
    data_list = []  # Liste pour stocker les données reçues
    tensions = {0: [], 1: [], 2: []}  # Dictionnaires pour les tensions
    courants = {3: [], 4: [], 5: []}  # Dictionnaires pour les courants
    def do_POST(self):
        global last_reception_time
        current_time = time.time()
        # Afficher le temps écoulé depuis la dernière réception
        if last_reception_time is not None:
            interval = current_time - last_reception_time
            print("Temps écoulé depuis la dernière réception :", f"{interval:.6f} secondes")
        else:
            print("Première réception de données.")
        last_reception_time = current_time
        # Lire les données envoyées par le client
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print("Longueur des données reçues :", content_length)
        print("Données brutes reçues :", post_data)
        try:
            # Décoder et nettoyer les données reçues
            data_str = post_data.decode('utf-8').strip('[]')
            pairs = data_str.split(',')
            for pair in pairs:
                if ':' in pair:
                    try:
                        chaine, value = pair.split(':')
                        # Vérifications avant conversion
                        if chaine.strip() == '' or value.strip() == '':
                            raise ValueError("Chaine ou valeur vide")
                        chaine = int(chaine.strip())
                        value = float(value.strip())
                        # Ajouter les valeurs dans les dictionnaires correspondants
                        if chaine in MyHandler.tensions:
                            MyHandler.tensions[chaine].append(value)
                        elif chaine in MyHandler.courants:
                            MyHandler.courants[chaine].append(value)
                        # Ajouter les données au format lisible
                        readable_time = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
                        MyHandler.data_list.append({
                            'time': readable_time,
                            'chaine': chaine,
                            'value': value,
                            'error': None
                        })
                    except ValueError as ve:
                        # Ajouter un message d'erreur pour la paire invalide
                        MyHandler.data_list.append({
                            'time': datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S'),
                            'chaine': pair,
                            'value': None,
                            'error': str(ve)
                        })
                        print(f"Erreur de conversion pour la paire '{pair}': {ve}")
            # Vérifier si chaque canal a atteint LOT_SIZE pour tensions et courants
            if all(len(MyHandler.tensions[ch]) >= LOT_SIZE for ch in MyHandler.tensions) and \
               all(len(MyHandler.courants[ch]) >= LOT_SIZE for ch in MyHandler.courants):
                # Calculer les RMS pour tensions et courants
                tensions_rms = self.calculate_rms(MyHandler.tensions)
                courants_rms = self.calculate_rms(MyHandler.courants)
                # Afficher les résultats des calculs RMS
                print("Dictionnaire des tensions : ", MyHandler.tensions)
                print("Dictionnaire des courants : ", MyHandler.courants)
                print("Tensions RMS :", tensions_rms)
                print("Courants RMS :", courants_rms)
                # Réinitialiser les dictionnaires pour les prochains lots
                for ch in MyHandler.tensions:
                    MyHandler.tensions[ch].clear()
                for ch in MyHandler.courants:
                    MyHandler.courants[ch].clear()
                # Vérifier les conditions pour envoyer open/close
                if (
                    (tensions_rms[0] > 100 and courants_rms[3] > 0) or
                    (tensions_rms[1] > 100 and courants_rms[4] > 0) or
                    (tensions_rms[2] > 100 and courants_rms[5] > 0)
                ):
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"open")
                    print("Conditions remplies, envoi de la commande : open")
                else:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"close")
                    print("Conditions non remplies, envoi de la commande : close")
            # Écriture dans le CSV si BATCH_SIZE atteint
            if len(MyHandler.data_list) >= BATCH_SIZE:
                self.write_to_csv()
        except Exception as e:
            error_message = f"Erreur lors du traitement des données : {e}"
            print(error_message)
            self.send_error(400, error_message)
            return
    def calculate_rms(self, data_dict):
        """
        Calcule la valeur efficace (RMS) pour chaque liste de données dans le dictionnaire.
        """
        rms_values = {}
        for key, values in data_dict.items():
            # Découper en sous-listes pour le calcul RMS par lot
            clean_values = [v for v in values if isinstance(v, (int, float)) and not np.isnan(v)]
            if len(clean_values) >= LOT_SIZE:
                sub_values = clean_values[-LOT_SIZE:]  # Garder uniquement les dernières valeurs LOT_SIZE
                rms = np.sqrt(np.mean(np.square(sub_values)))
                rms_values[key] = round(rms, 2)
            else:
                rms_values[key] = 0
        return rms_values
    def write_to_csv(self):
        
        try:
            df = pd.DataFrame(MyHandler.data_list)
            df.to_csv('output.csv', mode='a', index=False, header=not pd.io.common.file_exists('output.csv'))
            MyHandler.data_list.clear()
            print("Données enregistrées dans le fichier CSV.")
        except Exception as e:
            print("Erreur lors de l'enregistrement dans le fichier CSV :", e)

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serveur en écoute sur le port {PORT}")
    httpd.serve_forever()
