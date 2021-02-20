Download weights with

```
wget https://pjreddie.com/media/files/yolov3.weights -P yolo/
```

Usage 

```
usage: yolo_opencv.py [-h] -i INPUT [-c CONFIG] [-w WEIGHTS] [-cl CLASSES]
                      [-t CONFIDENCE_THRESHOLD] [-nsm CONFIDENCE_NSM]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        path to input image, video or directory with images
  -c CONFIG, --config CONFIG
                        path to yolo config file
  -w WEIGHTS, --weights WEIGHTS
                        path to yolo pre-trained weights
  -cl CLASSES, --classes CLASSES
                        path to text file containing class names
  -t CONFIDENCE_THRESHOLD, --confidence-threshold CONFIDENCE_THRESHOLD
                        classifier confidence threshold
  -nsm CONFIDENCE_NSM, --confidence-nsm CONFIDENCE_NSM
                        non max supression threshold
```
