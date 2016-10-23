from django.conf.urls import url

from pokeocr import views

app_name = 'pokeocr'

urlpatterns = [
    # /
    url(r'^', views.Index.as_view(), name='index'),
]
