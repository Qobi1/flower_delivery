from django.contrib import admin
from .models import *

admin.site.register(Flower)
admin.site.register(FlowerType)
admin.site.register(FlowerColour)
admin.site.register(Data)
admin.site.register(ChosenFlower)
