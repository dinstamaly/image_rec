import base64
import logging
import math

from sqlalchemy import and_

from controller.img_crop import crop_image, img_to_bytes
from controller.make_code import generate_code
from controller.operations import save_image
from db_home.models import db, Image


def get_card_front(bag):

    r = bag['image']
    image_64_encode = r

    img = base64.b64decode(image_64_encode)
    front_img = crop_image(front_img=img)

    return {'image': front_img.decode('utf-8')}


def get_card_back(bag):
    format_ = bag.get('format')
    content = bag.get('content')

    gen_code = generate_code(format_, content)

    return {
        'format': format_,
        'content': content,
        'image': gen_code.decode('utf-8')
    }


def add(bag):
    user_id = bag['user_id']
    format_ = bag['format']
    content = bag['content']
    card_front = bag['card_front']
    card_front = save_image(
        image=card_front,
        p_dir='front'
    )
    card_back = bag['card_back']
    card_back = save_image(
        image=card_back,
        p_dir='back'
    )

    new_img = Image(
        user_id=user_id,
        format=format_,
        content=content,
        card_front=card_front,
        card_back=card_back,
    )
    db.session.add(new_img)
    db.session.commit()

    return {
        "id": new_img.id
    }


def delete(bag):
    # user_id
    id_img = bag['image_id']
    user_id = bag['user_id']
    image = Image.query.filter(and_(
        Image.id == id_img,
        Image.user_id == user_id
    )
    ).first()
    if image:
        db.session.delete(image)
        db.session.commit()
    return {}

def get_list(bag):
    user_id = bag['user_id']
    v_count = bag.get('count', 20)
    v_page = bag.get('page', 1)
    all_images = bag.get('all')

    query = db.session.query(Image)
    # images = filter_by_keys(model=Image, query=image, bag=bag)
    query = query.filter(Image.user_id == user_id)

    v_total_count = query.count()

    if not all_images:
        query = query.order_by(
            'id'
        ).paginate(v_page, v_count, False).items

    result_list = []

    for image in query:
        json_image = {
            'id': image.id,
            'format': image.format,
            'content': image.content,
            'card_front': image.card_front,
            'card_back': image.card_back,
            'date_create': image.date_create,
        }

        result_list.append(json_image)

    return {
        'list': result_list,
        'total_count': v_total_count,
        'pages': int(math.ceil(v_total_count / float(v_count))),
    }
