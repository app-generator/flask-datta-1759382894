# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Ports(db.Model):

    __tablename__ = 'Ports'

    id = db.Column(db.Integer, primary_key=True)

    #__Ports_FIELDS__
    port_name = db.Column(db.Text, nullable=True)
    port_code = db.Column(db.Text, nullable=True)

    #__Ports_FIELDS__END

    def __init__(self, **kwargs):
        super(Ports, self).__init__(**kwargs)


class Offices(db.Model):

    __tablename__ = 'Offices'

    id = db.Column(db.Integer, primary_key=True)

    #__Offices_FIELDS__
    office_name = db.Column(db.Text, nullable=True)
    office_code = db.Column(db.Text, nullable=True)

    #__Offices_FIELDS__END

    def __init__(self, **kwargs):
        super(Offices, self).__init__(**kwargs)


class Country(db.Model):

    __tablename__ = 'Country'

    id = db.Column(db.Integer, primary_key=True)

    #__Country_FIELDS__
    country_name = db.Column(db.Text, nullable=True)
    country_code = db.Column(db.Text, nullable=True)

    #__Country_FIELDS__END

    def __init__(self, **kwargs):
        super(Country, self).__init__(**kwargs)



#__MODELS__END
