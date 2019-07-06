from picamera import PiCamera
from time import sleep
camera = PiCamera()

camera.rotation = 180
camera.resolution = (1024, 768)
camera.framerate = 15
camera.start_preview(alpha=200)
camera.start_recording('/home/pi/Desktop/video.h264')
sleep(10)
camera.stop_recording()
camera.stop_preview()
