import os
import numpy as np
from tflite_runtime.interpreter import Interpreter


class MLPhotoParser:

    def __init__(self, model_name, graph_name, labelmap_name):
        self.__model_name = model_name
        self.__labelmap_name = labelmap_name

        model_path = os.path.join(os.getcwd(), model_name, graph_name)
        self.__interpreter = Interpreter(model_path=model_path)
        self.__interpreter.allocate_tensors()

    def get_labels(self):
        path_to_labels = os.path.join(os.getcwd(), self.__model_name, self.__labelmap_name)
        with open(path_to_labels, 'r') as f:
            return [line.strip() for line in f.readlines()]

    def get_input_details(self):
        return self.__interpreter.get_input_details()

    def get_output_details(self):
        return self.__interpreter.get_output_details()

    def analyze_frame(self, frame):
        """
         Brains function. Analyzes frame and sets data on interpreter tensor
        """
        input_data = np.expand_dims(frame, axis=0)
        self.__interpreter.set_tensor(self.get_input_details()[0]['index'], input_data)
        self.__interpreter.invoke()

    def get_boxes(self):
        """
         Bounding box coordinates of detected objects
        """
        return self.__interpreter.get_tensor(self.get_output_details()[0]['index'])[0]

    def get_detected_object_id(self):
        """
         Class index of detected objects
        """
        return self.__interpreter.get_tensor(self.get_output_details()[1]['index'])[0]

    def get_scores(self):
        """
         Confidence of detected objects
        """
        return self.__interpreter.get_tensor(self.get_output_details()[2]['index'])[0]

    def get_detected_objects_count(self):
        """
         Total number of detected objects (inaccurate and not needed)
        """
        return self.__interpreter.get_tensor(self.get_output_details()[3]['index'])[0]


