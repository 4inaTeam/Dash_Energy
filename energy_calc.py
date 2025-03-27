import pandas as pd
import numpy as np
from math import sqrt
from sklearn.preprocessing import StandardScaler
import csv
import os 
import time

import numpy as np

# Fonction pour calculer les valeurs efficaces (RMS) d'une colonne de données
def calculate_rms(data):
    squared_values = data ** 2
    mean_square = squared_values.mean()
    return np.sqrt(mean_square)

# Fonction pour calculer les valeurs efficaces (RMS) de tension et courant
def calculate_effective_values(data):
    num_phases = 3
    V_eff = [calculate_rms(data[f'tension{i+1}']) for i in range(num_phases)]
    I_eff = [calculate_rms(data[f'courant{i+1}']) for i in range(num_phases)]
    return V_eff, I_eff


# Fonction pour calculer la puissance active, apparente et le facteur de puissance
def calculate_power(data, board_voltage):
    num_phases = 3
    vref = board_voltage / 1024  # Tension de référence du panneau
    
    # Facteurs d'exactitude pour le courant et la tension
    ct_accuracy_factor = 0.05
    AC_voltage_accuracy_factor = 10
    AC_voltage_ratio = 0.5
    
    # Facteur de correction du courant
    def scale_factor(ct_accuracy_factor):
        return vref * 100 * ct_accuracy_factor
    
    # Facteur de correction de la tension
    voltage_scaling_factor = vref * AC_voltage_ratio * AC_voltage_accuracy_factor
    
    # Initialisation des listes pour stocker les résultats
    P = [0] * num_phases
    S = [0] * num_phases
    cos_phi = [0] * num_phases
    
    # Calculer les valeurs efficaces pour chaque phase
    for i in range(num_phases):
        voltage_data = data[f'tension{i+1}']
        current_data = data[f'courant{i+1}']
        
        # Calculer la puissance active P comme le produit instantané de la tension et du courant
        inst_power = (voltage_data * current_data).mean()
        
        # Utiliser les valeurs efficaces pour calculer la puissance apparente et le cos(phi)
        V_eff = calculate_rms(voltage_data)
        I_eff = calculate_rms(current_data)
        
        P[i] = inst_power 
        S[i] = V_eff * I_eff
        cos_phi[i] = P[i] / S[i] if S[i] != 0 else 0
    
    return P, S, cos_phi

# Fonction pour traiter une ligne de données
def process_data(row, board_voltage):
    # Calculer les valeurs efficaces (RMS)
    V_eff, I_eff = calculate_effective_values(row)
    
    # Calculer les puissances
    P, S, cos_phi = calculate_power(row, board_voltage)
    
    # Ajouter les résultats au DataFrame
    for i in range(3):
        row[f'I_eff_{i+1}'] = I_eff[i]
        row[f'V_eff_{i+1}'] = V_eff[i]
        row[f'P_{i+1}'] = P[i]
        row[f'S_{i+1}'] = S[i]
        row[f'cos_phi_{i+1}'] = cos_phi[i]
    
    return row
def calculate_accumulated_energy(data):
    # Extract relevant columns
    time = pd.to_datetime(data['Date'])  # Convert 'Date' column to datetime
    P_1 = data['P_1'].astype(float)  # Using S_1 for energy calculation

    # Initialize variables for energy calculation
    EnergyKwhtot = 0
    accumulated_energy = []
    timestamps = []

    # Prepare CSV output file for accumulated energy
    with open('accumulated_energy.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Date', 'Accumulated Energy (kWh)'])

        # Calculate accumulated energy for each new data point
        for k in range(len(data) - 1):
            tim1 = time[k]
            tim2 = time[k + 1]

            # Calculate time difference in seconds
            deltah = (tim2 - tim1).total_seconds()

            # Apparent power in VA (volt-ampere)
            s = P_1[k] / 1000
            s = s / 3600

            # Calculate energy in kWh
            EnergyKwh = abs(s)  # This might need adjustment based on your energy calculation logic

            # Update total accumulated energy
            EnergyKwhtot += EnergyKwh

            # Append results to lists for plotting (if needed)
            accumulated_energy.append(EnergyKwhtot)
            timestamps.append(tim2)

            # Write date and accumulated energy to CSV
            csv_writer.writerow([tim2, EnergyKwhtot])

            # Debug prints
            #print(f"Timestamp: {tim2}, Energy (kWh): {EnergyKwh:.10f}, Accumulated Energy (kWh): {EnergyKwhtot:.10f}")

        return EnergyKwhtot


   
# Fonction pour simuler le traitement en temps réel
def simulate_real_time_processing_energy():
    columns = ['Date', 
               'courant1', 'courant2', 'courant3', 
               'tension1', 'tension2', 'tension3',
               'I_eff_1', 'V_eff_1', 'P_1', 'S_1', 'cos_phi_1', 
               'I_eff_2', 'V_eff_2', 'P_2', 'S_2', 'cos_phi_2', 
               'I_eff_3', 'V_eff_3', 'P_3', 'S_3', 'cos_phi_3'
              ]
    
    # Vérifier si le fichier min_data.csv existe
    while not os.path.exists('stockage_data/min_data.csv'):
        time.sleep(1)
    
    # Créer le fichier CSV avec le header uniquement s'il n'existe pas déjà
    if not os.path.exists('stockage_data/energy_data.csv'):
        with open('stockage_data/energy_data.csv', 'w') as f:
            f.write(','.join(columns) + '\n')
    
    # Boucle principale
    while True:
        # Lire la dernière ligne ajoutée au fichier CSV
        new_data = pd.read_csv('stockage_data/min_data.csv').tail(1)
        
        # Traiter la nouvelle ligne
        processed_data = process_data(new_data, board_voltage=5.0)  # Exemple de tension du panneau
        
        # Ajouter les données traitées au fichier data_all.csv
        processed_data.to_csv('stockage_data/energy_data.csv', mode='a', header=False, index=False)
        
        # Attendre un court instant pour que le fichier soit accessible
        time.sleep(3)

        # Read the updated data from CSV to include the latest entry
        data = pd.read_csv('stockage_data/energy_data.csv')

        # Calculate accumulated energy and get the latest total
        latest_accumulated_energy = calculate_accumulated_energy(data)

        # Print the latest accumulated energy (optional)
        print(f"Latest Accumulated Energy: {latest_accumulated_energy:.4f} kWh")

        # Add a delay before reading new data (adjust as needed)
        time.sleep(3)  # Attendre 1 seconde avant la prochaine itération



















'''

new calcul a determiner ##########
import pandas as pd
import numpy as np
from math import sqrt
from sklearn.preprocessing import StandardScaler
import csv
import os 
import time

import numpy as np

# Fonction pour calculer les valeurs efficaces (RMS) d'une colonne de données
def calculate_rms(data):
    squared_values = data ** 2
    mean_square = squared_values.mean()
    return np.sqrt(mean_square)

# Fonction pour calculer les valeurs efficaces (RMS) de tension et courant
def calculate_effective_values(data):
    num_phases = 3
    V_eff = [calculate_rms(data[f'tension{i+1}']) for i in range(num_phases)]
    I_eff = [calculate_rms(data[f'courant{i+1}']) for i in range(num_phases)]
    return V_eff, I_eff

def calculate_power(data, board_voltage):
    num_phases = 3
    vref = board_voltage / 1024  # Tension de référence du panneau
    
    # Facteurs d'exactitude pour le courant et la tension
    ct_accuracy_factor = 0.05
    AC_voltage_accuracy_factor = 10
    AC_voltage_ratio = 0.5
    
    # Initialisation des listes pour stocker les résultats
    P_inst = [0] * num_phases
    S_eff = [0] * num_phases
    cos_phi_inst = [0] * num_phases
    
    # Calculer les valeurs instantanées pour chaque phase
    for i in range(num_phases):
        voltage_data = data[f'tension{i+1}']
        current_data = data[f'courant{i+1}']
        
        # Calculer la puissance active instantanée P_inst comme le produit instantané de la tension et du courant
        P_inst[i] = (voltage_data * current_data)
        
        # Utiliser les valeurs efficaces pour calculer la puissance apparente et le cos(phi) instantanés
        V_eff = calculate_rms(voltage_data)
        I_eff = calculate_rms(current_data)
        
        S_eff[i] = V_eff * I_eff
        cos_phi_inst[i] = P_inst[i] / S_eff[i] if S_eff[i] != 0 else 0

    # Calculer la puissance active totale
    P_inst_triph = np.sum(P_inst)

    # Calculer la puissance apparente totale
    S_eff_triph = np.sqrt(np.sum(np.square(S_eff)))

    # Calculer le facteur de puissance total
    cos_phi_inst_triph = P_inst_triph / S_eff_triph if S_eff_triph != 0 else 0
    
    return P_inst, S_eff, cos_phi_inst, P_inst_triph, S_eff_triph, cos_phi_inst_triph

    
    #return P, S, cos_phi

# Fonction pour traiter une ligne de données
def process_data(row, board_voltage):
    # Calculer les valeurs efficaces (RMS)
    V_eff, I_eff = calculate_effective_values(row)
    
    # Calculer les puissances
    P, S, cos_phi, P_inst_triph, S_eff_triph, cos_phi_inst_triph = calculate_power(row, board_voltage)
    
    # Ajouter les résultats au DataFrame
    for i in range(3):
        row[f'I_eff_{i+1}'] = I_eff[i]
        row[f'V_eff_{i+1}'] = V_eff[i]
        row[f'P_{i+1}'] = P[i]
        row[f'S_{i+1}'] = S[i]
        row[f'cos_phi_{i+1}'] = cos_phi[i]
    row['P_triph'] = P_inst_triph
    row['S_triph'] = S_eff_triph
    row['cos_phi_triph'] = cos_phi_inst_triph
    
    return row
def calculate_accumulated_energy(data):
    # Extract relevant columns
    time = pd.to_datetime(data['Date'])  # Convert 'Date' column to datetime
    P_1 = data['P_1'].astype(float)  # Using S_1 for energy calculation

    # Initialize variables for energy calculation
    EnergyKwhtot = 0
    accumulated_energy = []
    timestamps = []

    # Prepare CSV output file for accumulated energy
    with open('accumulated_energy.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Date', 'Accumulated Energy (kWh)'])

        # Calculate accumulated energy for each new data point
        for k in range(len(data) - 1):
            tim1 = time[k]
            tim2 = time[k + 1]

            # Calculate time difference in seconds
            deltah = (tim2 - tim1).total_seconds
            # Apparent power in VA (volt-ampere)
            s = P_1[k] / 1000
            s = s / 3600

            # Calculate energy in kWh
            EnergyKwh = abs(s)  # This might need adjustment based on your energy calculation logic

            # Update total accumulated energy
            EnergyKwhtot += EnergyKwh

            # Append results to lists for plotting (if needed)
            accumulated_energy.append(EnergyKwhtot)
            timestamps.append(tim2)

            # Write date and accumulated energy to CSV
            csv_writer.writerow([tim2, EnergyKwhtot])

            # Debug prints
            #print(f"Timestamp: {tim2}, Energy (kWh): {EnergyKwh:.10f}, Accumulated Energy (kWh): {EnergyKwhtot:.10f}")

        return EnergyKwhtot


   
# Fonction pour simuler le traitement en temps réel
def simulate_real_time_processing_energy():
    columns = ['Date', 
               'courant1', 'courant2', 'courant3', 
               'tension1', 'tension2', 'tension3', 
               'I_eff_1', 'V_eff_1', 'P_1', 'S_1', 'cos_phi_1', 
               'I_eff_2', 'V_eff_2', 'P_2', 'S_2', 'cos_phi_2', 
               'I_eff_3', 'V_eff_3', 'P_3', 'S_3', 'cos_phi_3',
               'P_triph','S_triph','cos_phi_triph', 
              ]
    
    # Vérifier si le fichier min_data.csv existe
    while not os.path.exists('stockage_data/min_data.csv'):
        time.sleep(1)
    
    # Créer le fichier CSV avec le header uniquement s'il n'existe pas déjà
    if not os.path.exists('stockage_data/energy_data.csv'):
        with open('stockage_data/energy_data.csv', 'w') as f:
            f.write(','.join(columns) + '\n')
    
    # Boucle principale
    while True:
        # Lire la dernière ligne ajoutée au fichier CSV
        new_data = pd.read_csv('stockage_data/min_data.csv').tail(1)
        
        # Traiter la nouvelle ligne
        processed_data = process_data(new_data, board_voltage=5.0)  # Exemple de tension du panneau
        
        # Ajouter les données traitées au fichier data_all.csv
        processed_data.to_csv('stockage_data/energy_data.csv', mode='a', header=False, index=False)
        
        # Attendre un court instant pour que le fichier soit accessible
        time.sleep(3)

        # Read the updated data from CSV to include the latest entry
        data = pd.read_csv('stockage_data/energy_data.csv')

        # Calculate accumulated energy and get the latest total
        latest_accumulated_energy = calculate_accumulated_energy(data)

        # Print the latest accumulated energy (optional)
        print(f"Latest Accumulated Energy: {latest_accumulated_energy:.4f} kWh")

        # Add a delay before reading new data (adjust as needed)
        time.sleep(3)  # Attendre 1 seconde avant la prochaine itération



'''


