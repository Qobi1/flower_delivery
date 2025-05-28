import uuid
from django.db import models

class FlowerType(models.Model):
    name = models.CharField(max_length=512)
    image = models.ImageField()

    class Meta:
        verbose_name = "Flower Type"
        verbose_name_plural = "Flower Types"

    def __str__(self):
        return str(self.name)


class FlowerColour(models.Model):
    name = models.CharField(max_length=512)
    image = models.ImageField()

    class Meta:
        verbose_name = "Flower Colour"
        verbose_name_plural = "Flower Colours"

    def __str__(self):
        return f"{self.name} - {str(self.name)}"


class Flower(models.Model):
    image = models.ImageField()
    colour = models.ForeignKey(FlowerColour, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(FlowerType, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Flower"
        verbose_name_plural = "Flowers"

    def __str__(self):
        return f"{self.type.name} - {self.colour.name} - {str(self.id)}"


class Data(models.Model):
    name = models.CharField(max_length=512)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    flower_type = models.ManyToManyField(FlowerType, related_name='chosen_flower_types')
    flower_colour = models.ManyToManyField(FlowerColour, related_name='chosen_flower_colour')
    city = models.CharField(max_length=512)
    street = models.CharField(max_length=512)
    building = models.CharField(max_length=512)
    corpus = models.IntegerField()
    flat = models.IntegerField()
    phone_number = models.IntegerField()
    message = models.TextField()
    time = models.CharField(max_length=128)
    is_anonymous = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Data"
        verbose_name_plural = "Datas"

    def __str__(self):
        return f"{self.uuid} ({str(self.id)})"


class ChosenFlower(models.Model):
    TEXT = [
        ('фуу...', "фуу..."),
        ('нее', "нее"),
        ('хз', "хз"),
        ('норм', "норм"),
        ('ваау!!', "ваау!!"),
    ]
    flower = models.ForeignKey(Flower, related_name='flowers', on_delete=models.SET_NULL, null=True)
    data = models.ForeignKey(Data, on_delete=models.CASCADE, related_name='chosen_flowers')
    text = models.CharField(max_length=56, choices=TEXT)

    class Meta:
        verbose_name = "Chosen Flower"
        verbose_name_plural = "Chosen Flowers"

    def __str__(self):
        return f"{self.id} - Flower ID{self.flower.id}"
