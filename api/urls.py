from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import CategoriaViewSet, MetaEconomiaViewSet, TransacaoViewSet

router = DefaultRouter()
router.register('transacoes', TransacaoViewSet, basename='api-transacao')
router.register('categorias', CategoriaViewSet, basename='api-categoria')
router.register('metas', MetaEconomiaViewSet, basename='api-meta')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', obtain_auth_token, name='api-token'),
]
