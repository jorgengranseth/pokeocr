from django.conf.urls import url

from pokeocr import views

app_name = 'pokeocr'

urlpatterns = [
    # /
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^rate-a-mon$', views.RateAMon.as_view(), name='rate_a_mon'),
]
