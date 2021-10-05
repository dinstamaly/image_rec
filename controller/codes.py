SYSTEM_ERROR = -1
DATABASE_CONNECTION_ERROR = -2
REDIS_CONNECTION_ERROR = -3
FROM_DICT_TO_XML_CONVERSION_ERROR = -5
FROM_XML_TO_DICT_CONVERSION_ERROR = -6
SAVE_XML_ERROR = -7
DATE_PARSE_ERROR = -8
NO_REQUIRED_PARAM = -9
OBJECT_DOES_NOT_EXIST = -10
OK = 0
NO_TRANSFERS = -13
INVALID_PASS = -14
NOT_AUTHORIZED = -15
USER_BLOCKED = -16
ACCESS_DENIED = -17
UNKNOWN_METHOD = -18
INVALID_REQUISITE = -22
GNS_DISABLED_REGION = -110
GNS_WRONG_VEHICLE_NUM = -111
SF_DISABLED_REGION = -112
SP_RESPONSE_ERROR = -500
SP_SEND_REQUEST_ERROR = -501
SERVICE_CONFIG_ERROR = -100
ABS_SERVER_UNAVAILABLE = -101

MESSAGES = {
    'ru': {
        OK: 'ok',
        NO_TRANSFERS: 'Нет трансферов',
        SYSTEM_ERROR: 'Системная ошибка, попробуйте позже',
        INVALID_PASS: 'Неверное имя пользователя или пароль',
        NOT_AUTHORIZED: 'Сессия закрыта',
        USER_BLOCKED: 'Доступ заблокирован!',
        ACCESS_DENIED: 'Доступ заблокирован!',
        FROM_DICT_TO_XML_CONVERSION_ERROR: (
            'Ошибка конвертирования от Dictionary к XML'
        ),
        FROM_XML_TO_DICT_CONVERSION_ERROR: (
            'Ошибка конвертирования от XML к Dictionary',
        ),
        SAVE_XML_ERROR: 'Ошибка при сохранении XML',
        DATABASE_CONNECTION_ERROR: 'Ошибка соединения с базой данных',
        REDIS_CONNECTION_ERROR: 'Ошибка соединения с Redis',
        DATE_PARSE_ERROR: 'Формат даты некорректный',
        INVALID_REQUISITE: 'Неверный реквизит',
        NO_REQUIRED_PARAM: 'отсутсвует обязательный параметр',
        OBJECT_DOES_NOT_EXIST: 'Запрашиваемого обьекта в БД не существует',
        GNS_DISABLED_REGION: 'По выбранному району оплата не возможна.',
        GNS_WRONG_VEHICLE_NUM: 'Неверный номер транспорта!',
        SF_DISABLED_REGION: (
            'Прием платежей от ИП за Октябрьского и Сокулукского '
            'районов осуществляется в ГНС при ПКР.',
        ),
        SP_RESPONSE_ERROR: 'Ошибка! Ответ от сервера не успешно',
        SP_SEND_REQUEST_ERROR: 'Ошибка при запросе в сервер провайдера',
        UNKNOWN_METHOD: 'Неверный метод',
        SERVICE_CONFIG_ERROR: 'Неверное значение в запросе',
        ABS_SERVER_UNAVAILABLE: 'Сервер АБС не доступен',
    },
    'en': {},
    'kg': {},
}
