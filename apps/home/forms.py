# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,IntegerField,FloatField,BooleanField,SelectField
from wtforms.validators import Email, DataRequired
from flask_login import (
    current_user
)


# login and registration


class ApiForm(FlaskForm):
    api = StringField('Bybit Api Key',
                         id='api',
                         validators=[DataRequired()])
    secret = PasswordField('Bybit Secret Key',
                             id='secret',
                             validators=[DataRequired()])


class SetForm(FlaskForm):
    qt = FloatField('quantity of coin (not USDT)',
                             id='qtt',
                             validators=[DataRequired()])
    delay = FloatField('Delay (seconds)',
                             id='ddd',
                             validators=[DataRequired()])
    pair= StringField('Trading pair',id='mode',validators=[DataRequired()])
    


