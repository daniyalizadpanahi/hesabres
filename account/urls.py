from django.urls import path
from django.views.generic import TemplateView
from .views import login_view


urlpatterns = [
    path("", TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', login_view, name='login'),

]