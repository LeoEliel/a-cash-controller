import json
from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.views.generic import TemplateView

from financas.models import Transacao
from financas.services import saldo_usuario

MESES_ABREV = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
MESES_NOME  = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.localdate()
        mes, ano = today.month, today.year

        # ── KPIs do mês corrente ──────────────────────────────────────
        qs_mes = Transacao.objects.filter(usuario=user, data__year=ano, data__month=mes)
        total_entradas = qs_mes.filter(categoria__tipo='E').aggregate(s=Sum('valor'))['s'] or 0
        total_saidas   = qs_mes.filter(categoria__tipo='S').aggregate(s=Sum('valor'))['s'] or 0
        saldo = saldo_usuario(user)

        # ── Patrimônio acumulado (até 12 meses exibidos) ──────────────
        monthly_rows = (
            Transacao.objects
            .filter(usuario=user)
            .annotate(mes=TruncMonth('data'))
            .values('mes', 'categoria__tipo')
            .annotate(total=Sum('valor'))
            .order_by('mes')
        )

        monthly_map = defaultdict(lambda: {'E': 0.0, 'S': 0.0})
        for row in monthly_rows:
            monthly_map[row['mes']][row['categoria__tipo']] += float(row['total'])

        all_months = sorted(monthly_map)
        running = 0.0
        cumulative = {}
        for m in all_months:
            running += monthly_map[m]['E'] - monthly_map[m]['S']
            cumulative[m] = round(running, 2)

        display_months = all_months[-12:]
        patrimonio_labels = [MESES_ABREV[m.month - 1] for m in display_months]
        patrimonio_data   = [cumulative[m] for m in display_months]

        # ── Gastos por categoria do mês (rosca + top 5) ───────────────
        cats = list(
            qs_mes.filter(categoria__tipo='S')
            .values('categoria__nome')
            .annotate(total=Sum('valor'))
            .order_by('-total')
        )

        total_saidas_cats = sum(float(c['total']) for c in cats)

        cat_labels = [c['categoria__nome'] for c in cats]
        if total_saidas_cats > 0:
            cat_data = [round(float(c['total']) / total_saidas_cats * 100, 1) for c in cats]
        else:
            cat_data = [float(c['total']) for c in cats]

        top_categorias = [
            {
                'nome': c['categoria__nome'],
                'pct': round(float(c['total']) / total_saidas_cats * 100) if total_saidas_cats > 0 else 0,
            }
            for c in cats[:5]
        ]

        ctx.update({
            'saldo': saldo,
            'total_entradas': total_entradas,
            'total_saidas': total_saidas,
            'mes_nome': MESES_NOME[mes - 1],
            'ano': ano,
            'patrimonio_labels': json.dumps(patrimonio_labels),
            'patrimonio_data':   json.dumps(patrimonio_data),
            'cat_labels': json.dumps(cat_labels),
            'cat_data':   json.dumps(cat_data),
            'top_categorias': top_categorias,
        })
        return ctx
