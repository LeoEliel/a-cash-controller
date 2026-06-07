from django import forms
from django.core.exceptions import ValidationError

from .models import Categoria, MetaEconomia, Transacao
from .services import saldo_usuario


class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['descricao', 'valor', 'data', 'categoria']
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Supermercado, Salário, Academia...',
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0,00',
                'min': '0.01',
                'step': '0.01',
            }),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
        qs = Categoria.objects.filter(usuario=usuario).order_by('tipo', 'nome')
        saidas = [(c.pk, c.nome) for c in qs if c.tipo == 'S']
        entradas = [(c.pk, c.nome) for c in qs if c.tipo == 'E']
        self.fields['categoria'].queryset = qs
        # Agrupa as opções por tipo para exibir <optgroup> no select
        self.fields['categoria'].widget.choices = [
            ('', 'Selecione uma categoria...'),
            ('Saídas', saidas),
            ('Entradas', entradas),
        ]

    def clean(self):
        cleaned = super().clean()
        categoria = cleaned.get('categoria')
        valor = cleaned.get('valor')
        if not (categoria and valor):
            return cleaned
        if categoria.tipo != 'S':
            return cleaned
        saldo = saldo_usuario(self.usuario)
        # Em edição, devolve o valor atual da saída ao saldo antes de validar
        if self.instance.pk and self.instance.categoria.tipo == 'S':
            saldo += self.instance.valor
        if saldo < valor:
            raise ValidationError(
                {'valor': f'Saldo insuficiente. Saldo disponível: R$ {saldo:.2f}.'}
            )
        return cleaned


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'tipo', 'cor', 'icone']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Alimentação, Salário, Transporte...',
            }),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cor': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'icone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: cart, home, briefcase, heart-pulse...',
            }),
        }


class MetaEconomiaForm(forms.ModelForm):
    class Meta:
        model = MetaEconomia
        fields = ['nome', 'valor_alvo', 'valor_atual', 'prazo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Fundo de Emergência, Viagem...',
            }),
            'valor_alvo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '20000.00',
                'min': '0',
                'step': '0.01',
            }),
            'valor_atual': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01',
            }),
            'prazo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
