from picamera import PiCamera
from time import sleep, time
import sys
import argparse
import cv2

VALID_MODES = ["photo", "video"]


def video(camera, filename="/home/pi/Desktop/video.h264", duration=10):
    camera.start_recording(filename)
    sleep(duration)
    camera.stop_recording()
    return filename


def photo(camera, filename="/home/pi/Desktop/photo.jpg"):
    camera.capture(filename)
    return filename


def acquire(mode="video"):
    cam_settings = dict(resolution=(1024, 768), framerate=15)
    prev_settings = dict(alpha=200, fullscreen=False, window=(0, 0, 1024, 768))
    camera_function = dict(video=video, photo=photo)
    file_ext = dict(video="h264", photo="jpg")

    filename = f"/home/pi/Desktop/{mode}-{time()}.{file_ext[mode]}"

    with PiCamera(**cam_settings) as camera:
        camera.rotation = 90

        with camera.start_preview(**prev_settings) as preview:
            sleep(2)

            output = camera_function[mode](camera, filename=filename)
    return output


def cli_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to input image")
    ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
    ap.add_argument("-l", "--labels", required=True, help="path to ImageNet labels (i.e., syn-sets)")
    args = vars(ap.parse_args())
    return args


def main():
    mode = "photo"
    # args = cli_args()

    output = acquire(mode)

    print(f"Saved output to: {output}")


if __name__ == "__main__":
    main()
