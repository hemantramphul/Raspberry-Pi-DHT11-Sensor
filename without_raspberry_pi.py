"""
Assignment Title:   Save the data from the Raspberry Pi sensor in a database and then create a dashboard to make it an insight of your data.
Purpose:            To create a dashboard with all collected data.
Language:           Implementation in Python

Author:             Hemant Ramphul
Github:             https://github.com/hemantramphul/Raspberry-Pi-DHT11-Sensor
Date:               31 October 2022

Université des Mascareignes (UdM)
Faculty of Information and Communication Technology
Master Artificial Intelligence and Robotics
Official Website: https://udm.ac.mu
"""

import urllib.request as request
import time
import random as rand
import pyodbc as db

# Delay in-between sensor readings, in seconds.
DHT_READ_TIMEOUT = 15

# For local machine database use: MSSQL
# DB_CONNECTION = db.connect('Driver={SQL Server};'
#                         'Server=.\SQLEXPRESS;'
#                         'Database=IoT_UDM_Database;'
#                         'Trusted_Connection=yes;')

# For cloud database use: MSSQL Azure on portal.azure.com
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
DB_CONNECTION = db.connect('Driver={SQL Server};'
                           'Server=iot-hramphul.database.windows.net;'
                           'Database=IoT_UDM_Database;'
                           'Uid=hramphul;Pwd={your_password};'
                           'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')


# Define a function that can read cloud database data from any table
# @Table as parameter: HumitureSensor
def readDataFromDatabase(_table):
    # Map to ODBC
    cursor = DB_CONNECTION.cursor()
    # Query to execute
    query = 'SELECT * FROM {}'.format(_table)
    # Execute the query
    cursor.execute(query)

    # Loop over each record found in the table
    for i in cursor:
        # Display each row of data in console
        print(i)


# Define a function that saves data to the table
# @Temperature as parameter: _temperature
# @Humidity as parameter: _humidity
def saveData(_temperature, _humidity):
    # Map to ODBC
    cursor = DB_CONNECTION.cursor()
    # Query to execute
    cursor.execute('INSERT INTO HumitureSensor (Temperature, Humidity) VALUES (?, ?)', (_temperature, _humidity))
    # Execute the requested query
    DB_CONNECTION.commit()


# Define a function to push data collection/generation to Thingspeak.com
# @Temperature as parameter: _temperature
# @Humidity as parameter: _humidity
def thingspeak(_temperature, _humidity):
    # Enter your API key here
    key = '{your_write_key}'
    # URL where data will be send after generated, don't change it
    api_url = 'https://api.thingspeak.com/update?api_key={}&field1={}&field2={}'.format(key, _temperature, _humidity)
    # Sending data to Thingspeak
    request.urlopen(api_url)


# Define a function that will post [Temperature] and [Humidity] on Thingspeak server every 15 Seconds
def start():
    # Generate a random temperature
    temperature = rand.randint(-40, 80)
    # Generate a random humidity
    humidity = rand.randint(0, 100)

    # Display generated data in the console
    print('Temperature = {0:0.1f}℃ Humidity = {1:0.1f}%'.format(temperature, humidity))
    # Sending data to Thingspeak
    thingspeak(temperature, humidity)
    # Insert generated data to cloud database
    saveData(temperature, humidity)


if __name__ == '__main__':
    while True:
        # Start the main function
        start()
        # Delay
        time.sleep(DHT_READ_TIMEOUT)
