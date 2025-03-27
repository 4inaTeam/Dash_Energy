import serial
import csv
import time
print(serial.__file__)
# Ouvre le port série (remplace 'COMx' par le bon port, ex: 'COM5' sous Windows ou '/dev/ttyUSB0' sous Linux)
ser = serial.Serial(port='COM5', baudrate=9600, timeout=1)
# Nom du fichier CSV
csv_filename = "donnees.csv"
# Vérifie si le fichier existe déjà ou non
try:
    with open(csv_filename, "x", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Donnée reçue"])  # Écriture de l'en-tête
except FileExistsError:
    pass  # Le fichier existe déjà, donc on ne réécrit pas l'en-tête
try:
    with open(csv_filename, "a", newline="") as f:
        writer = csv.writer(f)
        while True:
            data = ser.readline().decode().strip()
            if data:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"{timestamp} - Reçu : {data}")  # Affichage
                writer.writerow([timestamp, data])  # Sauvegarde dans le fichier CSV
                f.flush()  # Force l'écriture immédiate dans le fichier
except KeyboardInterrupt:
    print("Arrêt du programme.")
finally:
    ser.close()