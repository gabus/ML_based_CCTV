from cv2 import cv2
import numpy as np
import time
from threading import Thread
from mail_manager import sendEmail
from writer import Writer
from datetime import datetime
from video_stream import VideoStream
from loguru import logger
import cli_argument_parser
from photo_ml_parser import MLPhotoParser


class ML_CCTV:

    def __init__(self):
        # Initialize video stream
        self.video_stream = VideoStream((cli_argument_parser.IM_W, cli_argument_parser.IM_H), cli_argument_parser.USER_FRAMERATE)

        # Initialize writer
        self.writer = Writer()

        self.ml = MLPhotoParser(cli_argument_parser.MODEL_NAME, cli_argument_parser.GRAPH_NAME, cli_argument_parser.LABELMAP_NAME)
        self.labels = self.ml.get_labels()

    def main(self):
        # Get model details
        height = self.ml.get_input_details()[0]['shape'][1]
        width = self.ml.get_input_details()[0]['shape'][2]

        # Initialize frame rate calculation
        frame_rate_calc = 1
        freq = cv2.getTickFrequency()

        person_detection_cooldown_time = 6  # in seconds
        person_detection_timer = 0

        logger.info("Start while loop")
        # for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
        while True:
            # Start timer (for calculating frame rate)
            t1 = cv2.getTickCount()

            frame = self.video_stream.get_new_frame()

            # Acquire frame and resize to expected shape [1xHxWx3]
            # frame = frame1.copy()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (width, height))

            # ML magic
            self.ml.analyze_frame(frame_resized)
            boxes = self.ml.get_boxes()
            classes = self.ml.get_detected_object_id()
            scores = self.ml.get_scores()

            person_score_threshold = 0.59

            # Loop over all detections
            for i in range(len(scores)):

                if scores[i] < person_score_threshold:
                    continue

                object_name = self.labels[int(classes[i])]  # Look up object name from "labels" array using class index

                if object_name != "person":
                    continue

                person_detection_timer = time.time()
                logger.debug({"scores[i]": scores[i], "label": object_name})

                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1, (boxes[i][0] * cli_argument_parser.IM_H)))
                xmin = int(max(1, (boxes[i][1] * cli_argument_parser.IM_W)))
                ymax = int(min(cli_argument_parser.IM_H, (boxes[i][2] * cli_argument_parser.IM_H)))
                xmax = int(min(cli_argument_parser.IM_W, (boxes[i][3] * cli_argument_parser.IM_W)))

                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 1)

                # ===============================================
                # ML human score (comment out when not used)
                # ===============================================
                label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
                label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
                cv2.rectangle(frame, (xmin, label_ymin - labelSize[1] - 10), (xmin + labelSize[0], label_ymin + baseLine - 10), (255, 255, 255),  cv2.FILLED)  # Draw white box to put label text in
                cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)  # Draw label text
                # ===============================================

                # Draw framerate in corner of frame
                cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

                # All the results have been drawn on the frame, so it's time to display it.
                # cv2.imshow('Object detector', frame)

                file_name = "%s.png" % (datetime.now().strftime("%Y-%m-%d_(%H-%M-%S)_%f"))
                self.writer.write_image(file_name, frame)

                self.detection_loop()

            # if object_name and object_name == "person" and person_score >= person_score_threshold or keep_recording:
            #     logger.info("recording")
            #     file_name = "%s.png" % (datetime.now().strftime("%Y-%m-%d_(%H-%M-%S)_%f"))
            #     writer.write_image(file_name, frame)
            #
            # if object_name and object_name == "person" and person_score >= person_score_threshold:
            #     keep_recording = True
            #
            #     if detection_time == 0:
            #         detection_time = time.time()
            #         keep_recording_timer = time.time()
            #
            #     full_file_path = writer.get_last_location(file_name)
            #     person_frame_names.append(full_file_path)
            #     logger.info("HUMAN FOUND: " + full_file_path)
            #
            # if person_frame_names and (detection_time + send_email_timeout < time.time()):
            #     logger.info("Sending email")
            #     person_frame_names_1 = person_frame_names.copy()
            #     Thread(target=sendEmail, args=(person_frame_names_1,)).start()
            #     person_frame_names.clear()
            #     detection_time = 0
            #
            # if keep_recording_timer != 0 and (keep_recording_timer + person_detection_sleep_cooldown_time < time.time()):
            #     keep_recording = False

            # Calculate frame rate
            t2 = cv2.getTickCount()
            time1 = (t2 - t1) / freq
            frame_rate_calc = 1 / time1

            if person_detection_cooldown_time + person_detection_timer > time.time():
                logger.debug("Human detected. Camera is alert")
                continue

            logger.debug("idle")
            time.sleep(1)

    def detection_loop(self):
        """
        for next x seconds just continue recording without analyzing frames
        """
        continues_recording_time = 3  # in seconds
        start_time = time.time()
        frame_rate_calc = 1

        while start_time + continues_recording_time > time.time():
            logger.debug("saving frame without analyzing it")
            t1 = cv2.getTickCount()
            freq = cv2.getTickFrequency()

            frame = self.video_stream.get_new_frame()
            cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

            file_name = "%s.png" % (datetime.now().strftime("%Y-%m-%d_(%H-%M-%S)_%f"))
            self.writer.write_image(file_name, frame)

            t2 = cv2.getTickCount()
            time1 = (t2 - t1) / freq
            frame_rate_calc = 1 / time1


ML_CCTV().main()
