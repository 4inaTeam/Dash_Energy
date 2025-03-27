import numpy as np
import pandas as pd
from datetime import datetime
import time
import os
import csv

# Function to calculate the Root Mean Square (RMS) of a data column
def calculate_rms(data):
    squared_values = data ** 2
    mean_square = squared_values.mean()
    return np.sqrt(mean_square)

# Function to find cycle boundaries based on zero crossings
def find_cycle_bounds(data_column):
    threshold = 0.5  # Threshold for considering a zero crossing
    zero_crossings = np.where(np.diff(np.sign(data_column)))[0]
    
    cycle_starts = []
    cycle_ends = []
    zero_count = 0
    
    for i in range(len(zero_crossings) - 1):
        if data_column[zero_crossings[i]] < threshold and data_column[zero_crossings[i + 1]] > -threshold:
            zero_count += 1
            if zero_count == 3:
                cycle_starts.append(zero_crossings[i])
        elif data_column[zero_crossings[i]] > -threshold and data_column[zero_crossings[i + 1]] < threshold:
            if zero_count == 3:
                cycle_ends.append(zero_crossings[i + 1])
                zero_count = 0
    
    return cycle_starts, cycle_ends


# Function to calculate active power, apparent power, and power factor for a cycle
def calculate_power_cycle(voltage_data, current_data):
    P = (voltage_data * current_data).mean()  # Active power
    V_eff = calculate_rms(voltage_data)       # Effective voltage
    I_eff = calculate_rms(current_data)       # Effective current
    S = V_eff * I_eff                         # Apparent power
    cos_phi = P / S if S != 0 else 0          # Power factor
    
    return P, S, cos_phi

# Function to calculate RMS of voltage and current for a cycle
def calculate_effective_values_cycle(voltage_data, current_data):
    # Use the same cycle boundaries for both voltage and current
    cycle_starts, cycle_ends = find_cycle_bounds(voltage_data)
    
    V_eff = []
    I_eff = []
    
    for start, end in zip(cycle_starts, cycle_ends):
        cycle_data_v = voltage_data[start:end + 1]
        cycle_data_i = current_data[start:end + 1]
        
        V_eff.append(calculate_rms(cycle_data_v))
        I_eff.append(calculate_rms(cycle_data_i))
    
    return V_eff, I_eff

def process_data(data, board_voltage):
    num_phases = 3
    vref = board_voltage / 1024  # Reference voltage of the board
    
    # Initialize an empty list to store processed results
    processed_data = []
    
    # Iterate through each phase (1 to 6) to calculate values for each detected cycle
    for phase in range(1, num_phases + 1):
        voltage_col = f'tension{phase}'
        current_col = f'courant{phase}'
        
        voltage_data = data[voltage_col]
        current_data = data[current_col]
        
        # Calculate effective values (V_eff and I_eff) for each cycle
        V_eff, I_eff = calculate_effective_values_cycle(voltage_data, current_data)
        
        # Find cycle boundaries
        cycle_starts, cycle_ends = find_cycle_bounds(voltage_data)
        
        # Process each detected cycle
        for cycle_idx, (start_idx, end_idx) in enumerate(zip(cycle_starts, cycle_ends)):
            cycle_voltage_data = voltage_data[start_idx:end_idx + 1]
            cycle_current_data = current_data[start_idx:end_idx + 1]
            
            # Check if cycle_idx is within bounds of both V_eff and I_eff
            if cycle_idx < len(V_eff) and cycle_idx < len(I_eff):
                V_eff_cycle = V_eff[cycle_idx]
                I_eff_cycle = I_eff[cycle_idx]
            else:
                V_eff_cycle = 0.0  # Handle out of bounds case
                I_eff_cycle = 0.0  # Handle out of bounds case
            
            # Calculate power values for this cycle
            P_cycle, S_cycle, cos_phi_cycle = calculate_power_cycle(cycle_voltage_data, cycle_current_data)
            
            # Determine the date of the last value in this cycle
            last_date = data.iloc[end_idx]['Date']  # Assuming 'Date' is the column name
            
            # Store results in a dictionary for each cycle
            cycle_result = {
                'Date': last_date,
                'Cycle': cycle_idx + 1,
                f'V_eff_{phase}': V_eff_cycle,
                f'I_eff_{phase}': I_eff_cycle,
                f'P_{phase}': P_cycle,
                f'S_{phase}': S_cycle,
                f'cos_phi_{phase}': cos_phi_cycle,
            }
            
            processed_data.append(cycle_result)
    
    # Convert processed_data list of dictionaries into a DataFrame
    processed_df = pd.DataFrame(processed_data)
    
    # Merge rows with the same date and cycle into a single row
    processed_df = processed_df.groupby(['Date', 'Cycle'], as_index=False).sum()
    
    return processed_df



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
# Function to simulate real-time processing and store data in 'data_all.csv'
def simulate_real_time_processing():
    board_voltage = 5.0  # Example board voltage
    
    while True:
        # Load data from min_data.csv (adjust path as needed)
        try:
            df = pd.read_csv('stockage_data/min_data.csv')
        except FileNotFoundError:
            print("Error: min_data.csv not found.")
            return
        except pd.errors.EmptyDataError:
            print("Error: min_data.csv is empty.")
            return
        
        # Process data to calculate values for each detected cycle
        processed_data = process_data(df, board_voltage)
        
        # Append processed data to data_all.csv
        if not os.path.exists('stockage_data/data_all.csv'):
            processed_data.to_csv('stockage_data/data_all.csv', index=False)
        else:
            processed_data.to_csv('stockage_data/data_all.csv', mode='a', header=False, index=False)
        
        print("Processed and stored data in data_all.csv")



'''
# new clalcul a determiner #
import numpy as np
import pandas as pd
from datetime import datetime
import time
import os
import csv

# Function to calculate the Root Mean Square (RMS) of a data column
def calculate_rms(data):
    squared_values = data ** 2
    mean_square = squared_values.mean()
    return np.sqrt(mean_square)

# Function to find cycle boundaries based on zero crossings
def find_cycle_bounds(data_column):
    threshold = 0.5  # Threshold for considering a zero crossing
    zero_crossings = np.where(np.diff(np.sign(data_column)))[0]
    
    cycle_starts = []
    cycle_ends = []
    zero_count = 0
    
    for i in range(len(zero_crossings) - 1):
        if data_column[zero_crossings[i]] < threshold and data_column[zero_crossings[i + 1]] > -threshold:
            zero_count += 1
            if zero_count == 3:
                cycle_starts.append(zero_crossings[i])
        elif data_column[zero_crossings[i]] > -threshold and data_column[zero_crossings[i + 1]] < threshold:
            if zero_count == 3:
                cycle_ends.append(zero_crossings[i + 1])
                zero_count = 0
    
    return cycle_starts, cycle_ends


# Function to calculate active power, apparent power, and power factor for a cycle
def calculate_power_cycle(voltage_data, current_data):
    P = (voltage_data * current_data).mean()  # Active power
    V_eff = calculate_rms(voltage_data)       # Effective voltage
    I_eff = calculate_rms(current_data)       # Effective current
    S = V_eff * I_eff                         # Apparent power
    cos_phi = P / S if S != 0 else 0          # Power factor
    
    return P, S, cos_phi

# Function to calculate RMS of voltage and current for a cycle
def calculate_effective_values_cycle(voltage_data, current_data):
    # Use the same cycle boundaries for both voltage and current
    cycle_starts, cycle_ends = find_cycle_bounds(voltage_data)
    
    V_eff = []
    I_eff = []
    
    for start, end in zip(cycle_starts, cycle_ends):
        cycle_data_v = voltage_data[start:end + 1]
        cycle_data_i = current_data[start:end + 1]
        
        V_eff.append(calculate_rms(cycle_data_v))
        I_eff.append(calculate_rms(cycle_data_i))
    
    return V_eff, I_eff

def process_data(data, board_voltage):
    num_phases = 3
    vref = board_voltage / 1024  # Reference voltage of the board
    
    # Initialize an empty list to store processed results
    processed_data = []
    
    # Iterate through each phase (1 to 6) to calculate values for each detected cycle
    for phase in range(1, num_phases + 1):
        voltage_col = f'tension{phase}'
        current_col = f'courant{phase}'
        
        voltage_data = data[voltage_col]
        current_data = data[current_col]
        
        # Calculate effective values (V_eff and I_eff) for each cycle
        V_eff, I_eff = calculate_effective_values_cycle(voltage_data, current_data)
        
        # Find cycle boundaries
        cycle_starts, cycle_ends = find_cycle_bounds(voltage_data)
        
        # Process each detected cycle
        for cycle_idx, (start_idx, end_idx) in enumerate(zip(cycle_starts, cycle_ends)):
            cycle_voltage_data = voltage_data[start_idx:end_idx + 1]
            cycle_current_data = current_data[start_idx:end_idx + 1]
            
            # Check if cycle_idx is within bounds of both V_eff and I_eff
            if cycle_idx < len(V_eff) and cycle_idx < len(I_eff):
                V_eff_cycle = V_eff[cycle_idx]
                I_eff_cycle = I_eff[cycle_idx]
            else:
                V_eff_cycle = 0.0  # Handle out of bounds case
                I_eff_cycle = 0.0  # Handle out of bounds case
            
            # Calculate power values for this cycle
            P_cycle, S_cycle, cos_phi_cycle = calculate_power_cycle(cycle_voltage_data, cycle_current_data)
            
            # Determine the date of the last value in this cycle
            last_date = data.iloc[end_idx]['Date']  # Assuming 'Date' is the column name
            
            # Store results in a dictionary for each cycle
            cycle_result = {
                'Date': last_date,
                'Cycle': cycle_idx + 1,
                f'V_eff_{phase}': V_eff_cycle,
                f'I_eff_{phase}': I_eff_cycle,
                f'P_{phase}': P_cycle,
                f'S_{phase}': S_cycle,
                f'cos_phi_{phase}': cos_phi_cycle,
            }
            
            processed_data.append(cycle_result)
    
    # Convert processed_data list of dictionaries into a DataFrame
    processed_df = pd.DataFrame(processed_data)
    
    # Merge rows with the same date and cycle into a single row
    processed_df = processed_df.groupby(['Date', 'Cycle'], as_index=False).sum()
    
    return processed_df



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
# Function to simulate real-time processing and store data in 'data_all.csv'
def simulate_real_time_processing():
    board_voltage = 5.0  # Example board voltage
    
    while True:
        # Load data from min_data.csv (adjust path as needed)
        try:
            df = pd.read_csv('stockage_data/min_data.csv')
        except FileNotFoundError:
            print("Error: min_data.csv not found.")
            return
        except pd.errors.EmptyDataError:
            print("Error: min_data.csv is empty.")
            return
        
        # Process data to calculate values for each detected cycle
        processed_data = process_data(df, board_voltage)
        
        # Append processed data to data_all.csv
        if not os.path.exists('stockage_data/data_all.csv'):
            processed_data.to_csv('stockage_data/data_all.csv', index=False)
        else:
            processed_data.to_csv('stockage_data/data_all.csv', mode='a', header=False, index=False)

        
        print("Processed and stored data in data_all.csv")
        time.sleep(0.1)

'''

       