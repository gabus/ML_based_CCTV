from cv2 import cv2
import time
from threading import Thread
from mail_manager import Mailer, AttachmentsSelectAlgorithm
from writer import Writer
from video_stream import VideoStream
from loguru import logger
import cli_argument_parser
from photo_ml_parser import MLPhotoParser
from utils.decorators import loop_for_sec
from settings import CONTINUOUS_RECORDING_TIMER, PERSON_SCORE_THRESHOLD
from utils.fps import FPS



class ML_CCTV:

    def __init__(self):
        # Initialize video stream
        self.video_stream = VideoStream((cli_argument_parser.IM_W, cli_argument_parser.IM_H), cli_argument_parser.USER_FRAMERATE)
        self.video_stream_restart_timer = 30 * 60  # how often reset camera to fix brightness (in minutes)
        self.next_video_stream_reset = time.time() + self.video_stream_restart_timer

        self.writer = Writer()
        self.mailer = Mailer()
        self.fps = FPS()

        self.ml = MLPhotoParser(cli_argument_parser.MODEL_NAME, cli_argument_parser.GRAPH_NAME, cli_argument_parser.LABELMAP_NAME)
        self.labels = self.ml.get_labels()

        self.person_detection_cooldown_time = 6  # how many seconds after human is detected, camera should be alert
        self.person_detection_timer = 0
        self.photos_to_send = []

    def main(self):
        # Get model details
        height = self.ml.get_input_details()[0]['shape'][1]
        width = self.ml.get_input_details()[0]['shape'][2]

        logger.info("Start while loop")
        while True:
            frame = self.video_stream.get_new_frame()

            # Acquire frame and resize to expected shape [1xHxWx3]
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (width, height))

            # ML magic
            self.ml.analyze_frame(frame_resized)
            boxes = self.ml.get_boxes()
            classes = self.ml.get_detected_object_id()
            scores = self.ml.get_scores()

            # Loop over all detections
            for i in range(len(scores)):

                object_name = self.labels[int(classes[i])]  # Look up object name from "labels" array using class index
                if object_name != "person":
                    continue

                if scores[i] < PERSON_SCORE_THRESHOLD:
                    continue

                self.person_detection_timer = time.time()
                logger.debug({"scores[i]": scores[i], "label": object_name})

                # Get bounding box coordinates and draw box
                ymin = int(max(1, (boxes[i][0] * cli_argument_parser.IM_H)))
                xmin = int(max(1, (boxes[i][1] * cli_argument_parser.IM_W)))
                ymax = int(min(cli_argument_parser.IM_H, (boxes[i][2] * cli_argument_parser.IM_H)))
                xmax = int(min(cli_argument_parser.IM_W, (boxes[i][3] * cli_argument_parser.IM_W)))

                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 1)

                # Draw framerate in corner of frame
                cv2.putText(frame, 'FPS: {0:.2f}'.format(self.fps.get_frame_time()), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

                # ===============================================
                # ML human score (comment out when not used)
                # ===============================================
                # label = '%s: %d%%' % (object_name, int(scores[i] * 100))  # Example: 'person: 72%'
                # labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
                # label_ymin = max(ymin, labelSize[1] + 10)  # Make sure not to draw label too close to top of window
                # cv2.rectangle(frame, (xmin, label_ymin - labelSize[1] - 10), (xmin + labelSize[0], label_ymin + baseLine - 10), (255, 255, 255),  cv2.FILLED)  # Draw white box to put label text in
                # cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)  # Draw label text
                # cv2.imshow('Object detector', frame)  # draw a frame on the screen
                # ===============================================

                file_location = self.writer.write_image(frame)
                self.photos_to_send.append(file_location)

                self.detection_loop()

            # force update at the end of execution as no "get_execution_time" was triggered
            # hence next frame won't be accurate
            self.fps.update()

            if self.person_detection_cooldown_time + self.person_detection_timer > time.time():
                logger.debug("Human detected. Camera is alert")
                continue

            if self.photos_to_send:
                Thread(target=self.mailer.send_email, args=(self.photos_to_send, AttachmentsSelectAlgorithm.spread_25mb,)).start()
                self.photos_to_send = []

            if self.next_video_stream_reset < time.time():
                self.video_stream.reset()
                self.next_video_stream_reset = self.next_video_stream_reset + self.video_stream_restart_timer

            logger.debug("idle")
            time.sleep(1)

    @loop_for_sec(seconds=CONTINUOUS_RECORDING_TIMER)
    def detection_loop(self):
        """
        for next x seconds just continue recording without analyzing frames
        """
        logger.debug("saving frames without analyzing")

        frame = self.video_stream.get_new_frame()
        cv2.putText(frame, 'FPS: {0:.2f}'.format(self.fps.get_frame_time()), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

        file_location = self.writer.write_image(frame)
        self.photos_to_send.append(file_location)
        time.sleep(0.3)


ML_CCTV().main()
