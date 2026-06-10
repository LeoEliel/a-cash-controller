from datetime import date, timedelta
from decimal import Decimal
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from financas.models import Categoria, Transacao, MetaEconomia, TipoTransacao

DEMO_USER = {'username': 'demo', 'password': 'demo1234', 'email': 'demo@example.com'}

CATEGORIAS = [
    {'nome': 'Salário',     'tipo': TipoTransacao.ENTRADA, 'cor': '#1D9E75', 'icone': 'briefcase'},
    {'nome': 'Freelance',   'tipo': TipoTransacao.ENTRADA, 'cor': '#2E6FB7', 'icone': 'laptop'},
    {'nome': 'Alimentação', 'tipo': TipoTransacao.SAIDA,   'cor': '#C25E3A', 'icone': 'cart'},
    {'nome': 'Moradia',     'tipo': TipoTransacao.SAIDA,   'cor': '#7C3AED', 'icone': 'home'},
    {'nome': 'Assinaturas', 'tipo': TipoTransacao.SAIDA,   'cor': '#D97706', 'icone': ''},
    {'nome': 'Saúde',       'tipo': TipoTransacao.SAIDA,   'cor': '#DC2626', 'icone': 'heart-pulse'},
    {'nome': 'Transporte',  'tipo': TipoTransacao.SAIDA,   'cor': '#2E6FB7', 'icone': ''},
    {'nome': 'Lazer',       'tipo': TipoTransacao.SAIDA,   'cor': '#8B5CF6', 'icone': ''},
]

METAS = [
    {'nome': 'Reserva de emergência', 'valor_alvo': Decimal('10000.00'), 'valor_atual': Decimal('4200.00'), 'prazo': date(2026, 12, 31)},
    {'nome': 'Viagem de férias',      'valor_alvo': Decimal('5000.00'),  'valor_atual': Decimal('1800.00'), 'prazo': date(2026, 7, 1)},
    {'nome': 'Notebook novo',         'valor_alvo': Decimal('3500.00'),  'valor_atual': Decimal('3500.00'), 'prazo': date(2026, 5, 1), 'concluida': True},
]


def _day(year, month, day):
    try:
        return date(year, month, day)
    except ValueError:
        return date(year, month, 28)


def build_transactions(user, cats):
    today = date.today()
    txs = []

    for months_back in range(5, -1, -1):
        m = today.month - months_back
        y = today.year
        while m <= 0:
            m += 12
            y -= 1

        sal = cats['Salário']
        free = cats['Freelance']
        alim = cats['Alimentação']
        mor = cats['Moradia']
        ass = cats['Assinaturas']
        sau = cats['Saúde']
        trans = cats['Transporte']
        lazer = cats['Lazer']

        txs += [
            (sal,  'Salário mensal',          Decimal('6500.00'), _day(y, m, 5)),
            (mor,  'Aluguel',                 Decimal('1800.00'), _day(y, m, 10)),
            (ass,  'Netflix',                 Decimal('55.90'),   _day(y, m, 12)),
            (ass,  'Spotify',                 Decimal('21.90'),   _day(y, m, 12)),
            (ass,  'Academia',                Decimal('89.90'),   _day(y, m, 15)),
            (trans,'Gasolina',                Decimal(str(round(random.uniform(180, 260), 2))), _day(y, m, 8)),
            (trans,'Uber',                    Decimal(str(round(random.uniform(20, 60), 2))),   _day(y, m, 18)),
            (alim, 'Supermercado',            Decimal(str(round(random.uniform(400, 700), 2))), _day(y, m, 6)),
            (alim, 'Restaurante',             Decimal(str(round(random.uniform(60, 130), 2))),  _day(y, m, 14)),
            (alim, 'Delivery',                Decimal(str(round(random.uniform(40, 90), 2))),   _day(y, m, 20)),
            (lazer,'Cinema',                  Decimal(str(round(random.uniform(40, 80), 2))),   _day(y, m, 22)),
        ]

        # Freelance some months
        if months_back in (1, 3, 5):
            txs.append((free, 'Projeto web', Decimal(str(round(random.uniform(800, 2000), 2))), _day(y, m, 25)))

        # Occasional health expense
        if months_back in (0, 2, 4):
            txs.append((sau, 'Consulta médica', Decimal(str(round(random.uniform(150, 350), 2))), _day(y, m, 17)))

    return txs


class Command(BaseCommand):
    help = 'Cria usuário demo com categorias, transações e metas de exemplo (idempotente)'

    def handle(self, *args, **options):
        random.seed(42)

        user, created = User.objects.get_or_create(
            username=DEMO_USER['username'],
            defaults={'email': DEMO_USER['email']},
        )
        if created:
            user.set_password(DEMO_USER['password'])
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Usuário "{user.username}" criado.'))
        else:
            self.stdout.write(f'Usuário "{user.username}" já existe.')

        cats = {}
        for dados in CATEGORIAS:
            cat, _ = Categoria.objects.get_or_create(
                usuario=user, nome=dados['nome'], tipo=dados['tipo'],
                defaults={'cor': dados['cor'], 'icone': dados['icone']},
            )
            cats[dados['nome']] = cat
        self.stdout.write(f'{len(cats)} categorias OK.')

        if not Transacao.objects.filter(usuario=user).exists():
            txs = build_transactions(user, cats)
            Transacao.objects.bulk_create([
                Transacao(usuario=user, categoria=cat, descricao=desc, valor=valor, data=data)
                for cat, desc, valor, data in txs
            ])
            self.stdout.write(self.style.SUCCESS(f'{len(txs)} transações criadas.'))
        else:
            self.stdout.write('Transações já existem, pulando.')

        for meta_data in METAS:
            MetaEconomia.objects.get_or_create(
                usuario=user, nome=meta_data['nome'],
                defaults={
                    'valor_alvo': meta_data['valor_alvo'],
                    'valor_atual': meta_data['valor_atual'],
                    'prazo': meta_data['prazo'],
                    'concluida': meta_data.get('concluida', False),
                },
            )
        self.stdout.write(self.style.SUCCESS(f'{len(METAS)} metas OK.'))

        self.stdout.write(self.style.SUCCESS(
            f'\nPronto! Login: username="{DEMO_USER["username"]}" password="{DEMO_USER["password"]}"'
        ))
