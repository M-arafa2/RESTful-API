from django.urls import path
from . import views

urlpatterns = [
    path('categories',views.categoryView.as_view()),
    path('groups/manager/users', views.UserGroupViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'})),
    path('groups/deliverycrew/users', views.DeliveryCrewViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'})),
]