# Modelagem de Dados — ACashController

> Diagrama visual: `docs/diagrama_er.png`

## Resumo das entidades

| Entidade | App | Papel |
|---|---|---|
| `User` | `django.contrib.auth` (nativo) | Dono de todos os dados. Não criamos — usamos o de Django. |
| `Token` | `rest_framework.authtoken` | 1:1 com User. Autentica chamadas da API. |
| `Categoria` | `financas` | Classifica transações (Entrada ou Saída). Por usuário. |
| `Transacao` | `financas` | Lançamento financeiro (E/S), valor, data, categoria. Por usuário. |
| `MetaEconomia` | `financas` | Meta de economia com valor-alvo e progresso. Por usuário. |

## Relacionamentos

- `User 1 — N Categoria`
- `User 1 — N Transacao`
- `User 1 — N MetaEconomia`
- `Categoria 1 — N Transacao`
- `User 1 — 1 Token` (DRF)

> **Decisão de modelagem (importante para a arguição):** o campo **`tipo` (Entrada/Saída) fica APENAS na `Categoria`**, não na `Transacao`. Como toda transação aponta para uma categoria (1:N), o tipo do lançamento é **derivado** de `transacao.categoria.tipo`. Guardar `tipo` também na `Transacao` seria **redundância** e poderia gerar **inconsistência** (uma transação 'S' apontando para uma categoria 'E'). Por isso `Transacao` expõe `tipo`/`tipo_display` como `@property` que leem a categoria — sem coluna duplicada no banco (modelo normalizado).

Tudo amarrado ao `User` → garante o isolamento por usuário exigido no enunciado.

---

## Models (Django) — referência de implementação

> Espelha o estilo do repo de referência: managers customizados, `Meta`, `__str__`, `verbose_name`.

```python
# financas/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class TipoTransacao(models.TextChoices):
    ENTRADA = 'E', 'Entrada'
    SAIDA = 'S', 'Saída'


class Categoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='categorias')
    nome = models.CharField(max_length=100)                   # tela: maxlength=100
    tipo = models.CharField(max_length=1, choices=TipoTransacao.choices)
    cor = models.CharField(max_length=7, default='#1D9E75')   # hex p/ Chart.js (input type=color)
    icone = models.CharField(max_length=50, blank=True)       # tela: maxlength=50, opcional (ex.: cart, home)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']
        unique_together = ('usuario', 'nome', 'tipo')

    def __str__(self):
        return f'{self.nome} ({self.get_tipo_display()})'


class Transacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='transacoes')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT,
                                  related_name='transacoes')
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
        # Tipo é DERIVADO da categoria — não há campo duplicado em Transacao.
        return self.categoria.tipo

    @property
    def tipo_display(self):
        return self.categoria.get_tipo_display()

    def clean(self):
        if self.valor is None or self.valor <= 0:
            raise ValidationError({'valor': 'O valor deve ser maior que zero.'})


class MetaEconomia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='metas')
    nome = models.CharField(max_length=120)                   # tela usa .goal-name = "nome"
    valor_alvo = models.DecimalField(max_digits=12, decimal_places=2)
    valor_atual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prazo = models.DateField(null=True, blank=True)           # tela: "Prazo: dd/mm/yyyy"
    concluida = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Meta de Economia'
        verbose_name_plural = 'Metas de Economia'
        ordering = ['concluida', 'prazo']

    def __str__(self):
        return self.nome

    @property
    def progresso(self):
        # usado no template: width do .goal-fill e texto "{{ progresso }}% concluído"
        if not self.valor_alvo:
            return 0
        return min(100, round((self.valor_atual / self.valor_alvo) * 100, 1))
```

---

## Regra de negócio: cálculo de saldo e validação

O **saldo** não é armazenado — é **derivado** das transações (fonte única de verdade, evita inconsistência):

```python
# saldo = soma(Entradas) - soma(Saídas) do usuário
from django.db.models import Sum, Q

def saldo_usuario(user):
    entradas = user.transacoes.filter(categoria__tipo='E').aggregate(s=Sum('valor'))['s'] or 0
    saidas   = user.transacoes.filter(categoria__tipo='S').aggregate(s=Sum('valor'))['s'] or 0
    return entradas - saidas
```

**Validação ao lançar uma Saída** (no form ou na view):

```python
# financas/forms.py — dentro do clean()
def clean(self):
    cleaned = super().clean()
    categoria = cleaned.get('categoria')
    valor = cleaned.get('valor')
    # O tipo (E/S) NÃO está na transação: é derivado da categoria escolhida.
    if categoria and valor and categoria.tipo == 'S':
        if saldo_usuario(self.usuario) < valor:
            raise ValidationError('Saldo insuficiente para esta saída.')
    return cleaned
```

> O `self.usuario` é injetado pela view via `get_form_kwargs()`. Esse é o ponto que o professor provavelmente vai cobrar — todos devem saber explicar **onde** e **por que** a validação acontece no form e não no model.

---

## Categorias de exemplo (seed)

> Alinhado às telas (`categorias.html` / `transacoes.html` / dashboard "Top Categorias"). `cor` em hex porque alimenta o Chart.js e o swatch da listagem.

| Nome | Tipo | Cor (hex) | Ícone |
|---|---|---|---|
| Salário | Entrada | #1D9E75 | briefcase |
| Freelance | Entrada | #2E6FB7 | laptop |
| Alimentação | Saída | #C25E3A | cart |
| Moradia | Saída | #7C3AED | home |
| Assinaturas | Saída | #D97706 | — |
| Saúde | Saída | #DC2626 | heart-pulse |
| Transporte | Saída | #2E6FB7 | — |
| Lazer | Saída | #8B5CF6 | — |

---

## Dados para os gráficos (context vars EXATAS das telas)

A `dashboard.html` espera estes nomes no contexto da `DashboardView` (não renomear — as telas já referenciam):

| Context var | Tipo | Onde é usada na tela |
|---|---|---|
| `saldo` | Decimal | `.stat-card.blue` → `R$ {{ saldo\|floatformat:2 }}` |
| `total_entradas` | Decimal | `.stat-card.green` |
| `total_saidas` | Decimal | `.stat-card.red` |
| `mes_nome`, `ano` | str/int | `.stat-sub` → "Junho 2026" |
| `patrimonio_labels` | list (JSON) | gráfico de **linha** `canvas#chartPatrimonio` |
| `patrimonio_data` | list (JSON) | idem |
| `cat_labels` | list (JSON) | gráfico de **rosca** `canvas#chartCategorias` |
| `cat_data` | list (JSON) | idem |
| `top_categorias` | list de dicts | barras de progresso "Top Categorias" (`{nome, pct}`) |

> No template os JSON entram com `{{ patrimonio_labels|safe }}` etc. (ou via `json_script`). Chart.js **4.4.0** via CDN (`chart.umd.min.js`). O `cutout: '62%'` faz a rosca.

**Linha (evolução mensal do patrimônio):**
```python
from django.db.models.functions import TruncMonth
from django.db.models import Sum

(Transacao.objects.filter(usuario=user)
    .annotate(mes=TruncMonth('data'))
    .values('mes', 'categoria__tipo')
    .annotate(total=Sum('valor'))
    .order_by('mes'))
# no Python: acumular (entradas - saídas) mês a mês = patrimônio acumulado
# -> alimenta patrimonio_labels (['Jan','Fev',...]) e patrimonio_data ([12000,...])
```

**Rosca/pizza (gastos por categoria) + Top Categorias:**
```python
gastos = (Transacao.objects.filter(usuario=user, categoria__tipo='S')
    .values('categoria__nome', 'categoria__cor')
    .annotate(total=Sum('valor'))
    .order_by('-total'))
# cat_labels  = [g['categoria__nome'] for g in gastos]
# cat_data    = [g['total'] for g in gastos]   (ou % do total de saídas)
# top_categorias = mesmos dados convertidos em [{'nome':..., 'pct':...}]  (5 maiores)
```
Esses resultados viram JSON e alimentam o Chart.js + as barras de progresso.
