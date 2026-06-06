from django.contrib import admin
from .models import Categoria, Transacao, MetaEconomia


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'cor', 'icone', 'usuario')
    list_filter = ('tipo', 'usuario')
    search_fields = ('nome',)


@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'categoria', 'usuario')
    list_filter = ('data', 'categoria')
    search_fields = ('descricao',)


@admin.register(MetaEconomia)
class MetaEconomiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor_alvo', 'valor_atual', 'prazo', 'concluida', 'usuario')
    list_filter = ('concluida',)
    search_fields = ('nome',)
