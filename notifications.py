# Initialize for 3 sensors
import time

import pandas as pd


notifications = []

def monitor_csv_files():
    global notifications
    while True:
        try:
            # Load the latest data from CSV file
            data = pd.read_csv('predictions_files/data_courant_tension_predites.csv').tail(1)
            code_M1 = data['code_M1'].values[0]

            # Send code_M1 as notification
            message = f'Code received: {code_M1}'
            if not any(notification['message'] == message for notification in notifications):
                notifications.append({
                    'code': code_M1,
                    'message': message
                })

            time.sleep(1)
        except Exception as e:
           
            time.sleep(1)
'''
latest_received_values = {i: None for i in range(1, 4)}
notifications = []

def monitor_csv_files():
    global latest_received_values, notifications
    while True:
        try:
            # Load the latest data from CSV files
            data = pd.read_csv('files_csv/data_courant_tension.csv').tail(1)
            
            for i in range(1, 4):
                courant = data[f'courant{i}'].values[0]
                tension = data[f'tension{i}'].values[0]
                
                latest_received_values[i] = {
                    'courant': courant,
                    'tension': tension,
                    'message': None
                }

                # Check for current anomalies
                if courant > 4 or courant < -4:
                    message = 'Anomaly in current'
                    if not any(notification['message'] == message for notification in notifications):
                        notifications.append({
                            'courant': courant,
                            'tension': tension,
                            'message': message
                        })

                # Check for tension anomalies
                if tension > 300 or tension < -300:
                    message = 'Anomaly in tension'
                    if not any(notification['message'] == message for notification in notifications):
                        notifications.append({
                            'courant': courant,
                            'tension': tension,
                            'message': message
                        })

            time.sleep(1)
        except Exception as e:
            print(f"Error reading CSV files: {e}")
            time.sleep(1)

'''