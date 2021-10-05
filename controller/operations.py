import base64
import datetime
import logging
import os


def save_image(image, filename=None,
                         p_kl_kod=None, p_method=None,
                         p_dir=None):
    if not image:
        image = 'NO DATA'
    image = base64.b64decode(image)
    ext = 'jpg'
    req_id = ''
    if p_method:
        req_id = p_method + '_' + req_id
    if p_kl_kod:
        req_id = p_kl_kod + '_' + req_id
    try:
        log_directory = 'image/' + p_dir
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
            f_output.write(image)
    except Exception as e:
        logging.error(str(e))
    return filename
