from django.urls import path

from Main.views import CheckAvailableCar, CalculatePrice, CreateSession, Statistic

urlpatterns = [
    path('available/<pk>', CheckAvailableCar.as_view(), name='available'),
    path('price/', CalculatePrice.as_view(), name='price'),
    path('session/', CreateSession.as_view(), name='session'),
    path('statistic/', Statistic.as_view(), name='statistic'),

]
