from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class TipoTransacao(models.TextChoices):
    ENTRADA = 'E', 'Entrada'
    SAIDA = 'S', 'Saída'


class Categoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categorias')
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=1, choices=TipoTransacao.choices)
    cor = models.CharField(max_length=7, default='#1D9E75')
    icone = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']
        unique_together = ('usuario', 'nome', 'tipo')

    def __str__(self):
        return f'{self.nome} ({self.get_tipo_display()})'


class Transacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transacoes')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='transacoes')
    descricao = models.CharField(max_length=160)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data = models.DateField()
    criado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-data', '-criado']

    def __str__(self):
        return f'{self.tipo_display} | {self.descricao} | R$ {self.valor}'

    @property
    def tipo(self):
        return self.categoria.tipo

    @property
    def tipo_display(self):
        return self.categoria.get_tipo_display()

    def clean(self):
        super().clean()
        if self.valor is not None and self.valor <= 0:
            raise ValidationError({'valor': 'O valor deve ser maior que zero.'})


class MetaEconomia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metas')
    nome = models.CharField(max_length=120)
    valor_alvo = models.DecimalField(max_digits=12, decimal_places=2)
    valor_atual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prazo = models.DateField(null=True, blank=True)
    concluida = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Meta de Economia'
        verbose_name_plural = 'Metas de Economia'
        ordering = ['concluida', 'prazo']

    def __str__(self):
        return self.nome

    @property
    def progresso(self):
        if not self.valor_alvo:
            return 0
        return min(100, round((self.valor_atual / self.valor_alvo) * 100, 1))
