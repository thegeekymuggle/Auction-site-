# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models


class category(models.Model):

    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class product(models.Model):
    product_name = models.CharField(max_length=100)
    p_category = models.ForeignKey(category, on_delete=models.CASCADE)
    price = models.FloatField()
    start = models.TimeField()
    image = models.FileField()
    highest = models.CharField(max_length=200, default=0)
    status = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('auction:product-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.product_name + '-' + str(self.p_category)


