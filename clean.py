# import pandas as pd
# import time
# import os
# def update_csv():
#     # Charger le fichier CSV avec les colonnes "time", "chaine", "value", et "error"
#     df = pd.read_csv('output.csv')
#     # Vérifier que le DataFrame contient bien les colonnes attendues
#     if not {'time', 'chaine', 'value', 'error'}.issubset(df.columns):
#         raise ValueError("Le fichier CSV doit contenir les colonnes 'time', 'chaine', 'value', et 'error'.")
#     # Filtrer les lignes sans erreur (colonne "error" vide)
#     df = df[df['error'].isna()]
#     # Liste pour stocker les lignes valides
#     rows = []
#     # Parcourir les données pour regrouper les valeurs par 8 lignes consécutives
#     for i in range(0, len(df), 8):
#         subset = df.iloc[i:i + 8]  # Obtenir 8 valeurs consécutives
#         if len(subset) == 8 and set(subset['chaine']) == {0, 1, 2, 3, 4, 5, 6, 7}:  # Vérifier qu'il y a bien 8 lignes uniques de 0 à 7
#             # Obtenir le timestamp du premier capteur dans le groupe
#             timestamp = subset.iloc[0]['time']
#             # Extraire les valeurs
#             values = subset.sort_values(by='chaine')['value'].tolist()
#             # Vérifier les conditions pour chaque capteur
#             tensions = values[0:3]
#             courants = values[3:6]
#             temperature = values[6]
#             cosphi = values[7]
#             if (
#                 all(-3500 <= t <= 3500 for t in tensions) and
#                 all(-3500 <= c <= 3500 for c in courants) and
#                 temperature <= 50 and
#                 -1 <= cosphi <= 1  # Plage typique pour cos phi
#             ):
#                 # Ajouter la ligne si toutes les valeurs sont dans les plages spécifiées, en incluant le timestamp
#                 rows.append([timestamp] + values)
#     # Créer un DataFrame avec les colonnes souhaitées
#     output_df = pd.DataFrame(rows, columns=['Date', 'tension1', 'tension2', 'tension3', 'courant1', 'courant2', 'courant3', 'temp', 'cosphi'])
#     # Sauvegarder le fichier CSV résultant
#     output_df.to_csv('fichier_clean5.csv', index=False)
#     output_df.to_csv('stockage_data/min_data.csv', index=False)

#     print("Fichier 'csv' généré avec succès.")
# # Boucle pour surveiller les nouveaux ajouts toutes les 10 secondes
# last_modified_time = 0
# while True:
#     try:
#         # Vérifier l'heure de la dernière modification du fichier CSV
#         current_modified_time = os.path.getmtime('output.csv')
#         if current_modified_time > last_modified_time:
#             print("Nouvelles données détectées, mise à jour du fichier...")
#             update_csv()
#             last_modified_time = current_modified_time
#         # Attendre 10 secondes avant de vérifier à nouveau
#         time.sleep(1)
#     except Exception as e:
#         print(f"Erreur : {e}")
#         break




# import pandas as pd
# import numpy as np
# import os
# import time
# def update_csv():
#     Charger le fichier CSV
#     df = pd.read_csv('output.csv', header=None, names=['time', 'chaine', 'value', 'error'], delimiter=',')
#     Filtrer les lignes sans erreur
#     df = df[df['error'].isna()]
#     Convertir les colonnes aux bons types
#     df['chaine'] = df['chaine'].astype(int)
#     df['value'] = pd.to_numeric(df['value'], errors='coerce')  # Convertir les valeurs en float, avec gestion des erreurs
#     Trouver la première occurrence de chaine = 0
#     first_index = df[df['chaine'] == 0].index.min()
#     if first_index is None:
#         print("Aucune chaîne 0 trouvée. Pas de nettoyage effectué.")
#         return  # Sortir si aucune chaîne 0 n'est trouvée
#     Couper le DataFrame à partir de la première chaîne 0
#     df = df.loc[first_index:].reset_index(drop=True)
#     rows = []  # Liste pour stocker les groupes valides
#     i = 0
#     while i < len(df):
#         subset = df.iloc[i:i + 8]  # Obtenir 8 valeurs consécutives
#         Vérifier qu'il y a 8 lignes avec les chaînes uniques de 0 à 7 dans l'ordre
#         if len(subset) == 8 and list(subset['chaine'].values) == [0, 1, 2, 3, 4, 5, 6, 7]:
#             subset = subset.sort_values(by='chaine')  # S'assurer de l'ordre (bien que l'on a déjà validé l'ordre précédemment)
#             timestamp = subset.iloc[0]['time']  # Timestamp
#             values = subset['value'].tolist()
#             Extraire les valeurs
#             tensions = values[0:3]
#             courants = values[3:6]
#             temperature = values[6]
#             cosphi = values[7]
#             Appliquer des conditions strictes
#             if (
#                 all(-3500 <= t <= 3500 for t in tensions) and  # Plage pour les tensions
#                 all(-3000 <= c <= 3000 for c in courants) and # Plage pour les courants
#                 -10 <= temperature <= 50 and                 # Température raisonnable
#                 -1 <= cosphi <= 1                            # Cos(phi)
#             ):
#                 Ajouter le groupe valide
#                 rows.append([timestamp] + values)
#             i += 8  # Passer au prochain groupe
#         else:
#             Si le groupe est incomplet ou mal ordonné, passer à la ligne suivante
#             i += 1
#     Créer un DataFrame avec les colonnes nécessaires
#     output_df = pd.DataFrame(rows, columns=['time', 't1', 't2', 't3', 'c1', 'c2', 'c3', 'temp', 'cosphi'])
#     Sauvegarder dans un fichier
#     if not output_df.empty:
#         output_df.to_csv('fichier_clean5.csv', mode='a', header=not os.path.exists('fichier_clean5.csv'), index=False)
#         print("Données ajoutées au fichier 'fichier_clean5.csv'.")
#     else:
#         print("Aucun groupe valide trouvé.")
# Boucle principale
# last_modified_time = 0
# while True:
#     try:
#         current_modified_time = os.path.getmtime('output.csv')
#         if current_modified_time > last_modified_time:
#             print("Nouvelles données détectées, mise à jour du fichier...")
#             update_csv()
#             last_modified_time = current_modified_time
#         time.sleep(1)
#     except Exception as e:
#         print(f"Erreur : {e}")
#         break




# import pandas as pd
# import numpy as np
# import os
# import time
# def update_csv():
#     # Charger le fichier CSV avec les colonnes "time", "chaine", "value", et "error"
#     df = pd.read_csv('output.csv')
#     # Vérifier que le DataFrame contient bien les colonnes attendues
#     if not {'time', 'chaine', 'value', 'error'}.issubset(df.columns):
#         raise ValueError("Le fichier CSV doit contenir les colonnes 'time', 'chaine', 'value', et 'error'.")
#     # Filtrer les lignes sans erreur (colonne "error" vide)
#     df = df[df['error'].isna()]
#     # Liste pour stocker les lignes valides
#     rows = []
#     # Parcourir les données pour regrouper les valeurs par 8 lignes consécutives
#     for i in range(0, len(df), 8):
#         subset = df.iloc[i:i + 8]  # Obtenir 8 valeurs consécutives
#         if len(subset) == 8 and set(subset['chaine']) == {0, 1, 2, 3, 4, 5, 6, 7}:  # Vérifier qu'il y a bien 8 lignes uniques de 0 à 7
#             # Obtenir le timestamp du premier capteur dans le groupe
#             timestamp = subset.iloc[0]['time']
#             # Extraire les valeurs
#             values = subset.sort_values(by='chaine')['value'].tolist()
#             # Vérifier les conditions pour chaque capteur
#             tensions = values[0:3]
#             courants = values[3:6]
#             temperature = values[6]
#             cosphi = values[7]
#             if (
#                 all(-3500 <= t <= 3500 for t in tensions) and
#                 all(-3500 <= c <= 3500 for c in courants) and
#                 temperature <= 50 and
#                 -1 <= cosphi <= 1  # Plage typique pour cos phi
#             ):
# # # # def update_csv():
# # # #     # Charger le fichier CSV
# # # #     df = pd.read_csv('output.csv', header=None, names=['time', 'chaine', 'value', 'error'])
# # # #     # Filtrer les lignes sans erreur
# # # #     df = df[df['error'].isna()]
# # # #     # Convertir les colonnes aux bons types
# # # #     df['chaine'] = df['chaine'].astype(int)
# # # #     df['value'] = df['value'].astype(float)
# # # #     # Trouver la première occurrence de chaine = 0
# # # #     first_index = df[df['chaine'] == 0].index.min()
# # # #     if first_index is None:
# # # #         print("Aucune chaîne 0 trouvée. Pas de nettoyage effectué.")
# # # #         return  # Sortir si aucune chaîne 0 n'est trouvée
# # # #     # Couper le DataFrame à partir de la première chaîne 0
# # # #     df = df.loc[first_index:].reset_index(drop=True)
# # # #     rows = []  # Liste pour stocker les groupes valides
# # # #     i = 0
# # # #     while i < len(df):
# # # #         subset = df.iloc[i:i + 8]  # Obtenir 8 valeurs consécutives
# # # #         # Vérifier qu'il y a 8 lignes avec les chaînes uniques de 0 à 7
# # # #         if len(subset) == 8 and subset['chaine'].values.all() == np.array([0, 1, 2, 3, 4, 5, 6, 7]).all():
# # # #             subset = subset.sort_values(by='chaine')  # S'assurer de l'ordre
# # # #             timestamp = subset.iloc[0]['time']  # Timestamp
# # # #             values = subset['value'].tolist()
# # # #             # Extraire les valeurs
# # # #             tensions = values[0:3]
# # # #             courants = values[3:6]
# # # #             temperature = values[6]
# # # #             cosphi = values[7]
# # # #             # Appliquer des conditions strictes
# # # #             if (
# # # #                 all(-3500 <= t <= 3500 for t in tensions) and  # Plage pour les tensions
# # # #                 all(-3000 <= c <= 3000 for c in courants) and # Plage pour les courants
# # # #                 -10 <= temperature <= 50 and                 # Température raisonnable
# # # #                 -1 <= cosphi <= 1                            # Cos(phi)
# # # #             ):
#                 # Ajouter le groupe valide
#                 rows.append([timestamp] + values)
#             i += 8  # Passer au prochain groupe
#         else:
#             # Sinon, passer à la prochaine ligne pour chercher un groupe valide
#             i += 1
#     # Créer un DataFrame avec les colonnes nécessaires
#     output_df = pd.DataFrame(rows, columns=['time', 't1', 't2', 't3', 'c1', 'c2', 'c3', 'temp', 'cosphi'])
#     # Sauvegarder dans un fichier
#     if not output_df.empty:
#         output_df.to_csv('stockage_data/min_data.csv', mode='a', header=not os.path.exists('stockage_data/min_data.csv'), index=False)
#         print("Données ajoutées au fichier 'stockage_data/min_data.csv'.")
#     else:
#         print("Aucun groupe valide trouvé.")
# # Boucle principale
# last_modified_time = 0
# while True:
#     try:
#         current_modified_time = os.path.getmtime('output.csv')
#         if current_modified_time > last_modified_time:
#             print("Nouvelles données détectées, mise à jour du fichier...")
#             update_csv()
#             last_modified_time = current_modified_time
#         time.sleep(1)
#     except Exception as e:
#         print(f"Erreur : {e}")
#         break

# 333333
import pandas as pd
import numpy as np
import os
import time
last_index = -1  # Variable pointeur pour suivre la dernière ligne traitée
def update_csv():
    global last_index
    # Charger le fichier CSV
    df = pd.read_csv('output.csv', header=None, names=['time', 'chaine', 'value', 'error'], delimiter=',', low_memory=False)
    # Filtrer les lignes sans erreur
    df = df[df['error'].isna()]
    # Convertir les colonnes aux bons types
    df['chaine'] = df['chaine'].astype(int)
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    # Vérifier si de nouvelles lignes sont disponibles
    if last_index >= len(df) - 1:
        print("Aucune nouvelle donnée à traiter.")
        return
    # Ignorer les lignes déjà traitées
    df = df.iloc[last_index + 1:].reset_index(drop=True)
    # Trouver la première occurrence de chaine = 0
    first_index = df[df['chaine'] == 0].index.min()
    if first_index is None:
        print("Aucune chaîne 0 trouvée. Pas de nettoyage effectué.")
        return  # Sortir si aucune chaîne 0 n'est trouvée
    # Couper le DataFrame à partir de la première chaîne 0
    df = df.loc[first_index:].reset_index(drop=True)
    rows = []  # Liste pour stocker les groupes valides
    new_last_index = last_index  # Nouveau pointeur mis à jour après traitement
    i = 0
    while i <= len(df) - 8:  # Assurer qu'on peut prendre un bloc de 8 lignes
        subset = df.iloc[i:i + 8]  # Obtenir 8 valeurs consécutives
        # Vérifier qu'il y a 8 lignes avec les chaînes uniques de 0 à 7 dans l'ordre
        if list(subset['chaine'].values) == [0, 1, 2, 3, 4, 5, 6, 7]:
            subset = subset.sort_values(by='chaine')  # S'assurer de l'ordre
            timestamp = subset.iloc[0]['time']  # Timestamp
            values = subset['value'].tolist()
            # Extraire les valeurs
            tensions = values[0:3]
            courants = values[3:6]
            temperature = values[6]
            cosphi = values[7]
            # Appliquer des conditions strictes
            if (
                all(-3500 <= t <= 3500 for t in tensions) and  # Plage pour les tensions
                all(-3000 <= c <= 3000 for c in courants) and # Plage pour les courants
                -10 <= temperature <= 50 and                 # Température raisonnable
                -1 <= cosphi <= 1                            # Cos(phi)
            ):
                # Ajouter le groupe valide
                rows.append([timestamp] + values)
                new_last_index = last_index + first_index + i + 7  # Mettre à jour l'index à la dernière ligne du groupe valide
            i += 8  # Passer au prochain groupe
        else:
            i += 1  # Si le groupe est incomplet, avancer d'une ligne
    # Mettre à jour le pointeur global après avoir traité les nouvelles données
    last_index = new_last_index
    # Créer un DataFrame avec les colonnes nécessaires
    output_df = pd.DataFrame(rows, columns=['Date', 'tension1', 'tension2', 'tension3', 'courant1', 'courant2', 'courant3', 'temp', 'cosphi'])
    output_df1 = pd.DataFrame(rows, columns=['Date', 'tension1', 'tension2', 'tension3', 'courant1', 'courant2', 'courant3', 'temp', 'cosphi'])
    # Sauvegarder dans un fichier
    if not output_df.empty:
        output_df.to_csv('stockage_data/min_data.csv', mode='a', header=not os.path.exists('stockage_data/min_data.csv'), index=False)
        print("Données ajoutées au fichier 'stockage_data/min_data.csv'.")
        output_df1.to_csv('temporal_data/min_data.csv', mode='a', header=not os.path.exists('stockage_data/min_data.csv'), index=False)
        print("Données ajoutées au fichier 'temporal_data/min_data.csv'.")
    else:
        print("Aucun groupe valide trouvé.")
# Boucle principale
# Initialiser le temps de modification du fichier à 0
last_modified_time = 0
while True:
    try:
        # Obtenir le temps de la dernière modification du fichier 'output.csv'
        current_modified_time = os.path.getmtime('output.csv')
        # Vérifier si le fichier a été modifié depuis la dernière vérification
        if current_modified_time > last_modified_time:
            print("Nouvelles données détectées, mise à jour du fichier...")
             # Appeler la fonction update_csv() pour traiter les nouvelles données
            update_csv()
             # Mettre à jour le dernier temps de modification connu
            last_modified_time = current_modified_time
        time.sleep(1)
    except Exception as e:
        print(f"Erreur : {e}")
        break



