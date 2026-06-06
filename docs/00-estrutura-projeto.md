# Estrutura do Projeto (espelhando ecommerce2026)

```
acashcontroller/
├── manage.py
├── requirements.txt
├── .env_vazio                 # modelo de variáveis (igual ao repo de ref.)
├── README.md
│
├── core/                      # projeto Django (settings central)
│   ├── __init__.py
│   ├── settings.py            # INSTALLED_APPS, DRF, auth, static, templates
│   ├── urls.py                # include() de cada app + admin + api
│   ├── asgi.py
│   └── wsgi.py
│
├── utils/                     # mixins reutilizáveis (igual repo ref.)
│   └── my_mixins.py           # GeraPDFMixin, UsuarioQuerysetMixin
│
├── usuario/                   # auth: cadastro, login, logout
│   ├── views.py               # CBV (CreateView de cadastro)
│   ├── forms.py
│   ├── urls.py
│   ├── tests.py
│   └── templates/
│       ├── registration/
│       │   ├── login.html
│       │   └── logout.html
│       └── usuario/
│           └── cadusuario.html
│
├── financas/                  # núcleo: categorias, transações, metas
│   ├── models.py              # Categoria(tem tipo E/S), Transacao(tipo derivado), MetaEconomia
│   ├── views.py               # CBV CRUD + validação de saldo
│   ├── forms.py               # TransacaoForm (clean: valida saldo)
│   ├── admin.py
│   ├── urls.py
│   ├── managers.py            # managers customizados (opcional)
│   ├── tests.py               # teste de validação de saldo + isolamento
│   ├── migrations/
│   └── templates/financas/
│       ├── transacao_list.html
│       ├── transacao_form.html
│       ├── transacao_confirm_delete.html
│       ├── categoria_list.html
│       ├── categoria_form.html
│       ├── meta_list.html
│       └── meta_form.html
│
├── dashboard/                 # agregações, gráficos, exportação
│   ├── views.py               # DashboardView, ExportarCSVView, ExportarPDFView
│   ├── urls.py
│   ├── tests.py
│   └── templates/dashboard/
│       ├── dashboard.html     # Chart.js (linha + pizza)
│       └── extrato_pdf.html   # template do PDF (xhtml2pdf)
│
├── api/                       # DRF + TokenAuthentication
│   ├── serializers.py
│   ├── views.py               # ViewSets (get_queryset por usuário)
│   ├── urls.py                # router + obtain_auth_token
│   └── tests.py               # teste de auth da API
│
├── templates/
│   └── base.html              # layout central, navbar, messages
│
└── static/
    ├── css/styles.css
    └── js/charts.js           # init do Chart.js consumindo o JSON do dashboard
```

## Pontos de paralelo com o repo de referência

| ecommerce2026 | nosso projeto |
|---|---|
| `utils/my_mixins.py` (`GeraPDFMixin`) | mesmo arquivo, mesmo mixin para o PDF |
| `catalogo/models.py` (manager `disponiveis`) | `financas/managers.py` (filtro por usuário) |
| views 100% CBV | idem |
| `templates/<app>/` por app + `base.html` | idem |
| `urls.py` central com `include()` | idem |
| Django 5.2 + `i18n_patterns` | Django 5.2 (i18n opcional — pode dispensar) |

## requirements.txt (base)

```
Django==5.2
djangorestframework==3.15.2
xhtml2pdf==0.2.17
pillow==12.1.1
python-environ==0.4.54
```

> Chart.js entra por **CDN** no template — não é dependência Python.
