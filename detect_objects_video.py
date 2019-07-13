from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2


# https://towardsdatascience.com/yolo-object-detection-with-opencv-and-python-21e50ac599e9


def get_output_layers(net):

    layer_names = net.getLayerNames()

    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


# function to draw bounding box on the detected object with class name
def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required=True, help="path to yolo config file")
ap.add_argument(
    "-w", "--weights", required=True, help="path to yolo pre-trained weights"
)
ap.add_argument(
    "-cl", "--classes", required=True, help="path to text file containing class names"
)
args = vars(ap.parse_args())

print(args)

# read class names from text file
classes = None
with open(args["classes"], "r") as f:
    classes = [line.strip() for line in f.readlines()]

# generate different colors for different classes
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

print("[INFO] loading model...")
# read pre-trained model and config file
net = cv2.dnn.readNet(args["weights"], args["config"])


# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    start = time.time()
    scale_width = 416
    frame = vs.read()
    print(f"RAW: {time.time() - start}")
    frame = imutils.resize(frame, width=scale_width)

    # grab the frame dimensions and convert it to a blob
    (_h, _w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(
        frame, 1.0, (scale_width, scale_width), (104.0, 177.0, 123.0)
    )

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)

    print(f"SCALED: {time.time() - start}")
    outs = net.forward(get_output_layers(net))

    print(f"NET: {time.time() - start}")
    # initialization
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    # for each detetion from each output layer
    # get the confidence, class id, bounding box params
    # and ignore weak detections (confidence < 0.5)
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and all([x < 2.0 for x in detection[:4]]):

                #  print(detection[:4])
                center_x = int(detection[0] * _w)
                center_y = int(detection[1] * _h)
                w = int(detection[2] * _w)
                h = int(detection[3] * _h)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
                # draw_bounding_box(frame, class_id, float(confidence), round(x), round(y), round(x + w), round(y + h))

    print(f"BOXES: {time.time() - start}")
    #  print(boxes)
    #  print(confidences)
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    # go through the detections remaining
    # after nms and draw bounding box
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        draw_bounding_box(
            frame,
            class_ids[i],
            confidences[i],
            round(x),
            round(y),
            round(x + w),
            round(y + h),
        )

    print(f"BOUND: {time.time() - start}")
    # time.sleep(5.0)
    # show the output frame
    cv2.imshow("Frame", frame)
    print(f"FRAME: {time.time() - start}")
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
