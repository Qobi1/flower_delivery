from django.contrib import admin
from .models import *
from django.utils.html import format_html

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    readonly_fields = ("type_name", "image_preview")
    list_display = ("display_image", "colour", "type_name")
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


@admin.register(OrderedBy)
class OrderedByAdmin(admin.ModelAdmin):
    list_display = (
        "id", "uuid", "name", "city", "street", "building",
        "flat", "phone_number", "time", "is_anonymous",
        "visits", "approved_count"
    )
    readonly_fields = ("approved_count",)
    search_fields = ("name", "phone_number", "uuid")
    list_filter = ("is_anonymous", "city", "flower_type", "flower_colour")

    def approved_count(self, obj):
        return ApprovedBy.objects.filter(order=obj).count()
    approved_count.short_description = "Количество подтверждений"



@admin.register(FlowerType)
class FlowerTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "display_image")
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

@admin.register(FlowerColour)
class FlowerColourAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "display_image")
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


admin.site.register(ApprovedBy)

