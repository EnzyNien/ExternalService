from django.urls import include, re_path, path
from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    re_path(r'^$', views.main, name='main'),
    path('load_data/', views.load_data, name='load_data'),
    path('clear_data/', views.clear_data, name='clear_data'),
    path('units/', views.Units_List.as_view(), name='units'),
    path('companys/', views.Companys_List.as_view(), name='companys'),
]
