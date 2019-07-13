# rpi-camera-ml

Attempting to get the RPI camera module working to work through Machine Vision and OpenCV tutorials

# Getting Started


It seems https://www.piwheels.org has limited prebuilt binary wheels.

See `install-deps.sh`

```bash
. ./install-deps.sh
```

```bash
python3 detect_objects_video.py --config yolov3.cfg --weights yolov3.weights --classes yolov3.txt
python3 detect_objects_video.py --config yolov3-tiny.cfg --weights yolov3-tiny.weights --classes yolov3.txt
```
