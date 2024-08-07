"""
Utilities custom filters
"""
import json
import math
from django.utils import formats
from django import template
from django.utils.timezone import now
from django.contrib.humanize.templatetags.humanize import intcomma
from datetime import datetime, timedelta
from utils import helpers

register = template.Library()


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def color_type(type): 
    return  helpers.TYPE_COLOR.get(type, 'silver')