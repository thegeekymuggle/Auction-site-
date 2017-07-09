# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import category, product, final
from django.contrib import admin

# Register your models here.

admin.site.register(category)
admin.site.register(product)
admin.site.register(final)
