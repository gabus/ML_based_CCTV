import os
import cv2


def write_image(file_dir, file_name, image):
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)

    file_path = os.path.join(file_dir, file_name)
    cv2.imwrite(file_path, image)
