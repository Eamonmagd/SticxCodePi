# created by Eamon Magdoubi
# creating class objects
from statistics import mean

class SensorObject:
    #create objects to store data locally
    def __init__(self):
        self.temperatureArray = []
        self.humidityArray = []
        self.temperatureAverage = 0
        self.humidityAverage = 0
        self.axAxis = []
        self.ayAxis = []
        self.azAxis = []
        self.xAverage = 0
        self.yAverage = 0
        self.zAverage = 0
        self.weightArray = []
        self.weightAverage = 0
        #second weight
        self.weightTwoArray = []
        self.weightTwoAverage = 0
        #secondaxis
        self.axAxisTwo = []
        self.ayAxisTwo = []
        self.azAxisTwo = []
        self.xAverageTwo = 0
        self.yAverageTwo = 0
        self.zAverageTwo = 0
    
    def weightIncrement(self, weight,weightTwo):
        self.weightArray.append(weight)
        self.weightTwoArray.append(weightTwo)
        
    def tempHumidIncrement(self, newTemp, newHumid):
        self.temperatureArray.append(newTemp)
        self.humidityArray.append(newHumid)
        
    def accelerationAxis(self, xAxis, yAxis, zAxis):
        self.axAxis.append(xAxis)
        self.ayAxis.append(yAxis)
        self.azAxis.append(zAxis)
    
    def accelerationAxisTwo(self, xAxis, yAxis, zAxis):
        self.axAxisTwo.append(xAxis)
        self.ayAxisTwo.append(yAxis)
        self.azAxisTwo.append(zAxis)
        
    #average from set variables
    def averageCalculator(self):
        self.temperatureAverage = round(mean(self.temperatureArray),2)
        self.humidityAverage = round(mean(self.humidityArray),2)
        self.xAverage = round(mean(self.axAxis),2)
        self.yAverage = round(mean(self.ayAxis),2)
        self.zAverage = round(mean(self.azAxis),2)
        self.weightAverage = round(mean(self.weightArray),2)
        self.weightTwoAverage = round(mean(self.weightTwoArray),2)
        self.xAverageTwo = round(mean(self.axAxisTwo),2)
        self.yAverageTwo = round(mean(self.ayAxisTwo),2)
        self.zAverageTwo = round(mean(self.azAxisTwo),2)
        
    #reset values in a quick finction
    def resetValues(self):
        self.temperatureArray = []
        self.humidityArray = []
        self.temperatureAverage = 0
        self.humidityAverage = 0
        self.axAxis = []
        self.ayAxis = []
        self.azAxis = []
        self.weightArray = []
        self.weightTwoArray = []
        self.xAverage = 0
        self.yAverage = 0
        self.zAverage = 0
        self.weightAverage = 0
        self.weightTwoAverage = 0
        self.axAxisTwo = []
        self.ayAxisTwo = []
        self.azAxisTwo = []
        self.xAverageTwo = 0
        self.yAverageTwo = 0
        self.zAverageTwo = 0