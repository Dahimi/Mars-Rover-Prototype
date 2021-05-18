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

    def __str__(self):
        return json.dumps({'temperature': self.temperature, 'humidity': self.humidity})


class ProcessThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.ArduinoSerial = ""
        self.isConnected = False

    def sendToArduino(self, data):
        if self.isConnected:
            self.ArduinoSerial.write(data.encode())
            response = self.ArduinoSerial.readline().decode("ascii")
            return response
        return "nothing"

    def run(self):
        try:
            self.ArduinoSerial = serial.Serial('COM9', '115200', timeout=20)
            time.sleep(2)
            print(self.ArduinoSerial.readline().decode("ascii"))
            self.isConnected = True
        except serial.SerialException:
            print('you are not lucky  !!')
        for i in range(1000):
            response = self.sendToArduino("SENSOR")[:-1].strip()
            print("response", response)
            response = response.split(" ")
            print('Random generated number', GraphConsumer.sensorData)
            GraphConsumer.sensorData.temperature = float(response[0])
            GraphConsumer.sensorData.humidity = float(response[1])
            GraphConsumer.numberSec = randint(0, 100)
            time.sleep(0.5)
        GraphConsumer.onProcess = False


class GraphConsumer(AsyncWebsocketConsumer):
    onProcess = False
    numberSec = 0
    sensorData = SensorData()
    processThread = ProcessThread()

    def __init__(self):
        super().__init__()
        if GraphConsumer.onProcess == False:
            GraphConsumer.startProcess()
            GraphConsumer.onProcess = True
        else:
            print('Process already started')

    async def connect(self):
        await self.accept()
        print("connected")

    async def disconnect(self, close_code):
        print("Disconnected")

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        print("data received")
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
        print(event, message)

        if event == 'SENSOR':
            await self.send(str(GraphConsumer.sensorData))
        if event == 'ACTION':
            print('exeecution of ',
                  message['alpha'], ' and ', message['vitesse'])

    @staticmethod
    def startProcess():
        GraphConsumer.processThread.start()
