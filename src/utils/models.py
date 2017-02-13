import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr

db = SQLAlchemy()


def to_underscore(name):

    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class BaseMixin(object):

    @declared_attr
    def __tablename__(self):
        return to_underscore(self.__name__)

    __mapper_args__ = {'always_refresh': True}

    id = db.Column(db.Integer, primary_key=True, index=True)
    created_on = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_on = db.Column(db.TIMESTAMP, onupdate=db.func.current_timestamp())


class ReprMixin(object):
    """Provides a string representible form for objects."""

    __repr_fields__ = ['id', 'name']

    def __repr__(self):
        fields =  {f:getattr(self, f, '<BLANK>') for f in self.__repr_fields__}
        pattern = ['{0}={{{0}}}'.format(f) for f in self.__repr_fields__]
        pattern = ' '.join(pattern)
        pattern = pattern.format(**fields)
        return '<{} {}>'.format(self.__class__.__name__, pattern)
