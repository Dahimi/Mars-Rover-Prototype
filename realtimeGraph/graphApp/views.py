from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from graphApp.camera import VideoCamera
# Create your views here.

def index(request) : 
    return render(request, 'graphApp/index.html' , context = {'text' : 'hello world'})

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


