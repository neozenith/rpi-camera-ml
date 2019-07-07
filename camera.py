from picamera import PiCamera
from time import sleep

cam_settings = dict(resolution=(1024, 768), framerate=15)
prev_settings = dict(alpha=200)

with PiCamera(**cam_settings) as camera:
    camera.rotation = 180
    camera.start_preview(**prev_settings)
    camera.start_recording("/home/pi/Desktop/video.h264")
    sleep(10)
    camera.stop_recording()
    camera.stop_preview()
