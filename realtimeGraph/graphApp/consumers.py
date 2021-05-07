from channels.generic.websocket import AsyncWebsocketConsumer
import json 
from random import randint
from asyncio import sleep
import time
import threading
import serial
class GraphConsumer(AsyncWebsocketConsumer):
    onProcess = False 
    numberSec = 0
    def __init__(self):
        super().__init__()
        if GraphConsumer.onProcess == False :
            GraphConsumer.startProcess()
            GraphConsumer.onProcess =True
        else :
            print('Process already started')
    async def connect(self):
        await self.accept()
        print("connected")
        for i in range(1000):
            
            await self.send(json.dumps({'value' :GraphConsumer.numberSec }))
            await sleep(1)
    async def disconnect(self, close_code):
        print("Disconnected")
        
    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
        if event == 'MOVE':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                "event": "MOVE"
            })

        if event == 'START':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "START"
            })

        if event == 'END':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "END"
            })
    @staticmethod
    def startProcess():
        ProcessThread().start()
        

class ProcessThread(threading.Thread):

    def __init__(self ):
            threading.Thread.__init__(self)
            self.daemon = True
    def run(self):

        print('call')
        try :
            self.ArduinoSerial = serial.Serial('COM16', '115200', timeout=20)
            time.sleep(2)
            print(self.ArduinoSerial.readline().decode("ascii"))
            
        except serial.SerialException :
            print('you are not lucky !!')
        for i in range(100):
            print('Random generated number' , GraphConsumer.numberSec )
            GraphConsumer.numberSec = randint(0,20)
            time.sleep(1)
        GraphConsumer.onProcess = False