from django.db.models import Sum


def saldo_usuario(user):
    entradas = user.transacoes.filter(categoria__tipo='E').aggregate(s=Sum('valor'))['s'] or 0
    saidas = user.transacoes.filter(categoria__tipo='S').aggregate(s=Sum('valor'))['s'] or 0
    return entradas - saidas
