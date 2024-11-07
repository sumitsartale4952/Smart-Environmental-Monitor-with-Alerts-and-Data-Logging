from dfadc import *  # DFRobot ADC library
from lcddf import *  # LCD library
import time
import csv
from datetime import datetime

# Initialize the board
board_detect()
while board.begin() != board.STA_OK:
    print_board_status()
    print("Board initialization failed")
    time.sleep(2)
print("Board initialization successful")
board.set_adc_enable()

# Set up the CSV log file
log_file = "temp_humidity_log.csv"
with open(log_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Temperature (C)", "Humidity (%)"])  # Header

# Thresholds for alerts
TEMP_THRESHOLD = 30.0  # Celsius
HUMIDITY_THRESHOLD = 70.0  # Percentage

while True:
    # Read and calculate temperature
    val_temp = board.get_adc_value(board.A0)
    temperature = (val_temp / 4096) * 3300 / 10.24
    temp_display = f"Temp: {temperature:.1f}C ☀️" if temperature > TEMP_THRESHOLD else f"Temp: {temperature:.1f}C"
    
    # Display temperature with background color based on threshold
    setText(temp_display)
    setRGB(255, 100, 100) if temperature > TEMP_THRESHOLD else setRGB(0, 128, 255)
    time.sleep(2)

    # Read and calculate humidity
    val_humid = board.get_adc_value(board.A1)
    humidity = (val_humid / 4096) * 100
    humid_display = f"Humidity: {humidity:.1f}% 💧" if humidity > HUMIDITY_THRESHOLD else f"Humidity: {humidity:.1f}%"
    
    # Display humidity with background color based on threshold
    setText(humid_display)
    setRGB(255, 100, 100) if humidity > HUMIDITY_THRESHOLD else setRGB(0, 255, 0)
    time.sleep(2)

    # Flash effect for high values
    if temperature > TEMP_THRESHOLD or humidity > HUMIDITY_THRESHOLD:
        for _ in range(3):
            setRGB(255, 0, 0)  # Flash red for alert
            time.sleep(0.3)
            setRGB(255, 100, 100)  # Dim flash
            time.sleep(0.3)
    
    # Log data to CSV file
    with open(log_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), round(temperature, 1), round(humidity, 1)])

    print(f"Logged: {temp_display}, {humid_display}")