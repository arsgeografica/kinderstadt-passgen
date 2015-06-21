# -*- coding: utf-8 -*-
from flask import current_app as app
from flask.ext.wtf import Form
from wtforms import BooleanField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class OrderForm(Form):
    range_size = IntegerField(validators=[DataRequired()])
    single_page = BooleanField()

    def __init__(self, *args, **kwargs):
        max_val = app.config['RANGE_SIZE_MAX']
        msg = u'Sie können maximal %d Pässe auf einmal anfordern.' % max_val
        range_validator = NumberRange(min=1, max=max_val, message=msg)
        self.range_size.kwargs['validators'].append(range_validator)
        self.range_size.kwargs['default'] = app.config['RANGE_SIZE_DEFAULT']

        super(OrderForm, self).__init__(*args, **kwargs)
