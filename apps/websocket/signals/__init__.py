import datetime
import decimal
from uuid import UUID


def types_dict_convert(o):
    if isinstance(o, UUID):
        return str(o)
    elif isinstance(o, datetime.datetime):
        return o.isoformat()
    elif isinstance(o, decimal.Decimal):
        return str(o)
    elif isinstance(o, datetime.date):
        return o.isoformat()
    else:
        return o.id if o.id is not None else str(o)
