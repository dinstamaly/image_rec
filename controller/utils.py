import decimal
from copy import copy

import datetime
import json
from xml.etree import cElementTree

from flask import Response, g
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql import ClauseElement

from controller.codes import OBJECT_DOES_NOT_EXIST, MESSAGES


class BusinessException(Exception):

    def __init__(self, code, message=None):
        super(BusinessException, self).__init__()
        self.code = code
        self.message = message


def make_xml_response(p_code: int,
                      p_message: str = None,
                      p_dict: dict = None,
                      p_data_tree=None,
                      p_plain_text=None) -> Response:
    """
    Функция формирует xml контент и возврощает обьект Response
    """
    if p_code != 0 and not p_message:
        p_message = MESSAGES.get(g.language, {}).get(
            p_code, 'Unknown error code: {}'.format(p_code)
        )

    v_xml = cElementTree.Element("xml")
    v_status_tree = cElementTree.SubElement(v_xml, 'status')
    cElementTree.SubElement(v_status_tree, 'code').text = str(p_code)
    cElementTree.SubElement(v_status_tree, 'message').text = p_message

    if p_dict:
        v_data_tree = cElementTree.SubElement(v_xml, 'data')

        for k in p_dict.keys():
            cElementTree.SubElement(v_data_tree, k).text = str(p_dict[k])

    if p_data_tree:
        v_xml.append(p_data_tree)

    if p_plain_text:
        cElementTree.SubElement(v_xml, 'data').text = p_plain_text

    xml_str = cElementTree.tostring(v_xml, encoding='UTF-8')
    resp = Response(xml_str, mimetype='application/xml; charset=utf-8')

    return resp


def join_by_field(query, model, field_key, value):
    attrs = field_key.split('.')

    if len(attrs) == 1:
        query = _filter_by_column(query, model, field_key, value)

    elif len(attrs) == 2:
        joined_col = attrs[0]

        if hasattr(model, joined_col):
            rel_obj = getattr(model, joined_col)
            if hasattr(rel_obj, 'property'):
                if hasattr(rel_obj.property, 'mapper'):
                    if hasattr(rel_obj.property.mapper, 'class_'):
                        rel_class = rel_obj.property.mapper.class_
                        query = query.join(rel_class)
                        query = _filter_by_column(
                            query, rel_class, attrs[1], value
                        )

    elif len(attrs) > 2:
        joined_col = attrs[0]
        attrs.pop(0)
        field_key = '.'.join(attrs)
        rel_obj = getattr(model, joined_col)

        if hasattr(rel_obj, 'property'):
            if hasattr(rel_obj.property, 'mapper'):
                if hasattr(rel_obj.property.mapper, 'class_'):
                    rel_class = rel_obj.property.mapper.class_
                    query = query.join(rel_class)
                    query = join_by_field(query, rel_class, field_key, value)

    return query


def _filter_by_column(query, model, field, value):
    if hasattr(model, field):
        field = getattr(model, field)
        if hasattr(field, 'type'):

            if isinstance(field.type, String):
                query = query.filter(field.ilike(u'%{}%'.format(value)))
            elif isinstance(field.type, Integer):
                query = query.filter(field == value)
            elif isinstance(field.type, Boolean):
                if isinstance(value, str):
                    if value.lower() == 'true':
                        value = True
                    else:
                        value = False

                if isinstance(value, bool):
                    query = query.filter(field.is_(value))
            elif isinstance(field.type, DateTime):
                # convert value to datetime and filter by datetime
                pass
            # elif isinstance()

    return query


def filter_by_keys(model, query, bag):
    for k in bag.keys():
        query = join_by_field(
            query=query, model=model, field_key=k, value=bag[k],
        )

    return query


def save_obj(session, obj):
    try:
        session.add(obj)
    except Exception:
        raise BusinessException(code=OBJECT_DOES_NOT_EXIST)
    else:
        return True


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        return instance, True


class JSONEncoderCore(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            r = str(o)[:19]
            return r
        elif isinstance(o, datetime.date):
            return str(o)
        elif isinstance(o, datetime.time):
            r = str(o)
            return r
        elif isinstance(o, decimal.Decimal):
            return fakefloat(o)
        elif isinstance(o, datetime.timedelta):
            return o.total_seconds()
        elif isinstance(o.__class__, DeclarativeMeta):
            return orm_to_json(o)
        else:
            return super(JSONEncoderCore, self).default(o)


class fakefloat(float):
    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return str(self._value)


def orm_to_json(orm):
    if not orm:
        return None
    if isinstance(orm, list):
        ret = []
        for o in orm:
            if hasattr(o, '__dict__'):
                d = copy(o.__dict__)
            else:
                d = o._asdict()
            d.pop('_sa_instance_state', None)
            ret.append(d)
        return ret
    else:
        if hasattr(orm, '__dict__'):
            d = copy(orm.__dict__)
        else:
            d = orm._asdict()
        d.pop('_sa_instance_state', None)
        return d


def make_json_response(p_content):
    if not p_content:
        p_content = {}

    if 'result' not in p_content:
        p_content.update({'result': 0})

    resp = Response(
        json.dumps(p_content, cls=JSONEncoderCore),
        mimetype='application/json; charset=utf-8',
    )

    return resp

