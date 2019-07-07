from picamera import PiCamera
from time import sleep, time
import sys


def video(camera, filename="/home/pi/Desktop/video.h264", duration=10):
    camera.start_recording(filename)
    sleep(duration)
    camera.stop_recording()
    return filename


def photo(camera, filename="/home/pi/Desktop/photo.jpg"):
    camera.capture(filename)
    return filename


def main():

    cam_settings = dict(resolution=(1024, 768), framerate=15)
    prev_settings = dict(alpha=200)

    mode = "video"
    if len(sys.argv) > 1 and sys.argv[1] in cam_settings.keys():
        mode = sys.argv[1]

    camera_function = dict(video=video, photo=photo)
    file_ext = dict(video="h264", photo="jpg")
    filename = f"/home/pi/Desktop/{mode}-{time()}.{file_ext[mode]}"

    with PiCamera(**cam_settings) as camera:
        camera.rotation = 180
        camera.start_preview(**prev_settings)
        sleep(2)

        output = camera_function[mode](camera, filename=filename)
        print(f"Saved output to: {output}")
        camera.stop_preview()


if __name__ == "__main__":
    main()
