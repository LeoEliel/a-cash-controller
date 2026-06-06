from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from financas.models import Categoria, TipoTransacao

CATEGORIAS = [
    {'nome': 'Salário',      'tipo': TipoTransacao.ENTRADA, 'cor': '#1D9E75', 'icone': 'briefcase'},
    {'nome': 'Freelance',    'tipo': TipoTransacao.ENTRADA, 'cor': '#2E6FB7', 'icone': 'laptop'},
    {'nome': 'Alimentação',  'tipo': TipoTransacao.SAIDA,   'cor': '#C25E3A', 'icone': 'cart'},
    {'nome': 'Moradia',      'tipo': TipoTransacao.SAIDA,   'cor': '#7C3AED', 'icone': 'home'},
    {'nome': 'Assinaturas',  'tipo': TipoTransacao.SAIDA,   'cor': '#D97706', 'icone': ''},
    {'nome': 'Saúde',        'tipo': TipoTransacao.SAIDA,   'cor': '#DC2626', 'icone': 'heart-pulse'},
    {'nome': 'Transporte',   'tipo': TipoTransacao.SAIDA,   'cor': '#2E6FB7', 'icone': ''},
    {'nome': 'Lazer',        'tipo': TipoTransacao.SAIDA,   'cor': '#8B5CF6', 'icone': ''},
]


class Command(BaseCommand):
    help = 'Cria categorias padrão para um usuário (idempotente)'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username do usuário alvo')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'Usuário "{username}" não encontrado.')

        criadas = 0
        for dados in CATEGORIAS:
            _, created = Categoria.objects.get_or_create(
                usuario=user,
                nome=dados['nome'],
                tipo=dados['tipo'],
                defaults={'cor': dados['cor'], 'icone': dados['icone']},
            )
            if created:
                criadas += 1

        self.stdout.write(self.style.SUCCESS(
            f'{criadas} categoria(s) criada(s) para "{username}" '
            f'({len(CATEGORIAS) - criadas} já existiam).'
        ))
