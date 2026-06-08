from datetime import date

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from financas.models import Categoria, Transacao

from .services import get_extrato


def make_user(username='dashuser', password='pass1234!'):
    return User.objects.create_user(username=username, password=password)


def make_cats(user):
    cat_e = Categoria.objects.create(usuario=user, nome='Salário', tipo='E')
    cat_s = Categoria.objects.create(usuario=user, nome='Mercado', tipo='S')
    return cat_e, cat_s


def make_tx(user, cat, valor, when=None):
    return Transacao.objects.create(
        usuario=user, categoria=cat,
        descricao='test', valor=valor,
        data=when or date.today())


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client = Client()

    def test_dashboard_exige_login(self):
        resp = self.client.get(reverse('dashboard'))
        self.assertRedirects(resp, '/login/?next=/dashboard/', fetch_redirect_response=False)

    def test_dashboard_logado_200(self):
        self.client.login(username='dashuser', password='pass1234!')
        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'dashboard/dashboard.html')


class GetExtratoServiceTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.cat_e, self.cat_s = make_cats(self.user)
        today = timezone.localdate()
        self.mes = today.month
        self.ano = today.year

    def test_get_extrato_totais(self):
        make_tx(self.user, self.cat_e, 3000)
        make_tx(self.user, self.cat_s, 800)
        ext = get_extrato(self.user, self.mes, self.ano)
        self.assertEqual(ext['total_entradas'], 3000)
        self.assertEqual(ext['total_saidas'], 800)
        self.assertIn(ext['mes_nome'], [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro',
        ])

    def test_get_extrato_mes_vazio(self):
        ext = get_extrato(self.user, self.mes, self.ano)
        self.assertEqual(ext['total_entradas'], 0)
        self.assertEqual(ext['total_saidas'], 0)
        self.assertEqual(list(ext['transacoes']), [])


class ExportViewTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client = Client()
        self.client.login(username='dashuser', password='pass1234!')

    def test_exportar_csv_logado(self):
        resp = self.client.get(reverse('exportar_csv'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('text/csv', resp['Content-Type'])
        content = resp.content.decode('utf-8-sig')
        self.assertIn('Extrato Mensal', content)

    def test_exportar_pdf_logado(self):
        resp = self.client.get(reverse('exportar_pdf'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'application/pdf')
        self.assertTrue(resp.content.startswith(b'%PDF'))

    def test_export_exige_login(self):
        anon = Client()
        for url_name in ('exportar_csv', 'exportar_pdf'):
            resp = anon.get(reverse(url_name))
            self.assertEqual(resp.status_code, 302)
            self.assertIn('/login/', resp['Location'])
