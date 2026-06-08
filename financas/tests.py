from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from .forms import TransacaoForm
from .models import Categoria, MetaEconomia, Transacao
from .services import saldo_usuario


def make_user(username='tester', password='pass1234!'):
    return User.objects.create_user(username=username, password=password)


def make_cats(user):
    cat_e = Categoria.objects.create(usuario=user, nome='Salário', tipo='E')
    cat_s = Categoria.objects.create(usuario=user, nome='Mercado', tipo='S')
    return cat_e, cat_s


class ModelTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.cat_e, self.cat_s = make_cats(self.user)

    def test_transacao_tipo_property(self):
        t_e = Transacao(usuario=self.user, categoria=self.cat_e,
                        descricao='x', valor=100, data=date.today())
        self.assertEqual(t_e.tipo, 'E')
        self.assertEqual(t_e.tipo_display, 'Entrada')

        t_s = Transacao(usuario=self.user, categoria=self.cat_s,
                        descricao='x', valor=100, data=date.today())
        self.assertEqual(t_s.tipo, 'S')
        self.assertEqual(t_s.tipo_display, 'Saída')

    def test_transacao_clean_valor_zero_ou_negativo(self):
        for v in (0, -10):
            t = Transacao(usuario=self.user, categoria=self.cat_e,
                          descricao='x', valor=v, data=date.today())
            with self.assertRaises(ValidationError) as cm:
                t.clean()
            self.assertIn('valor', cm.exception.message_dict)

    def test_transacao_clean_valor_none_nao_quebra(self):
        t = Transacao(usuario=self.user, categoria=self.cat_e,
                      descricao='x', valor=None, data=date.today())
        t.clean()  # não deve levantar

    def test_categoria_unique_together(self):
        with self.assertRaises(IntegrityError):
            Categoria.objects.create(usuario=self.user, nome='Salário', tipo='E')

    def test_categoria_str(self):
        self.assertEqual(str(self.cat_e), 'Salário (Entrada)')
        self.assertEqual(str(self.cat_s), 'Mercado (Saída)')

    def test_meta_str(self):
        meta = MetaEconomia.objects.create(
            usuario=self.user, nome='Viagem', valor_alvo=5000)
        self.assertEqual(str(meta), 'Viagem')

    def test_meta_progresso(self):
        meta = MetaEconomia(valor_alvo=1000, valor_atual=500)
        self.assertEqual(meta.progresso, 50.0)

        meta.valor_atual = 2000
        self.assertEqual(meta.progresso, 100)

        meta.valor_alvo = 0
        self.assertEqual(meta.progresso, 0)


class SaldoServiceTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.cat_e, self.cat_s = make_cats(self.user)

    def _tx(self, cat, valor):
        return Transacao.objects.create(
            usuario=self.user, categoria=cat,
            descricao='test', valor=valor, data=date.today())

    def test_saldo_sem_transacoes(self):
        self.assertEqual(saldo_usuario(self.user), 0)

    def test_saldo_entradas_menos_saidas(self):
        self._tx(self.cat_e, 5000)
        self._tx(self.cat_s, 300)
        self.assertEqual(saldo_usuario(self.user), Decimal('4700'))

    def test_saldo_isolado_por_usuario(self):
        outro = make_user('outro')
        cat_outro = Categoria.objects.create(usuario=outro, nome='Salário', tipo='E')
        Transacao.objects.create(
            usuario=outro, categoria=cat_outro,
            descricao='não meu', valor=9999, data=date.today())
        self.assertEqual(saldo_usuario(self.user), 0)


class TransacaoFormTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.cat_e, self.cat_s = make_cats(self.user)

    def _form(self, valor, cat, instance=None):
        data = {
            'descricao': 'Teste',
            'valor': str(valor),
            'data': date.today().isoformat(),
            'categoria': cat.pk,
        }
        return TransacaoForm(data, usuario=self.user, instance=instance)

    def _tx(self, cat, valor):
        return Transacao.objects.create(
            usuario=self.user, categoria=cat,
            descricao='test', valor=valor, data=date.today())

    def test_form_valido_entrada(self):
        self.assertTrue(self._form(1000, self.cat_e).is_valid())

    def test_saida_dentro_do_saldo_valida(self):
        self._tx(self.cat_e, 5000)
        self.assertTrue(self._form(300, self.cat_s).is_valid())

    def test_saida_acima_do_saldo_invalida(self):
        self._tx(self.cat_e, 100)
        form = self._form(500, self.cat_s)
        self.assertFalse(form.is_valid())
        self.assertIn('valor', form.errors)
        self.assertIn('Saldo insuficiente', form.errors['valor'][0])

    def test_edicao_saida_devolve_valor_ao_saldo(self):
        # Saldo = 1000 - 900 = 100; editar a saída com o mesmo valor deve ser válido
        self._tx(self.cat_e, 1000)
        saida = self._tx(self.cat_s, 900)
        form = self._form(900, self.cat_s, instance=saida)
        self.assertTrue(form.is_valid(), form.errors)

    def test_categoria_queryset_filtrado_por_usuario(self):
        outro = make_user('outro')
        Categoria.objects.create(usuario=outro, nome='Salário', tipo='E')
        form = TransacaoForm(usuario=self.user)
        pks = list(form.fields['categoria'].queryset.values_list('pk', flat=True))
        self.assertIn(self.cat_e.pk, pks)
        self.assertIn(self.cat_s.pk, pks)
        # categorias do outro usuário não aparecem
        outro_pks = Categoria.objects.filter(usuario=outro).values_list('pk', flat=True)
        for pk in outro_pks:
            self.assertNotIn(pk, pks)
