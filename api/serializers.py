from rest_framework import serializers

from financas.models import Categoria, MetaEconomia, Transacao


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'tipo', 'cor', 'icone']
        read_only_fields = ['id']


class TransacaoSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(read_only=True)

    class Meta:
        model = Transacao
        fields = ['id', 'descricao', 'valor', 'data', 'categoria', 'tipo_display', 'criado']
        read_only_fields = ['id', 'tipo_display', 'criado']


class MetaEconomiaSerializer(serializers.ModelSerializer):
    progresso = serializers.FloatField(read_only=True)

    class Meta:
        model = MetaEconomia
        fields = ['id', 'nome', 'valor_alvo', 'valor_atual', 'prazo', 'concluida', 'progresso']
        read_only_fields = ['id', 'progresso']
