from rest_framework.urls import path
from .views import FlowerRetrieveListAPIView, FlowerColourRetrieveAPIView, FlowerTypeRetrieveList, DataCreateRetrieveListAPIView

urlpatterns = [
    path('flower-colour/', FlowerColourRetrieveAPIView.as_view(), name='api_flower_colour'),
    path('flower-type/', FlowerTypeRetrieveList.as_view(), name='api_flower_type'),
    path('flower/', FlowerRetrieveListAPIView.as_view(), name='api_flowers'),
    path('saved-data/', DataCreateRetrieveListAPIView.as_view(), name='api_saved_data'),
]
