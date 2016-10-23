from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from django.core.urlresolvers import reverse_lazy

import models


class Index(TemplateView):

    template_name = 'index.html'
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

class RateAMon(CreateView):
    model = models.UploadedImage
    fields = ['img_file']

    success_url = reverse_lazy('pokeocr:index')
