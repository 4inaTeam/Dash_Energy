import os
import time
import joblib
import pandas as pd
from keras.models import load_model
import numpy as np

##################### Chargement des modèles #############################

# Chargement du label encoder pour les données de courant
label_encoder_courant = joblib.load('Lstm_models/label_encoder.pkl')

# Chargement du modèle LSTM pour les prédictions de courant
model_courant_lstm = load_model('Lstm_models/model.h5')

# Chargement du label encoder pour les données de tension
label_encoder_tension = joblib.load('Lstm_models/label_encoder_tension.pkl')

# Chargement du modèle LSTM pour les prédictions de tension
model_tension_lstm = load_model('Lstm_models/model_tension.h5')

# Chargement du modèle et de l'encodeur pour les prévisions de température
model_tm1 = joblib.load('models_1/model_temp_1.joblib')
encoder_tm1 = joblib.load('models_1/encoder_temp_1.joblib')

############################################################# Prédictions de température ##############################################################

def predict_temp_1():
    """
    Fonction pour prédire les températures en continu à partir des données
    présentes dans 'files_csv/maps_temp_data.csv'. Les prédictions sont sauvegardées
    dans 'predictions_files/data_temp_predites.csv'.
    """
    while True:
        # Attendre jusqu'à ce que le fichier CSV soit disponible
        while not os.path.exists('files_csv/maps_temp_data.csv'):
            time.sleep(1)

        try:
            # Lire les données
            data = pd.read_csv('files_csv/maps_temp_data.csv', sep=',')
            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)

            # Faire des prédictions pour chaque colonne de température
            for i in range(1, 4):
                feature = data[[f'temperature{i}']].rename(columns={f'temperature{i}': 'Temperature1'})
                prediction = model_tm1.predict(feature)
                data[f'code_temperature{i}'] = encoder_tm1.inverse_transform(prediction)[0]

            # Créer un code basé sur les prédictions
            data['code'] = data.apply(lambda x: ''.join(map(str, [x[f'code_temperature{i}'] for i in range(1, 4)])), axis=1)
            data.reset_index(inplace=True)

            # Sélectionner les colonnes pertinentes pour sauvegarder
            columns_to_save = ['Date'] + [f'temperature{i}' for i in range(1, 4)] + ['code']
            data[columns_to_save].to_csv('predictions_files/data_temp_predites.csv', mode='a',
                                         header=not os.path.exists('predictions_files/data_temp_predites.csv'),
                                         index=False)
            time.sleep(1)  # Attendre avant de recommencer

        except pd.errors.ParserError as e:
            print(f"Erreur de parseur : {e}. Ligne ignorée.")
        except Exception as e:
            print(f"Une erreur s'est produite lors de la prédiction : {e}")

############################################################# Prédictions de courant et tension avec LSTM #############################################################

def predict_courant_tension_2():
    """
    Fonction pour prédire les valeurs de courant et de tension en continu à partir des
    données présentes dans 'stockage_data/min_data.csv'. Les prédictions sont sauvegardées
    dans 'predictions_files/data_courant_tension_predites.csv'.
    """
    while True:
        if not os.path.exists('stockage_data/min_data.csv'):
            time.sleep(1)
            continue

        try:
            # Lire les nouvelles données
            data = pd.read_csv('stockage_data/min_data.csv', on_bad_lines='skip')
            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)

            # Prédictions pour les colonnes de courant
            for i in range(1, 4):
                feature_courant = data[[f'courant{i}']].rename(columns={f'courant{i}': 'courant1'})
                prediction = model_courant_lstm.predict(feature_courant)
                prediction_courant = label_encoder_courant.inverse_transform(np.argmax(prediction, axis=1))
                data[f'code_courant{i}'] = prediction_courant

            # Prédictions pour les colonnes de tension
            for i in range(1, 4):
                feature_tension = data[[f'tension{i}']].rename(columns={f'tension{i}': 'tension1'})
                prediction = model_tension_lstm.predict(feature_tension)
                prediction_tension = label_encoder_tension.inverse_transform(np.argmax(prediction, axis=1))
                data[f'code_tension{i}'] = prediction_tension

            # Créer les codes combinés pour courant et tension
            data['code_courant_1'] = data.apply(lambda x: ''.join(map(str, [x[f'code_courant{i}'] for i in range(1, 4)])), axis=1)
            data['code_tension_1'] = data.apply(lambda x: ''.join(map(str, [x[f'code_tension{i}'] for i in range(1, 4)])), axis=1)

            # Créer le code final combiné
            data['code_M1'] = data['code_courant_1'] + data['code_tension_1']

            # Sauvegarder les résultats
            data.reset_index(inplace=True)
            selected_data = data[['Date'] + [f'courant{i}' for i in range(1, 4)] + [f'tension{i}' for i in range(1, 4)] + ['code_M1']]
            selected_data.to_csv('predictions_files/data_courant_tension_predites.csv', mode='a',
                                 header=not os.path.exists('predictions_files/data_courant_tension_predites.csv'),
                                 index=False)

            time.sleep(1)  # Attendre avant de recommencer

        except pd.errors.ParserError as e:
            print(f"Erreur de parseur : {e}. Ligne ignorée.")
            time.sleep(1)  # Attendre un peu avant de réessayer
        except Exception as e:
            print(f"Une erreur s'est produite lors de la prédiction : {e}")
            time.sleep(1)  # Attendre un peu avant de réessayer



            
'''
def predict_courant_tension_2():
    while True:
        if not os.path.exists('stockage_data/min_data.csv'):
            time.sleep(1)
            continue

        try:
            # Lire les nouvelles données
            data = pd.read_csv('stockage_data/min_data.csv', on_bad_lines='skip')
            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)

            # Normaliser les données
            for i in range(1, 7):
                feature_courant = data[[f'courant{i}']].rename(columns={f'courant{i}': 'courant1'})

                # Faire des prédictions
                prediction = model_courant_lstm.predict(feature_courant)
                prediction_courant = label_encoder_courant.inverse_transform(np.argmax(prediction, axis=1))
                data[f'code_courant{i}'] = prediction_courant

            # Prédire les codes de tension à l'aide de genere_code_tension
            for i in range(1, 7):
                feature_tension = data[[f'tension{i}']].rename(columns={f'tension{i}': 'tension1'})

                # Faire des prédictions
                prediction = model_tension_lstm.predict(feature_tension)
                prediction_tension = label_encoder_tension.inverse_transform(np.argmax(prediction, axis=1))
                data[f'code_tension{i}'] = prediction_tension

            # Créer les codes courants et tensions
            data['code_courant'] = data.apply(lambda x: ''.join(map(str, [x[f'code_courant{i}'] for i in range(1, 7)])), axis=1)
            data['code_tension'] = data.apply(lambda x: ''.join(map(str, [x[f'code_tension{i}'] for i in range(1, 7)])), axis=1)

            # Créer le code final
            data['code_c'] = data['code_courant']
            data['code_t'] = data['code_tension']

            # Sauvegarder les résultats
            data.reset_index(inplace=True)
            selected_data = data[['Date'] + [f'courant{i}' for i in range(1, 7)] + [f'tension{i}' for i in range(1, 7)] + ['code_c'] + ['code_t']]
            selected_data.to_csv('predictions_files/data_courant_tension_predites.csv', mode='a', header=not os.path.exists('predictions_files/data_courant_tension_predites.csv'), index=False)

            time.sleep(1)
        except pd.errors.ParserError as e:
            print(f"Erreur de parseur : {e}. Ligne ignorée.")
        except Exception as e:
            print(f"Une erreur s'est produite lors de la prédiction : {e}")

            '''