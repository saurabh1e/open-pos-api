from abc import ABC, abstractstaticmethod
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import cast, Date


class Operators(ABC):
    op = 'equal'

    @staticmethod
    @abstractstaticmethod
    def prepare_queryset(query, model, key, value):
        return query.filter(getattr(model, key) == value)


class In(Operators):
    op = 'in'

    @staticmethod
    def prepare_queryset(query, model, key, values):
        if len(values) == 1:
            values = values[0].split(',')
        return query.filter(getattr(model, key).in_(values))


class Equal(Operators):
    op = 'equal'

    @staticmethod
    def prepare_queryset(query, model, key, value):
        return query.filter(getattr(model, key) == value[0])


class Contains(Operators):
    op = 'contains'

    @staticmethod
    def prepare_queryset(query, model, key, value):
        return query.filter(func.lower(getattr(model, key)).contains(value[0].lower()))


class Boolean(Operators):
    op = 'bool'

    @staticmethod
    def prepare_queryset(query, model, key, value):
        val = False if value[0] == 'false' else True
        return query.filter(getattr(model, key) == val)


class Between(Operators):
    op = 'between'

    @staticmethod
    def prepare_queryset(query, model, key, value):
        val1 = value[0]
        val2 = value[1]
        return query.filter(getattr(model, key).between(val1, val2))


class Greater(Operators):
    op = 'gt'

    @staticmethod
    def prepare_queryset(query, model, key, value):
        return query.filter(getattr(model, key) > value[0])


class Lesser(Operators):
    op = 'lt'

    @staticmethod
    def prepare_queryset(query, model, key, value):
        return query.filter(getattr(model, key) < value[0])


class Greaterequal(Operators):
    op = 'gte'

    @staticmethod
    def prepare_queryset(query, model, key, value):
        return query.filter(getattr(model, key) >= value[0])


class LesserEqual(Operators):
    op = 'lte'

    @staticmethod
    def prepare_queryset(query, model, key, value):
        return query.filter(getattr(model, key) <= value[0])


class DateEqual(Operators):
    op = 'date_equal'

    @staticmethod
    def prepare_queryset(query, model, key, value):
        return query.filter(cast(getattr(model, key), Date) == datetime.strptime(value[0], '%Y-%m-%dT%H:%M:%S.%fZ').date())


class DateGreaterEqual(Operators):
    op = 'date_gte'

    @staticmethod
    def prepare_queryset(query, model, key, value):
        return query.filter(cast(getattr(model, key), Date) >= datetime.strptime(value[0], '%Y-%m-%dT%H:%M:%S.%fZ').date())


class DateLesserEqual(Operators):
    op = 'date_lte'

    @staticmethod
    def prepare_queryset(query, model, key, value):
        return query.filter(cast(getattr(model, key), Date) <= datetime.strptime(value[0], '%Y-%m-%dT%H:%M:%S.%fZ').date())
