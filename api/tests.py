from datetime import date

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from financas.models import Categoria, Transacao


def make_user(username, password='pass1234!'):
    return User.objects.create_user(username=username, password=password)


def make_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token


def make_cat(user, nome='Salário', tipo='E'):
    return Categoria.objects.create(usuario=user, nome=nome, tipo=tipo)


def make_tx(user, cat, valor=100):
    return Transacao.objects.create(
        usuario=user, categoria=cat,
        descricao='test', valor=valor, data=date.today())


class APIAuthTests(APITestCase):
    def setUp(self):
        self.user_a = make_user('user_a')
        self.token_a = make_token(self.user_a)

    def test_sem_token_401(self):
        resp = self.client.get('/api/transacoes/')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_endpoint(self):
        resp = self.client.post('/api/token/', {
            'username': 'user_a',
            'password': 'pass1234!',
        })
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('token', resp.data)


class APIIsolamentoTests(APITestCase):
    def setUp(self):
        self.user_a = make_user('user_a')
        self.user_b = make_user('user_b')
        self.token_a = make_token(self.user_a)
        self.token_b = make_token(self.user_b)
        self.cat_a = make_cat(self.user_a, 'Salário A', 'E')
        self.cat_b = make_cat(self.user_b, 'Salário B', 'E')
        make_tx(self.user_a, self.cat_a, 500)

    def _auth(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_isolamento_leitura(self):
        # A vê 1 transação
        self._auth(self.token_a)
        resp = self.client.get('/api/transacoes/')
        self.assertEqual(len(resp.data), 1)

        # B vê 0 transações de A
        self._auth(self.token_b)
        resp = self.client.get('/api/transacoes/')
        self.assertEqual(len(resp.data), 0)

    def test_perform_create_injeta_usuario(self):
        self._auth(self.token_a)
        resp = self.client.post('/api/transacoes/', {
            'descricao': 'Nova',
            'valor': '200.00',
            'data': date.today().isoformat(),
            'categoria': self.cat_a.pk,
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        tx = Transacao.objects.get(pk=resp.data['id'])
        self.assertEqual(tx.usuario, self.user_a)

    def test_cross_write_categoria_bloqueado(self):
        # B tenta usar categoria de A → 400
        self._auth(self.token_b)
        resp = self.client.post('/api/transacoes/', {
            'descricao': 'Invasão',
            'valor': '100.00',
            'data': date.today().isoformat(),
            'categoria': self.cat_a.pk,
        })
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('categoria', resp.data)

    def test_categoria_propria_ok(self):
        self._auth(self.token_b)
        resp = self.client.post('/api/transacoes/', {
            'descricao': 'Minha tx',
            'valor': '50.00',
            'data': date.today().isoformat(),
            'categoria': self.cat_b.pk,
        })
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_tipo_display_na_resposta(self):
        cat_s = make_cat(self.user_a, 'Mercado', 'S')
        make_tx(self.user_a, cat_s, 100)
        self._auth(self.token_a)
        resp = self.client.get('/api/transacoes/')
        tipo_displays = [item['tipo_display'] for item in resp.data]
        self.assertIn('Entrada', tipo_displays)
        self.assertIn('Saída', tipo_displays)
