from django.db.models import Sum

from financas.models import Transacao
from financas.services import saldo_usuario

MESES_NOME = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro',
]


def get_extrato(user, mes, ano):
    qs = (
        Transacao.objects
        .filter(usuario=user, data__year=ano, data__month=mes)
        .select_related('categoria')
    )
    total_entradas = qs.filter(categoria__tipo='E').aggregate(s=Sum('valor'))['s'] or 0
    total_saidas   = qs.filter(categoria__tipo='S').aggregate(s=Sum('valor'))['s'] or 0
    return {
        'transacoes':      qs.order_by('-data', '-criado'),
        'total_entradas':  total_entradas,
        'total_saidas':    total_saidas,
        'saldo':           saldo_usuario(user),
        'mes_nome':        MESES_NOME[mes - 1],
        'ano':             ano,
    }
