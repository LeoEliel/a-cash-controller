from django.urls import path

from . import views

urlpatterns = [
    # Transações
    path('transacoes/', views.TransacaoListView.as_view(), name='transacoes'),
    path('transacoes/nova/', views.TransacaoCreateView.as_view(), name='transacao_nova'),
    path('transacoes/<int:pk>/editar/', views.TransacaoUpdateView.as_view(), name='transacao_editar'),
    path('transacoes/<int:pk>/excluir/', views.TransacaoDeleteView.as_view(), name='transacao_excluir'),
    # Categorias
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/nova/', views.CategoriaCreateView.as_view(), name='categoria_nova'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_editar'),
    path('categorias/<int:pk>/excluir/', views.CategoriaDeleteView.as_view(), name='categoria_excluir'),
    # Metas
    path('metas/', views.MetaListView.as_view(), name='metas'),
    path('metas/nova/', views.MetaCreateView.as_view(), name='meta_nova'),
    path('metas/<int:pk>/editar/', views.MetaUpdateView.as_view(), name='meta_editar'),
    path('metas/<int:pk>/excluir/', views.MetaDeleteView.as_view(), name='meta_excluir'),
]
