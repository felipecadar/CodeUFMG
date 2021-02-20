import cv2
import argparse
import numpy as np
import os
import glob

class BallTracker:
    def __init__(self, yolo_cfg, yolo_classes, yolo_weights, conf_threshold, nms_threshold):
        self.classes = None
        with open(yolo_classes, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.COLORS = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.net = cv2.dnn.readNet(yolo_weights, yolo_cfg)

        self.conf_threshold = conf_threshold
        self.nms_threshold = nms_threshold

    def get_output_layers(self):
        
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        return output_layers


    def draw_prediction(self, img, class_id, x, y, x_plus_w, y_plus_h):
        label = str(self.classes[class_id])
        color = self.COLORS[class_id]
        cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
        cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def predict(self, image, draw=False):
        Width = image.shape[1]
        Height = image.shape[0]
        scale = 0.00392

        blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.get_output_layers())

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.conf_threshold and class_id == 32:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])


        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.conf_threshold, self.nms_threshold)
        if draw:
            for i in indices:
                i = i[0]
                box = boxes[i]
                x = box[0]
                y = box[1]
                w = box[2]
                h = box[3]
                self.draw_prediction(image, class_ids[i], round(x), round(y), round(x+w), round(y+h))

        return [boxes, confidences, class_ids]

def parseArgs():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', required=True,
                    help = 'path to input image, video or directory with images')
    ap.add_argument('-c', '--config', required=False, default="yolo/yolov3.cfg",
                    help = 'path to yolo config file')
    ap.add_argument('-w', '--weights', required=False, default="yolo/yolov3.weights",
                    help = 'path to yolo pre-trained weights')
    ap.add_argument('-cl', '--classes', required=False, default="yolo/yolov3.txt",
                    help = 'path to text file containing class names')
    ap.add_argument('-t', '--confidence-threshold', required=False, default=0.5, type=float,
                    help = 'classifier confidence threshold')
    ap.add_argument('-nsm', '--confidence-nsm', required=False, default=0.4, type=float,
                    help = 'non max supression threshold')
    args = ap.parse_args()
    return args

if __name__ == "__main__":

    args = parseArgs()

    tracker = BallTracker(args.config, args.classes, args.weights, args.confidence_threshold, args.confidence_nsm)

    video = False
    if os.path.isdir(args.input):
        images = sorted(glob.glob(os.path.join(args.input, "*.*")))
    
    elif os.path.isfile(args.input):
        if ".avi" in args.input or ".mp4" in args.input:
            video = True
        else:
            images = [args.input]


    if video:
        cap = cv2.VideoCapture(args.input)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                tracker.predict(frame, draw=True)
                cv2.imshow('frame', frame)
                # & 0xFF is required for a 64-bit system
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

    else:
        for input_image_path in images:

            image = cv2.imread(input_image_path)
            tracker.predict(image, draw=True)

            cv2.imshow("object detection", image)
            if cv2.waitKey() & 0xFF == ord('q'):
                break

