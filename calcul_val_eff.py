import os
import numpy as np
import pandas as pd
import csv
import time
import threading

# Function to calculate the Root Mean Square (RMS) of a data column
def calculate_rms(data):
    squared_values = data ** 2
    mean_square = squared_values.mean()
    return np.sqrt(mean_square)

# Function to calculate active power, apparent power, and power factor for a cycle
def calculate_power_cycle(voltage_data, current_data):
    P = (voltage_data * current_data).mean()  # Active power
    V_eff = calculate_rms(voltage_data)       # Effective voltage
    I_eff = calculate_rms(current_data)       # Effective current
    S = V_eff * I_eff                         # Apparent power
    Q = np.sqrt(S**2 - P**2) if S**2 >= P**2 else 0               # v a r
    cos_phi = P / S if S != 0 else 0          # Power factor
    return P, S, Q, cos_phi

# Function to calculate effective values and power metrics every second with exactly 900 data points
# def calculate_effective_values_per_second(data, window_size=900):
#     results = []
#     data['Date'] = pd.to_datetime(data['Date'])
#     data.set_index('Date', inplace=True)
#     grouped = data.resample('S').apply(lambda x: len(x))
#     grouped = data.resample('s').apply(lambda x: len(x))
#     valid_seconds = grouped[grouped == window_size].index

#     for timestamp in valid_seconds:
#         second_data = data.loc[timestamp:timestamp + pd.Timedelta(seconds=1) - pd.Timedelta(milliseconds=1)]
#         result = {'Date': timestamp}
#         for phase in range(1, 4):  # pour le new factory changer 7 
#             voltage_col = f'tension{phase}'
#             current_col = f'courant{phase}'
#             if voltage_col in second_data.columns and current_col in second_data.columns:
#                 voltage_data = second_data[voltage_col]
#                 current_data = second_data[current_col]
#                 V_eff = calculate_rms(voltage_data)
#                 I_eff = calculate_rms(current_data)
#                 P, S, Q, cos_phi = calculate_power_cycle(voltage_data, current_data)
#                 result[f'V_eff_{phase}'] = V_eff
#                 result[f'I_eff_{phase}'] = I_eff
#                 result[f'P_{phase}'] = P
#                 result[f'S_{phase}'] = S
#                 result[f'Q_{phase}'] = Q
#                 result[f'cos_phi_{phase}'] = cos_phi
#         results.append(result)
#     results_df = pd.DataFrame(results)
#     return results_df
def calculate_effective_values_per_second(data, window_size=900):
    results = []
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    
    # Group by minute
    grouped = data.resample('1min').apply(lambda x: len(x))  # 'T' is the frequency code for minutes
    valid_minutes = grouped[grouped == window_size].index  # Ensure the expected number of samples per minute

    for timestamp in valid_minutes:
        # Get the data for the entire minute
        minute_data = data.loc[timestamp:timestamp + pd.Timedelta(minutes=1) - pd.Timedelta(milliseconds=1)]
        result = {'Date': timestamp}
        
        for phase in range(1, 4):  # Loop through the phases
            voltage_col = f'tension{phase}'
            current_col = f'courant{phase}'
            
            if voltage_col in minute_data.columns and current_col in minute_data.columns:
                voltage_data = minute_data[voltage_col]
                current_data = minute_data[current_col]
                
                V_eff = calculate_rms(voltage_data)
                I_eff = calculate_rms(current_data)
                P, S, Q, cos_phi = calculate_power_cycle(voltage_data, current_data)
                
                result[f'V_eff_{phase}'] = V_eff
                result[f'I_eff_{phase}'] = I_eff
                result[f'P_{phase}'] = P
                result[f'S_{phase}'] = S
                result[f'Q_{phase}'] = Q
                result[f'cos_phi_{phase}'] = cos_phi
        
        results.append(result)
    
    results_df = pd.DataFrame(results)
    return results_df

def calculate_accumulated_energy(data):
    # Convert 'Date' column to datetime format
    time = pd.to_datetime(data['Date'])
    # print("data" ,data )
    # Initialize variables for accumulated energy calculations
    EnergyKwhtot_1 = 0
    EnergyKwhtot_2 = 0
    EnergyKwhtot_3 = 0
    accumulated_energy_1 = []
    accumulated_energy_2 = []
    accumulated_energy_3 = []
    timestamps = []

    with open('stockage_data/accumulated_energy_per_phase_1.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Date', 'Accumulated Energy Phase 1 (kWh)', 'Accumulated Energy Phase 2 (kWh)', 'Accumulated Energy Phase 3 (kWh)'])

        # Iterate through each row in the data
        for k in range(len(data) - 1):
            tim1 = time[k]
            tim2 = time[k + 1]
            
            # Calculate time difference in seconds
            deltah = (tim2 - tim1).total_seconds()
            
            # Get power values for each phase, handle missing values by using 0 if not available
            P_1 = data['P_1'].astype(float).iloc[k] if pd.notna(data['P_1'].iloc[k]) else 0
            P_2 = data['P_2'].astype(float).iloc[k] if pd.notna(data['P_2'].iloc[k]) else 0
            P_3 = data['P_3'].astype(float).iloc[k] if pd.notna(data['P_3'].iloc[k]) else 0
            
            # Convert power to energy (kWh) over the time interval
            EnergyKwh_1 = abs(P_1 / 1000 * (deltah / 3600))
            EnergyKwh_2 = abs(P_2 / 1000 * (deltah / 3600))
            EnergyKwh_3 = abs(P_3 / 1000 * (deltah / 3600))
            
            # Update accumulated energy
            EnergyKwhtot_1 += EnergyKwh_1
            EnergyKwhtot_2 += EnergyKwh_2
            EnergyKwhtot_3 += EnergyKwh_3
            
            # Append accumulated energy and timestamps
            accumulated_energy_1.append(EnergyKwhtot_1)
            accumulated_energy_2.append(EnergyKwhtot_2)
            accumulated_energy_3.append(EnergyKwhtot_3)
            timestamps.append(tim2)
            # Write to CSV if there is valid accumulated energy
            if any([EnergyKwhtot_1, EnergyKwhtot_2, EnergyKwhtot_3]):
                csv_writer.writerow([tim2, EnergyKwhtot_1, EnergyKwhtot_2, EnergyKwhtot_3])
    return EnergyKwhtot_1, EnergyKwhtot_2, EnergyKwhtot_3
# Function to process and store data
def process_and_store_data():
    # input_file = 'clean.csv'
    input_file = 'stockage_data/min_data.csv'
    # input_file = 'Dates_data/sec_data_moy.csv'
    processed_file = 'stockage_data/data_efficace.csv'
    while not os.path.exists(input_file):
        print(f"{input_file} does not exist. Waiting...")
        time.sleep(2)  # Wait for 2 seconds before checking again
    # Load data from the CSV file
    data = pd.read_csv(input_file)
    # Calculate effective values and power metrics
    processed_data = calculate_effective_values_per_second(data)
    processed_data.to_csv(processed_file, index=False)
    # print(f"Data written to {processed_file}",processed_data)
    # Calculate and save accumulated energy
    calculate_accumulated_energy(processed_data)






'''
import numpy as np
import pandas as pd
import csv
import os

# Function to calculate the Root Mean Square (RMS) of a data column
def calculate_rms(data):
    squared_values = data ** 2
    mean_square = squared_values.mean()
    return np.sqrt(mean_square)

# Function to calculate active power, apparent power, and power factor for a cycle
def calculate_power_cycle(voltage_data, current_data):
    P = (voltage_data * current_data).mean()  # Active power
    V_eff = calculate_rms(voltage_data)       # Effective voltage
    I_eff = calculate_rms(current_data)       # Effective current
    S = V_eff * I_eff                         # Apparent power
    cos_phi = P / S if S != 0 else 0          # Power factor
    
    return P, S, cos_phi

# Function to calculate effective values and power metrics every second with exactly 900 data points
def calculate_effective_values_per_second(data, window_size=900):
    results = []
    
    # Ensure 'Date' column is in datetime format
    data['Date'] = pd.to_datetime(data['Date'])
    
    # Set 'Date' column as index for easier resampling
    data.set_index('Date', inplace=True)

    # Group by second and check if there are exactly 900 rows
    grouped = data.resample('S').apply(lambda x: len(x))

    # Filter to keep only those seconds with exactly 900 data points
    valid_seconds = grouped[grouped == window_size].index

    for timestamp in valid_seconds:
        # Extract the data for the current second
        second_data = data.loc[timestamp:timestamp + pd.Timedelta(seconds=1) - pd.Timedelta(milliseconds=1)]
        
        # Initialize results for this timestamp
        result = {'Date': timestamp}
        
        for phase in range(1, 4):
            voltage_col = f'tension{phase}'
            current_col = f'courant{phase}'
            
            # Calculate effective values
            if voltage_col in second_data.columns and current_col in second_data.columns:
                voltage_data = second_data[voltage_col]
                current_data = second_data[current_col]
                
                V_eff = calculate_rms(voltage_data)
                I_eff = calculate_rms(current_data)
                
                # Calculate power metrics
                P, S, cos_phi = calculate_power_cycle(voltage_data, current_data)
                
                result[f'V_eff{phase}'] = V_eff
                result[f'I_eff{phase}'] = I_eff
                result[f'P_{phase}'] = P
                result[f'S_{phase}'] = S
                result[f'cos_phi_{phase}'] = cos_phi
        
        results.append(result)
    
    # Convert results list of dictionaries into a DataFrame
    results_df = pd.DataFrame(results)
    
    return results_df

# Function to calculate accumulated energy for each phase
def calculate_accumulated_energy(data):
    # Extract relevant columns
    time = pd.to_datetime(data['Date'])  # Convert 'Date' column to datetime

    # Initialize variables for energy calculation
    EnergyKwhtot_1 = 0
    EnergyKwhtot_2 = 0
    EnergyKwhtot_3 = 0
    accumulated_energy_1 = []
    accumulated_energy_2 = []
    accumulated_energy_3 = []
    timestamps = []

    # Prepare CSV output file for accumulated energy
    with open('accumulated_energy_per_phase.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Date', 'Accumulated Energy Phase 1 (kWh)', 'Accumulated Energy Phase 2 (kWh)', 'Accumulated Energy Phase 3 (kWh)'])

        # Calculate accumulated energy for each new data point
        for k in range(len(data) - 1):
            tim1 = time[k]
            tim2 = time[k + 1]

            # Calculate time difference in seconds
            deltah = (tim2 - tim1).total_seconds()

            # Power for each phase
            P_1 = data['P_1'].astype(float)
            P_2 = data['P_2'].astype(float)
            P_3 = data['P_3'].astype(float)

            # Apparent power in VA (volt-ampere)
            s1 = P_1[k] / 1000
            s2 = P_2[k] / 1000
            s3 = P_3[k] / 1000

            s1 = s1 / 3600
            s2 = s2 / 3600
            s3 = s3 / 3600

            # Calculate energy in kWh for each phase
            EnergyKwh_1 = abs(s1)
            EnergyKwh_2 = abs(s2)
            EnergyKwh_3 = abs(s3)

            # Update total accumulated energy for each phase
            EnergyKwhtot_1 += EnergyKwh_1
            EnergyKwhtot_2 += EnergyKwh_2
            EnergyKwhtot_3 += EnergyKwh_3

            # Append results to lists for plotting (if needed)
            accumulated_energy_1.append(EnergyKwhtot_1)
            accumulated_energy_2.append(EnergyKwhtot_2)
            accumulated_energy_3.append(EnergyKwhtot_3)
            timestamps.append(tim2)

            # Write date and accumulated energy to CSV
            csv_writer.writerow([tim2, EnergyKwhtot_1, EnergyKwhtot_2, EnergyKwhtot_3])
        
        return EnergyKwhtot_1, EnergyKwhtot_2, EnergyKwhtot_3

# Main function to process data and store results
def main():
    input_file = 'stockage_data/min_data.csv'
    processed_file = 'stockage_data/data_efficace.csv'

    # Load data from the CSV file
    data = pd.read_csv(input_file)
    
    # Calculate effective values and power metrics
    processed_data = calculate_effective_values_per_second(data)
    processed_data.to_csv(processed_file, index=False)
    
    # Calculate and save accumulated energy
    calculate_accumulated_energy(processed_data)

    print("Processed and stored data in data_efficace.csv and accumulated_energy_per_phase.csv")

if __name__ == "__main__":
    main()

'''