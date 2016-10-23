from __future__ import unicode_literals

from django.db import models

import datetime.datetime

# class Pokemon(models.Model):
#     name = models.CharField(max_length=30)
#
#     base_attack = models.IntegerField()
#     base_defence = models.IntegerField()
#     base_stamina = models.IntegerField()
#
#
# class UploadedPokemon(Pokemon):
#     cp = models.IntegerField()
#     hp = models.IntegerField()
#     upgrade_cost = models.IntegerField()
#
#     iv_attack = IntegerField()
#     iv_defence = IntegerField()
#     iv_stamina = IntegerField()
#
#     source = UploadedImage()

def decide_path(instance, filename):
    filename = ""
    dt = datetime.datetime.now()
    new_name = "uploads/{}-{}-{}_{}-{}_{}"
    new_name = filename.format(dt.year,
                       dt.month,
                       dt.day,
                       dt.hour,
                       dt.second,
                       dt.microsecond)

    new_name += "." + filename.split(".")[-1]

    return new_name

    # extension = filename.split(".")[-1]
    # file_path = "../../../media/" + filename
    # if os.path.exists(file_path):
    #     num_files = os.listdir(

class UploadedImage(models.Model):
    img_file = models.ImageField(upload_to=decide_path)



