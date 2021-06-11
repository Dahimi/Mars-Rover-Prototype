from channels.generic.websocket import AsyncWebsocketConsumer
import json
from random import randint
from asyncio import sleep
import time
import threading
import serial


class SensorData():
    def __init__(self):
        self.temperature = 0
        self.humidity = 0
        self.distance = 0

    def __str__(self):
        return json.dumps({'temperature': self.temperature, 'humidity': self.humidity, 'distance': self.distance})


class GraphConsumer(AsyncWebsocketConsumer):
    onProcess = False
    numberSec = 0
    sensorData = SensorData()
    ArduinoSerial = ""
    isConnected = False

    def __init__(self):
        super().__init__()
        if GraphConsumer.onProcess == False:
            GraphConsumer.startProcess()
            GraphConsumer.onProcess = True
        else:
            print('Process already started')

    async def connect(self):
        sleep(1)
        await self.accept()
        print("connected")

    async def disconnect(self, close_code):
        print("Disconnected")

    def sendToArduino(self, data):
        if GraphConsumer.isConnected:
            GraphConsumer.ArduinoSerial.write(data.encode())
            response = GraphConsumer.ArduinoSerial.readline().decode("ascii")
            return response
        return "nothing"

    async def readSensor(self):
        response = self.sendToArduino("SENSOR")[:-1].strip()
        print(" expected", response)
        response = response.split(" ")
        try:
            GraphConsumer.sensorData.temperature = float(response[0])
            GraphConsumer.sensorData.humidity = float(response[1])
            GraphConsumer.sensorData.distance = float(response[2])
        except:
            print("error")

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
        print(event, message)

        if event == 'SENSOR':
            await self.readSensor()
            await self.send(str(GraphConsumer.sensorData))
        if event == 'ACTION':
            print('exeecution of ',
                  message['alpha'], ' and ', message['vitesse'])
            command = "ACTION " + \
                str(message['alpha']) + " " + str(message['vitesse'])
            response = self.sendToArduino(command)[:-1].strip()
            print("after command", response)

    @staticmethod
    def startProcess():
        try:
            GraphConsumer.ArduinoSerial = serial.Serial(
                'COM4', '57600', timeout=20)
            time.sleep(2)
            print(GraphConsumer.ArduinoSerial.readline().decode("ascii"))
            GraphConsumer.isConnected = True
        except serial.SerialException:
            print('you are not lucky  !!')
