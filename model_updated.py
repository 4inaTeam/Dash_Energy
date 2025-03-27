import os
import time
import joblib
import pandas as pd
from keras.models import load_model
import numpy as np

##################### Chargement des modèles #############################
# model & encoder triphasé courant
model_courant_triph = joblib.load('models_updated/model_courant_triph.joblib')
label_encoder_courant_triph = joblib.load('models_updated/encoder_courant_triph.joblib')
# model & encoder mono courant
model_courant_mono = joblib.load('models_updated/model_courant_mono.joblib')
label_encoder_courant_mono = joblib.load('models_updated/encoder_courant_mono.joblib')

# model & encoder triphasé tension
model_tension_triph = joblib.load('models_updated/model_tension_triph.joblib')
label_tension_courant_triph = joblib.load('models_updated/encoder_tension_triph.joblib')
# model & encoder mono tension
model_tension_mono = joblib.load('models_updated/model_tension_mono.joblib')
label_encoder_tension_mono = joblib.load('models_updated/encoder_tension_mono.joblib')

# model & encoder triphasé puissance active
model_puissance_active_triph = joblib.load('models_updated/model_puissance.joblib')
label_encoder_puissance_active_triph = joblib.load('models_updated/encoder_puissance.joblib')
# model & encoder triphasé puissance apparente
model_puissance_apparente_triph = joblib.load('models_updated/model_puissance_apparente.joblib')
label_encoder_puissance_apparente_triph = joblib.load('models_updated/encoder_puissance_apparente.joblib')
# model & encoder triphasé puissance reactive
model_puissance_reactive_triph = joblib.load('models_updated/model_puissance_reactive.joblib')
label_encoder_puissance_reactive_triph = joblib.load('models_updated/encoder_puissance_reactive.joblib')

# model & encoder mono puissance active
model_puissance_active_mono = joblib.load('models_updated/model_puissance_active_mono.joblib')
label_encoder_puissance_active_mono = joblib.load('models_updated/encoder_puissance_mono.joblib')
# model & encoder mono puissance apparente
model_puissance_apparente_mono = joblib.load('models_updated/model_puissance_apparente_mono.joblib')
label_encoder_puissance_apparente_mono = joblib.load('models_updated/encoder_puissance_apparente_mono.joblib')
# model & encoder mono puissance reactive
model_puissance_reactive_mono = joblib.load('models_updated/model_puissance_reactive_mono.joblib')
label_encoder_puissance_reactive_mono = joblib.load('models_updated/encoder_puissance_reactive_mono.joblib')



############################################################# Prédictions de courant et tension avec random forest #############################################################




def predict_courant_tension_2():
    """
    Fonction pour prédire les valeurs de courant et de tension en continu à partir des
    données présentes dans 'stockage_data/data_efficace.csv'. Les prédictions sont sauvegardées
    dans 'predictions_files/data_courant_tension_predites.csv'.
    """
    while True:
        if not os.path.exists('stockage_data/data_efficace.csv'):
            time.sleep(1)
            continue

        try:
            # Lire les nouvelles données
            data = pd.read_csv('stockage_data/data_efficace.csv', on_bad_lines='skip')
            data['Date'] = pd.to_datetime(data['Date'])
            data.set_index('Date', inplace=True)
            ############################   Machine MONO ###########################
            # Prédictions pour les colonnes de courant 
            
            feature_courant_mono = data[[f'I_eff_0']].rename(columns={f'I_eff_0': 'courant'})
            prediction_c_mono = model_courant_mono.predict(feature_courant_mono)
            prediction_courant_mono = label_encoder_courant_mono.inverse_transform(np.argmax(prediction_c_mono, axis=1))
            data[f'code_courant_mono'] = prediction_courant_mono

            # Prédictions pour les colonnes de tension 
            
            feature_tension_mono = data[[f'V_eff_0']].rename(columns={f'V_eff_0': 'tension'})
            prediction_t_mono = model_tension_mono.predict(feature_tension_mono)
            prediction_tension_mono = label_encoder_tension_mono.inverse_transform(np.argmax(prediction_t_mono, axis=1))
            data[f'code_tension_mono'] = prediction_tension_mono

            # Prédictions pour les colonnes de puissance p 
            
            feature_p_mono = data[[f'P_0']].rename(columns={f'P_0': 'P'})
            prediction_p_mono = model_puissance_active_mono.predict(feature_p_mono)
            prediction_puiss_mono = label_encoder_puissance_active_mono.inverse_transform(np.argmax(prediction_p_mono, axis=1))
            data[f'code_p_mono'] = prediction_puiss_mono
            # Prédictions pour les colonnes de puissance s  
            feature_s_mono = data[[f'S_0']].rename(columns={f'S_0': 'tension'})
            prediction_s_mono = model_puissance_apparente_mono.predict(feature_s_mono)
            prediction_apparent_mono = label_encoder_puissance_apparente_mono.inverse_transform(np.argmax(prediction_s_mono, axis=1))
            data[f'code_s_mono'] = prediction_apparent_mono
            # Prédictions pour les colonnes de puissance s  de machine 1 triphasé
            
            feature_q_mono = data[[f'Q_0']].rename(columns={f'Q_0': 'Q'})
            prediction_q_mono = model_puissance_reactive_mono.predict(feature_q_mono)
            prediction_reactive_mono = label_encoder_puissance_reactive_mono.inverse_transform(np.argmax(prediction_q_mono, axis=1))
            data[f'code_q_mono'] = prediction_reactive_mono


            ############################   Machine 1 trihpase ###########################
            # Prédictions pour les colonnes de courant de machine 1 triphasé
            for i in range(1, 4):
                feature_courant_1 = data[[f'I_eff_{i}']].rename(columns={f'I_eff_{i}': 'courant'})
                prediction_c_1 = model_courant_triph.predict(feature_courant_1)
                prediction_courant_1 = label_encoder_courant_triph.inverse_transform(np.argmax(prediction_c_1, axis=1))
                data[f'code_courant_1{i}'] = prediction_courant_1

            # Prédictions pour les colonnes de tension de machine 1 triphasé
            for i in range(1, 4):
                feature_tension_1 = data[[f'V_eff_{i}']].rename(columns={f'V_eff_{i}': 'tension'})
                prediction_t_1 = model_tension_triph.predict(feature_tension_1)
                prediction_tension_1 = label_tension_courant_triph.inverse_transform(np.argmax(prediction_t_1, axis=1))
                data[f'code_tension_1{i}'] = prediction_tension_1

            # Prédictions pour les colonnes de puissance p de machine 1 triphasé
            for i in range(1, 4):
                feature_p_1 = data[[f'P_{i}']].rename(columns={f'P_{i}': 'P'})
                prediction_p_1 = model_puissance_active_triph.predict(feature_p_1)
                prediction_puiss_1 = label_encoder_puissance_active_triph.inverse_transform(np.argmax(prediction_p_1, axis=1))
                data[f'code_p_1{i}'] = prediction_puiss_1

            # Prédictions pour les colonnes de puissance s  de machine 1 triphasé
            for i in range(1, 4):
                feature_s_1 = data[[f'S_{i}']].rename(columns={f'S_{i}': 'tension'})
                prediction_s_1 = model_puissance_apparente_triph.predict(feature_s_1)
                prediction_apparent_1 = label_encoder_puissance_apparente_triph.inverse_transform(np.argmax(prediction_s_1, axis=1))
                data[f'code_s_1{i}'] = prediction_apparent_1
            # Prédictions pour les colonnes de puissance s  de machine 1 triphasé
            for i in range(1, 4):
                feature_q_1 = data[[f'Q_{i}']].rename(columns={f'Q_{i}': 'Q'})
                prediction_q_1 = model_puissance_reactive_triph.predict(feature_q_1)
                prediction_reactive_1 = label_encoder_puissance_reactive_triph.inverse_transform(np.argmax(prediction_q_1, axis=1))
                data[f'code_q_1{i}'] = prediction_reactive_1

            ############################   Machine 2 trihpase ###########################

            # Prédictions pour les colonnes de courant de machine 2 triphasé
            for i in range(4, 7):
                feature_courant_2 = data[[f'I_eff_{i}']].rename(columns={f'I_eff_{i}': 'courant'})
                prediction_c_2 = model_courant_triph.predict(feature_courant_2)
                prediction_courant_2 = label_encoder_courant_triph.inverse_transform(np.argmax(prediction_c_2, axis=1))
                data[f'code_courant_2{i}'] = prediction_courant_2

            # Prédictions pour les colonnes de tension de machine 2 triphasé
            for i in range(4, 7):
                feature_tension_2 = data[[f'V_eff_{i}']].rename(columns={f'V_eff_{i}': 'tension'})
                prediction_t_2 = model_tension_triph.predict(feature_tension_2)
                prediction_tension_2 = label_tension_courant_triph.inverse_transform(np.argmax(prediction_t_2, axis=1))
                data[f'code_tension_2{i}'] = prediction_tension_2
            # Prédictions pour les colonnes de puissance p de machine 2 triphasé
            for i in range(4, 7):
                feature_p_2 = data[[f'P_{i}']].rename(columns={f'P_{i}': 'P'})
                prediction_p_2 = model_puissance_active_triph.predict(feature_p_2)
                prediction_puiss_2 = label_encoder_puissance_active_triph.inverse_transform(np.argmax(prediction_p_2, axis=1))
                data[f'code_p_2{i}'] = prediction_puiss_2

            # Prédictions pour les colonnes de puissance s  de machine 2 triphasé
            for i in range(4, 7):
                feature_s_2 = data[[f'S_{i}']].rename(columns={f'S_{i}': 'tension'})
                prediction_s_2 = model_puissance_apparente_triph.predict(feature_s_2)
                prediction_apparent_2 = label_encoder_puissance_apparente_triph.inverse_transform(np.argmax(prediction_s_2, axis=1))
                data[f'code_s_2{i}'] = prediction_apparent_2
            # Prédictions pour les colonnes de puissance s  de machine 2 triphasé
            for i in range(4, 7):
                feature_q_2 = data[[f'Q_{i}']].rename(columns={f'Q_{i}': 'Q'})
                prediction_q_2 = model_puissance_reactive_triph.predict(feature_q_2)
                prediction_reactive_2 = label_encoder_puissance_reactive_triph.inverse_transform(np.argmax(prediction_q_2, axis=1))
                data[f'code_q_2{i}'] = prediction_reactive_2

            # Créer le code final combiné
            data['code_Mono'] = data['code_courant_mono'] + data['code_tension_mono']
            data['code_validation_mono'] =  data['code_p_mono'] + data['code_s_mono'] + data['code_q_mono']
           
            # Créer les codes combinés pour courant et tension pour machine 1
            data['code_courant_1'] = data.apply(lambda x: ''.join(map(str, [x[f'code_courant_1{i}'] for i in range(1, 4)])), axis=1)
            data['code_tension_1'] = data.apply(lambda x: ''.join(map(str, [x[f'code_tension_1{i}'] for i in range(1, 4)])), axis=1)
            # Créer les codes combinés pour puissanec p et s et q e pour machine 1
            data['code_p_1'] = data.apply(lambda x: ''.join(map(str, [x[f'code_p_1{i}'] for i in range(1, 4)])), axis=1)
            data['code_s_1'] = data.apply(lambda x: ''.join(map(str, [x[f'code_s_1{i}'] for i in range(1, 4)])), axis=1)
            data['code_q_1'] = data.apply(lambda x: ''.join(map(str, [x[f'code_q_1{i}'] for i in range(1, 4)])), axis=1)

            # Créer le code final combiné
            data['code_M1'] = data['code_courant_1'] + data['code_tension_1']
            data['code_validation1'] =  data['code_p_1'] + data['code_s_1'] + data['code_q_1']

            # Créer les codes combinés pour courant et tension pour machine 2
            data['code_courant_2'] = data.apply(lambda x: ''.join(map(str, [x[f'code_courant_2{i}'] for i in range(1, 4)])), axis=1)
            data['code_tension_2'] = data.apply(lambda x: ''.join(map(str, [x[f'code_tension_2{i}'] for i in range(1, 4)])), axis=1)
            # Créer les codes combinés pour puissanec p et s et q e pour machine 2
            data['code_p_2'] = data.apply(lambda x: ''.join(map(str, [x[f'code_p_2{i}'] for i in range(4, 7)])), axis=1)
            data['code_s_2'] = data.apply(lambda x: ''.join(map(str, [x[f'code_s_2{i}'] for i in range(4, 7)])), axis=1)
            data['code_q_2'] = data.apply(lambda x: ''.join(map(str, [x[f'code_q_2{i}'] for i in range(4, 7)])), axis=1)

            # Créer le code final combiné
            data['code_M2'] = data['code_courant_2'] + data['code_tension_2']
            data['code_validation2'] =  data['code_p_2'] + data['code_s_2'] + data['code_q_2']

            # Sauvegarder les résultats
            data.reset_index(inplace=True)
            selected_data = data[['Date'] + [f'I_eff_{i}' for i in range(0, 7)] + [f'V_eff_{i}' for i in range(0, 7)]
                                 + [f'P_{i}' for i in range(0, 7)] + [f'S_{i}' for i in range(0, 7)] + [f'Q_{i}' for i in range(0, 7)]  
                                 + ['code_Mono'] + data['code_validation_mono'] + ['code_M1'] + data['code_validation1']  + ['code_M2'] + data['code_validation2']]
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








