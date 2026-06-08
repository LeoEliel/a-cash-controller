from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from financas.models import Categoria, MetaEconomia, Transacao

from .serializers import CategoriaSerializer, MetaEconomiaSerializer, TransacaoSerializer


class BaseUserViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class TransacaoViewSet(BaseUserViewSet):
    queryset = Transacao.objects.select_related('categoria').order_by('-data', '-criado')
    serializer_class = TransacaoSerializer


class CategoriaViewSet(BaseUserViewSet):
    queryset = Categoria.objects.order_by('tipo', 'nome')
    serializer_class = CategoriaSerializer


class MetaEconomiaViewSet(BaseUserViewSet):
    queryset = MetaEconomia.objects.order_by('concluida', 'prazo')
    serializer_class = MetaEconomiaSerializer
