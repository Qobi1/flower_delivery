from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from app.models import FlowerColour, Flower, FlowerType, ApprovedBy, OrderedBy
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .serializers import FlowerSerializer, FlowerColourSerializer, FlowerTypeSerializer, DataSerializer, ChosenFlowerSerializer
from rest_framework.response import Response
from .utils import parse_list_param


class FlowerRetrieveListAPIView(APIView):
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
    serializer_class = FlowerSerializer

    @extend_schema(
        request=serializer_class,
        responses={201: serializer_class, 200: serializer_class},
        tags=['Flower'],
        parameters=[
            OpenApiParameter(
                name='colour',
                type=OpenApiTypes.STR,
                description='List of colour IDs as a JSON array, e.g. [1,2,3]',
                required=False,
            ),
            OpenApiParameter(
                name='type',
                type=OpenApiTypes.STR,
                description='List of type IDs as a JSON array, e.g. [1,2,3]',
                required=False,
            )
        ],
    )
    def get(self, request):
        flower_colour = parse_list_param(request.query_params.get('colour', None))
        flower_type = parse_list_param(request.query_params.get('type', None))
        queryset = Flower.objects.all()

        if flower_colour or flower_type:
            if flower_type:
                queryset = queryset.filter(type__in=flower_type)
            if flower_colour:
                queryset = queryset.filter(colour__in=flower_colour)

        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class FlowerColourRetrieveAPIView(APIView):
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
    serializer_class = FlowerColourSerializer

    @extend_schema(
        request=serializer_class,
        responses={201: serializer_class, 200: serializer_class},
        tags=['FlowerColour']
    )
    def get(self, request):
        queryset = FlowerColour.objects.all()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class FlowerTypeRetrieveList(APIView):
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
    serializer_class = FlowerTypeSerializer

    @extend_schema(
        request=serializer_class,
        responses={201: serializer_class, 200: serializer_class},
        tags=['FlowerType'],
    )
    def get(self, request):
        queryset = FlowerType.objects.all()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DataCreateRetrieveListAPIView(APIView):
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
    serializer_class = DataSerializer

    @extend_schema(
        request=serializer_class,
        responses={201: serializer_class, 200: serializer_class},
        tags=['Data'],
    )
    def get(self, request):
        queryset = Data.objects.all()
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=serializer_class,
        responses={201: serializer_class, 200: serializer_class},
        tags=['Data'],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
