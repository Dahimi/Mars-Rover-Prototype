from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from graphApp.camera import VideoCamera
from django.http import JsonResponse
import json
#from websocket import create_connection
import websockets
import asyncio
# Create your views here.


def index(request):
    lat, lon = 32.21821, -7.93565
    mpbox_access_token = 'pk.eyJ1Ijoic291ZmlhbmVkYWhpbWkiLCJhIjoiY2tucTJxZjh4MGF0eDJucGZqdGd2dnQzZiJ9.gR_gX_q39d2Qp2CUK_soIw'
    return render(request, 'index.html', context={'text': 'hello world', 'accessToken': mpbox_access_token, 'lon': lon, 'lat': lat})


def stream(request):
    return render(request, 'graphApp/home.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
    respone = gen(VideoCamera())
    print(type(respone))
    return StreamingHttpResponse(respone,
                                 content_type='multipart/x-mixed-replace; boundary=frame')


async def command(request):

    print("we got new command")
    message = str(request.GET['command'])
    async with websockets.connect("ws://localhost:8000/ws/graph/") as ws:
        await ws.send(json.dumps({"event": "COMMAND", "message": message}))

    return JsonResponse({"response": "ok"}, status=200)
