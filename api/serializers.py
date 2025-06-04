from rest_framework import serializers
from app.models import Flower, FlowerColour, FlowerType, ApprovedBy, OrderedBy, ChosenFlower


class FlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = '__all__'


class FlowerColourSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowerColour
        fields = '__all__'


class FlowerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowerType
        fields = '__all__'


class ChosenFlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChosenFlower
        fields = '__all__'
        read_only_fields = ['data']

    def to_representation(self, instance):
        request = self.context['request']
        representation = super().to_representation(instance)

        if instance.flower:
            image_url = (
                request.build_absolute_uri(instance.flower.image.url)
                if request and instance.flower.image
                else None
            )
            representation['flower'] = {
                'id': instance.flower.id,
                'image': image_url
            }

        return representation



class DataSerializer(serializers.ModelSerializer):
    flower_type = serializers.PrimaryKeyRelatedField(
        queryset=FlowerType.objects.all(), many=True
    )
    flower_colour = serializers.PrimaryKeyRelatedField(
        queryset=FlowerColour.objects.all(), many=True
    )
    chosen_flowers = ChosenFlowerSerializer(many=True, write_only=True)

    class Meta:
        model = OrderedBy
        fields = '__all__'
        write_only_fields = ['message']

    def to_representation(self, instance):
        request = self.context['request']
        representation = super().to_representation(instance)
        password = self.context['password']

        selected_colors = list(instance.flower_colour.values_list('id', flat=True))
        all_colours = FlowerColour.objects.all()

        representation['flower_colour'] = [
            {
                'id': i.id,
                'name': i.name,
                'image': request.build_absolute_uri(i.image.url),
                'selected': i.id in selected_colors
            }
            for i in all_colours
        ]

        selected_types = list(instance.flower_type.values_list('id', flat=True))
        all_types = FlowerType.objects.all()
        representation['flower_type'] = [
            {
                'id': i.id,
                'name': i.name,
                'image': request.build_absolute_uri(i.image.url),
                'selected': i.id in selected_types
            }
            for i in all_types
        ]

        representation['chosen_flowers'] = ChosenFlowerSerializer(
            ChosenFlower.objects.filter(data=instance), many=True, context={'request': request}
        ).data

        print(password)
        if representation.get('is_anonymous') is True and password is False:
            representation['city'] = None
            representation['street'] = None
            representation['building'] = None
            representation['corpus'] = None
            representation['flat'] = None
            representation['phone_number'] = None
            representation['time'] = None

        return representation

    def create(self, validated_data):
        chosen_flowers_data = validated_data.pop('chosen_flowers', [])
        flower_type = validated_data.pop('flower_type', [])
        flower_colour = validated_data.pop('flower_colour', [])

        # Create Data instance
        data_instance = OrderedBy.objects.create(**validated_data)
        data_instance.flower_type.set(flower_type)
        data_instance.flower_colour.set(flower_colour)

        # Create related ChosenFlower instances
        for flower_data in chosen_flowers_data:
            ChosenFlower.objects.create(data=data_instance, **flower_data)
        return data_instance


class ApprovedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovedBy
        fields = '__all__'

