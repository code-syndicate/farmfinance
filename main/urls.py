from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', views.IndexView, name = 'indexview'),
    path('tokenomics/', views.TokenomicsView, name = 'tokenomics'),
    path('telegram_bot/', include('django_telegrambot.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)