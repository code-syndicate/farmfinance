from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from farmfinancebot import urls as farmfinancebot_urls

app_name = 'main'

urlpatterns = [

    path('', views.IndexView, name = 'indexview'),
    path('tokenomics/', views.TokenomicsView, name = 'tokenomics'),
    path('farmfinancebot/', include(farmfinancebot_urls)),
    

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)