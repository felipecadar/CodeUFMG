import cv2
import os
import numpy as np

class VideoSaver:
    def __init__(self, v_id, output, frame_width, frame_height):
        self.frame_width = frame_width
        self.frame_height = frame_height

        output = os.path.abspath(output)
        self.rgb_cap = cv2.VideoWriter(os.path.join(output,'rgb_{}.avi'.format(v_id)),cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height)) 
        self.depth_cap = cv2.VideoWriter(os.path.join(output,'depth_{}.avi'.format(v_id)),cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height)) 
        self.segmentation_cap = cv2.VideoWriter(os.path.join(output,'segmentation_{}.avi'.format(v_id)),cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height)) 


        self.segmentation2color_dict  = {
            0:		( 0, 0, 0),
            1:		( 70, 70, 70),
            2:		(190, 153, 153),
            3:		(250, 170, 160),
            4:		(220, 20, 60),
            5:		(153, 153, 153),
            6:	 	(157, 234, 50),
            7:		(128, 64, 128),
            8:		(244, 35, 232),
            9:		(107, 142, 35),
            10:		( 0, 0, 142),
            11:		(102, 102, 156),
            12:	 	(220, 220, 0)
        }


    def SaveFrameRGB(self, image):
        np_image = np.asarray(image.raw_data).reshape([self.frame_height, self.frame_width, 4]).astype(np.uint8)[:,:,:-1]
        cv2.imwrite("img_rgb.png", np_image)
        self.rgb_cap.write(np_image)

    def SaveFrameDepth(self, image):
        np_image = np.asarray(image.raw_data).reshape([self.frame_height, self.frame_width, -1])[:, :, :3]
        np_image = np_image[:, :, ::-1]
        np_image = np_image.astype(np.float32)
        R = np_image[:, :, 0]
        G = np_image[:, :, 1]
        B = np_image[:, :, 2]
        normalized = ((R + (G * 256.0) + (B * 256.0 * 256.0)) / ((256.0 * 256.0 * 256.0) - 1)) * 1000.0
        normalized = normalized.astype(np.uint8)

        new_frame = np.zeros([self.frame_height, self.frame_width, 3], dtype=np.uint8)
        new_frame[:, :, 0] = normalized
        new_frame[:, :, 1] = normalized
        new_frame[:, :, 2] = normalized

        cv2.imwrite("img_depth.png", new_frame)
        self.depth_cap.write(new_frame)

    def SaveFrameSegmentation(self, image):
        np_image = np.asarray(image.raw_data).reshape([self.frame_height, self.frame_width, -1])[:, :, :3]
        segmentation = np_image[:, :, 2]

        new_frame = np.zeros([self.frame_height, self.frame_width, 3], dtype=np.uint8)
        for key, color in self.segmentation2color_dict.items():
            new_frame[segmentation == key] = color

        cv2.imwrite("img_seg.png", new_frame)
        self.segmentation_cap.write(new_frame)

    def stopAll(self):
        self.rgb_cap.release()
        self.depth_cap.release()
        self.segmentation_cap.release()
