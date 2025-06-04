import uuid
from django.db import models

class FlowerType(models.Model):
    name = models.CharField(max_length=512)
    image = models.ImageField()

    class Meta:
        verbose_name = "Типы цветов"
        verbose_name_plural = "Типы цветов"

    def __str__(self):
        return str(self.name)


class FlowerColour(models.Model):
    name = models.CharField(max_length=512)
    image = models.ImageField()

    class Meta:
        verbose_name = "Цвет цвета"
        verbose_name_plural = "Цвета цветов"

    def __str__(self):
        return f"{self.name}"


class Flower(models.Model):
    image = models.ImageField()
    colour = models.ForeignKey(FlowerColour, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(FlowerType, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Цветок"
        verbose_name_plural = "Цветы"

    def __str__(self):
        return f"{self.type.name} - {self.colour.name} - {str(self.id)}"


class OrderedBy(models.Model):
    name = models.CharField(max_length=512, verbose_name="Имя")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="UUID")
    flower_type = models.ManyToManyField(FlowerType, related_name='chosen_flower_types', verbose_name='Тип цветка')
    flower_colour = models.ManyToManyField(FlowerColour, related_name='chosen_flower_colour', verbose_name='Цвет цветка')
    city = models.CharField(max_length=512, verbose_name="Город", null=True, blank=True)
    street = models.CharField(max_length=512, verbose_name="Улица", null=True, blank=True)
    building = models.CharField(max_length=512, verbose_name="Здание", null=True, blank=True)
    corpus = models.CharField(max_length=512, null=True, blank=True)
    flat = models.CharField(max_length=512, verbose_name="Квартира", null=True, blank=True)
    phone_number = models.CharField(max_length=512, verbose_name="Номер телефона", null=True, blank=True)
    message = models.TextField(verbose_name='Сообщение', null=True, blank=True)
    time = models.CharField(max_length=128, verbose_name="Время", null=True, blank=True)
    is_anonymous = models.BooleanField(default=False, verbose_name="Анонимный", null=True, blank=True)
    visits = models.PositiveIntegerField(default=0, verbose_name="Посещения", null=True, blank=True)
    address_mentioned = models.BooleanField(default=True, verbose_name='Адрес написан?')

    class Meta:
        verbose_name = "Заказчик"
        verbose_name_plural = "Заказчики"

    def __str__(self):
        return f"{self.uuid} ({str(self.id)})"


class ApprovedBy(models.Model):
    city = models.CharField(max_length=512, verbose_name="Город")
    street = models.CharField(max_length=512, verbose_name="Улица")
    building = models.CharField(max_length=512, verbose_name="Здание")
    corpus = models.CharField(verbose_name="Корпус")
    flat = models.CharField(verbose_name="Квартира")
    phone_number = models.CharField(verbose_name="Номер телефона")
    message = models.TextField(verbose_name='Сообщение')
    time = models.CharField(max_length=128, verbose_name="Время")
    is_address_typed = models.BooleanField(default=False, verbose_name='Адрес написан?')
    uuid = models.UUIDField(verbose_name='UUID')

    class Meta:
        verbose_name = "Утвердивший"
        verbose_name_plural = "Утвердившие"

    def __str__(self):
        return f"({str(self.id)})"


class ChosenFlower(models.Model):
    TEXT = [
        ('фуу...', "фуу..."),
        ('нее', "нее"),
        ('хз', "хз"),
        ('норм', "норм"),
        ('ваау!!', "ваау!!"),
    ]
    flower = models.ForeignKey(Flower, related_name='flowers', on_delete=models.SET_NULL, null=True)
    data = models.ForeignKey(OrderedBy, on_delete=models.CASCADE, related_name='chosen_flowers')
    text = models.CharField(max_length=56, choices=TEXT)

    class Meta:
        verbose_name = "Выбранные цветы"
        verbose_name_plural = "	Выбранные цветы"

    def __str__(self):
        return f"{self.id} - Flower ID{self.flower.id}"
