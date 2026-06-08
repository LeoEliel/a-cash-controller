from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class CadastroTests(TestCase):
    def test_cadastro_cria_usuario(self):
        resp = self.client.post(reverse('cadastro'), {
            'username': 'novouser',
            'email': 'novo@example.com',
            'password1': 'SenhaForte123!',
            'password2': 'SenhaForte123!',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username='novouser').exists())


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('loginuser', password='pass1234!')

    def test_login_valido(self):
        resp = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'pass1234!',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_encerra_sessao(self):
        self.client.login(username='loginuser', password='pass1234!')
        self.client.post(reverse('logout'))
        self.assertNotIn('_auth_user_id', self.client.session)


class PaginasProtegidasTests(TestCase):
    def test_paginas_protegidas_redirecionam(self):
        urls = [
            reverse('dashboard'),
            reverse('transacoes'),
            reverse('categoria_list'),
            reverse('metas'),
        ]
        for url in urls:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 302, f'{url} deveria redirecionar')
            self.assertIn('/login/', resp['Location'], f'{url} deveria ir para /login/')
