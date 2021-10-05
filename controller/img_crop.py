import base64
import datetime
import logging
import os

import cv2
import imutils


def crop_image(front_img, filename=None,
                         p_kl_kod=None, p_method=None,
                         p_dir='upload'):
    if not front_img:
        front_img = 'NO DATA'
    ext = 'jpg'
    req_id = ''
    if p_method:
        req_id = p_method + '_' + req_id
    if p_kl_kod:
        req_id = p_kl_kod + '_' + req_id
    try:
        log_directory = 'crop/' + p_dir
        log_directory = os.path.join(log_directory,
                                     datetime.datetime.now().strftime(
                                         "%Y-%m-%d"))

        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        if not filename:
            filename = os.path.join(log_directory,
                                    req_id + datetime.datetime.now().strftime(
                                        "%Y-%m-%d_%H-%M-%S-%f") + '.' + ext)

        with open(filename, 'wb') as f_output:
            f_output.write(front_img)
        image = cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        ret, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU)
        inverted_binary = ~binary

        contours, hierarchy = cv2.findContours(
            inverted_binary,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE)

        mx = (0, 0, 0, 0)
        mx_area = 0
        for cont in contours:
            x, y, w, h = cv2.boundingRect(cont)
            area = w * h
            if area > mx_area:
                mx = x, y, w, h
                mx_area = area
        x, y, w, h = mx

        # Crop and save
        roi = image[y:y + h, x:x + w]

        h, w, c = roi.shape
        if h > w:
            roi = imutils.rotate_bound(roi, -90)

        cv2.imwrite(filename, roi)
    except Exception as e:
        logging.error(str(e))
    return img_to_bytes(filename)


def img_to_bytes(img):
    img = cv2.imread(img)
    _, img_encoded = cv2.imencode('.jpg', img)
    img = base64.b64encode(img_encoded)
    return img
