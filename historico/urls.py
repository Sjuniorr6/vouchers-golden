
from django.urls import path
from .views import historico
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('historico', historico.as_view(), name='historico_list'),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
