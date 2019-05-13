#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from samples.views import SampleList

app_name = 'samples'

urlpatterns = [
    path('', csrf_exempt(SampleList.as_view()))
]