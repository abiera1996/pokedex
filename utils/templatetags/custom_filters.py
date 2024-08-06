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

register = template.Library()


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)