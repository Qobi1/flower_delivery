from django.contrib import admin
from .models import *
from django.utils.html import format_html, mark_safe

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    readonly_fields = ("type_name", "image_preview")
    list_display = ("display_image", "colour_display", "type_name")
    fields = ("image_preview", "image", "colour", "type")

    def type_name(self, obj):
        return obj.type.name if obj.type else "-"
    type_name.short_description = "Тип цветка"

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit:cover; border-radius:50%;" />',
                obj.image.url
            )
        return "-"
    display_image.short_description = "Фото"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit:cover; border-radius:50%;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Превью изображения"

    @admin.display(description="Цвет")
    def colour_display(self, obj):
        return obj.colour


@admin.register(FlowerType)
class FlowerTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "display_image", "display_name")
    readonly_fields = ("image_preview",)
    fields = ("image_preview", "image", "name")

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit:cover; border-radius:50%;" />',
                obj.image.url
            )
        return "-"
    display_image.short_description = "Фото"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit:cover; border-radius:50%;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Превью изображения"

    @admin.display(description="Тип")
    def display_name(self, obj):
        return obj.name

@admin.register(FlowerColour)
class FlowerColourAdmin(admin.ModelAdmin):
    list_display = ("id", "display_image", "colour_display")
    readonly_fields = ("image_preview",)
    fields = ("image_preview", "image", "name")

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit:cover; border-radius:50%;" />',
                obj.image.url
            )
        return "-"
    display_image.short_description = "Фото"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit:cover; border-radius:50%;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Превью изображения"

    @admin.display(description="Название")
    def colour_display(self, obj):
        return obj.name



@admin.register(OrderedBy)
class OrderedByAdmin(admin.ModelAdmin):
    list_display = (
        "id", "uuid", "name", "city", "phone_number", "time", "is_anonymous",
        "visits", "approved_count", 'chosen_flowers_display'
    )
    readonly_fields = ('uuid', "approved_count", "chosen_flower_images_with_text")
    search_fields = ("name", "phone_number", "uuid")
    list_filter = ("is_anonymous", )

    def approved_count(self, obj):
        return ApprovedBy.objects.filter(uuid=obj.uuid).count()
    approved_count.short_description = "Количество подтверждений"

    def chosen_flowers_display(self, obj):
        return ", ".join([str(f.flower.id) for f in obj.chosen_flowers.all() if f.flower])

    chosen_flowers_display.short_description = "Выбранные цветы"

    def chosen_flower_images_with_text(self, obj):
        blocks = []
        for chosen in obj.chosen_flowers.select_related('flower'):
            if chosen.flower and chosen.flower.image:
                img_html = f'<img src="{chosen.flower.image.url}" style="height:100px; margin-right:10px;" />'
                text_html = f'<span style="vertical-align:top; font-weight:bold;">{chosen.text}</span>'
                block = f'<div style="margin-bottom:15px; display:flex; align-items:center;">{img_html}{text_html}</div>'
                blocks.append(block)
        if blocks:
            return mark_safe("".join(blocks))
        return "Нет выбранных цветов"
    chosen_flower_images_with_text.short_description = "Изображения выбранных цветов"


@admin.register(ApprovedBy)
class ApprovedByAdmin(admin.ModelAdmin):
    list_display = (
        'get_id', 'get_city', 'get_street','get_phone_number', 'get_time', 'get_is_address_typed', 'get_uuid'
    )
    search_fields = ('phone_number', 'uuid')
    readonly_fields = ('id',)
    ordering = ('-id',)

    fieldsets = (
        (None, {
            'fields': ('uuid', 'city', 'street', 'building', 'corpus', 'flat',
                       'phone_number', 'message', 'time', 'is_address_typed', 'buyer_phone')
        }),
    )

    @admin.display(description='ID')
    def get_id(self, obj):
        return obj.id

    @admin.display(description='Заказ')
    def get_uuid(self, obj):
        order = OrderedBy.objects.filter(uuid=obj.uuid).first()
        if order:
            return order.uuid
        return None

    @admin.display(description='Город')
    def get_city(self, obj):
        return obj.city

    @admin.display(description='Улица')
    def get_street(self, obj):
        return obj.street

    @admin.display(description='Дом')
    def get_building(self, obj):
        return obj.building

    @admin.display(description='Корпус')
    def get_corpus(self, obj):
        return obj.corpus

    @admin.display(description='Квартира')
    def get_flat(self, obj):
        return obj.flat

    @admin.display(description='Телефон')
    def get_phone_number(self, obj):
        return obj.phone_number

    @admin.display(description='Время')
    def get_time(self, obj):
        return obj.time

    @admin.display(description='Введён адрес?')
    def get_is_address_typed(self, obj):
        return "да" if obj.is_address_typed else "нет"




