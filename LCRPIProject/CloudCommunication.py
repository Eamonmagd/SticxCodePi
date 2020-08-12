# created by Eamon Magdoubi
#communication to the external database
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore
import datetime
import csv
import os
    
class CloudCommunication():
    def __init__(self):
        
        cred = credentials.Certificate('/home/pi/Desktop/LCRPIProject/pi-iot-project-240909-firebase-adminsdk-n3mcl-a44a263deb.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.entries = os.listdir('/media/pi/') if  len(os.listdir('/media/pi/')) else [];
        if len(self.entries) > 0:
            self.entries = '/media/pi/'+ self.entries[0] + '/backup.csv'
            try:
                with open(self.entries, 'rb') as csvfile:
                    sniffer = csv.Sniffer()
                    has_header = sniffer.has_header('Temperature')
                    #print(has_header)
                    if has_header == False:
                        thewriter.writeheader()
            except:
                with open(self.entries, 'a', newline='') as f:
                    fieldnames = ['Temperature','Humidity', 'X Axis', 'Y Axis', 'Z Axis', 'Force','Force 2', 'X Axis 2', 'Y Axis 2', 'Z Axis 2', 'Date Time']
                    thewriter = csv.DictWriter(f, fieldnames=fieldnames)
                    thewriter.writeheader()
        else:
            self.entries = ''
            
    #adding new dataset
    def addValue(self, temp, humid, xaxis, yaxis, zaxis, weight, weightTwo, xaxisTwo, yaxisTwo, zaxisTwo):
    # TE = Temperature
    # H = Humidity
    # V = VibrationCount
    # Til = Tilting Count
    # S =  Sound Sensor
    # XA = X Axis Acceleration
    # YA = Y Axis Acceleration
    # ZA = Z Axis Acceleration
    # F = Weight Force Average
    # F2 = Weight Force 2 Average
    # TF = Time Frame
    # XA2 = X Axis Acceleration 2
    # YA2 = Y Axis Acceleration 2
    # ZA2 = Z Axis Acceleration 2
    
        #here is the datetime and the format is %c and can be changed here for the csv
        #date is local so change the time zone on the pi if needed
        dateTime = datetime.datetime.now().strftime("%c")
        self.entries = '/media/pi/'+ os.listdir('/media/pi/')[0] + '/backup.csv' if  len(os.listdir('/media/pi/')) else '';
        if len(self.entries) >0:    
            with open(self.entries, 'a', newline='') as f:
                fieldnames = ['Temperature','Humidity', 'X Axis', 'Y Axis', 'Z Axis', 'Force', 'Force 2', 'X Axis 2', 'Y Axis 2','Z Axis 2','Date Time']
                thewriter = csv.DictWriter(f, fieldnames=fieldnames)
                #thewriter.writeheader()
                thewriter.writerow({'Temperature': temp, 'Humidity': humid,'X Axis': xaxis,'Y Axis': yaxis,'Z Axis': zaxis, 'Force': weight ,'Force 2': weightTwo,'X Axis 2': xaxisTwo,'Y Axis 2': yaxisTwo,'Z Axis 2': zaxisTwo,'Date Time': dateTime})
                
        doc_ref = self.db.collection(u'sensorData').add(
            {'Te' : temp,
             'H' : humid,
             'TF': dateTime,
             'XA':xaxis,
             'YA':yaxis,
             'ZA':zaxis,
             'F': weight,
             'F2': weightTwo,
             'XA2':xaxisTwo,
             'YA2':yaxisTwo,
             'ZA2': zaxisTwo})
        
    #if data reads are required in future development for the pi to interfact with the db   
    def readValue():
        sensor_ref = self.db.collection(u'sensorData')
        docs = user_ref.get()
        return docs
    
    
        
