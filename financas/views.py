from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from utils.my_mixins import UsuarioQuerysetMixin

from .forms import CategoriaForm, MetaEconomiaForm, TransacaoForm
from .models import Categoria, MetaEconomia, Transacao

MESES = [
    (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
    (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
    (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro'),
]


# ── Transação ──────────────────────────────────────────────────────────────

class TransacaoListView(LoginRequiredMixin, UsuarioQuerysetMixin, ListView):
    model = Transacao
    template_name = 'financas/transacao_list.html'
    context_object_name = 'transacoes'
    paginate_by = 10

    def _get_mes_ano(self):
        today = timezone.localdate()
        try:
            mes = int(self.request.GET.get('mes', today.month))
            ano = int(self.request.GET.get('ano', today.year))
        except (ValueError, TypeError):
            mes, ano = today.month, today.year
        return mes, ano

    def get_queryset(self):
        qs = super().get_queryset()
        mes, ano = self._get_mes_ano()
        qs = qs.filter(data__year=ano, data__month=mes)
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(descricao__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()
        mes_atual, ano_atual = self._get_mes_ano()
        anos = list(
            self.request.user.transacoes
            .values_list('data__year', flat=True)
            .distinct().order_by('data__year')
        )
        if today.year not in anos:
            anos.append(today.year)
        anos.sort()
        params = self.request.GET.copy()
        params.pop('page', None)
        qs_str = params.urlencode()
        ctx.update({
            'meses': MESES,
            'anos': anos,
            'mes_atual': mes_atual,
            'ano_atual': ano_atual,
            'filter_qs': f'&{qs_str}' if qs_str else '',
        })
        return ctx


class TransacaoCreateView(LoginRequiredMixin, UsuarioQuerysetMixin, CreateView):
    model = Transacao
    form_class = TransacaoForm
    template_name = 'financas/transacao_form.html'
    success_url = reverse_lazy('transacoes')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Transação adicionada com sucesso.')
        return super().form_valid(form)


class TransacaoUpdateView(LoginRequiredMixin, UsuarioQuerysetMixin, UpdateView):
    model = Transacao
    form_class = TransacaoForm
    template_name = 'financas/transacao_form.html'
    success_url = reverse_lazy('transacoes')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Transação atualizada com sucesso.')
        return super().form_valid(form)


class TransacaoDeleteView(LoginRequiredMixin, UsuarioQuerysetMixin, DeleteView):
    model = Transacao
    template_name = 'financas/transacao_confirm_delete.html'
    success_url = reverse_lazy('transacoes')

    def form_valid(self, form):
        messages.success(self.request, 'Transação excluída com sucesso.')
        return super().form_valid(form)


# ── Categoria ──────────────────────────────────────────────────────────────

class CategoriaListView(LoginRequiredMixin, UsuarioQuerysetMixin, ListView):
    model = Categoria
    template_name = 'financas/categoria_list.html'
    context_object_name = 'categorias'


class CategoriaCreateView(LoginRequiredMixin, UsuarioQuerysetMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'financas/categoria_form.html'
    success_url = reverse_lazy('categoria_list')

    def form_valid(self, form):
        messages.success(self.request, 'Categoria criada com sucesso.')
        return super().form_valid(form)


class CategoriaUpdateView(LoginRequiredMixin, UsuarioQuerysetMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'financas/categoria_form.html'
    success_url = reverse_lazy('categoria_list')

    def form_valid(self, form):
        messages.success(self.request, 'Categoria atualizada com sucesso.')
        return super().form_valid(form)


class CategoriaDeleteView(LoginRequiredMixin, UsuarioQuerysetMixin, DeleteView):
    model = Categoria
    template_name = 'financas/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria_list')

    def form_valid(self, form):
        messages.success(self.request, 'Categoria excluída com sucesso.')
        return super().form_valid(form)


# ── Meta de Economia ───────────────────────────────────────────────────────

class MetaListView(LoginRequiredMixin, UsuarioQuerysetMixin, ListView):
    model = MetaEconomia
    template_name = 'financas/meta_list.html'
    context_object_name = 'metas'


class MetaCreateView(LoginRequiredMixin, UsuarioQuerysetMixin, CreateView):
    model = MetaEconomia
    form_class = MetaEconomiaForm
    template_name = 'financas/meta_form.html'
    success_url = reverse_lazy('metas')

    def form_valid(self, form):
        messages.success(self.request, 'Meta criada com sucesso.')
        return super().form_valid(form)


class MetaUpdateView(LoginRequiredMixin, UsuarioQuerysetMixin, UpdateView):
    model = MetaEconomia
    form_class = MetaEconomiaForm
    template_name = 'financas/meta_form.html'
    success_url = reverse_lazy('metas')

    def form_valid(self, form):
        messages.success(self.request, 'Meta atualizada com sucesso.')
        return super().form_valid(form)


class MetaDeleteView(LoginRequiredMixin, UsuarioQuerysetMixin, DeleteView):
    model = MetaEconomia
    template_name = 'financas/meta_confirm_delete.html'
    success_url = reverse_lazy('metas')

    def form_valid(self, form):
        messages.success(self.request, 'Meta excluída com sucesso.')
        return super().form_valid(form)
