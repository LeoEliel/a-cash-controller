# Plano de Execução — ACashController

> **ACashController** — Aplicação de controle financeiro pessoal
> Trabalho final • Django • Grupo de 3 pessoas
> **Entrega:** 11/06/2026 — 30 pts (projeto) + 20 pts (perguntas orais)

---

## 1. Visão geral

Aplicação web Django para **controle de receitas, despesas e metas de economia**, com:

- Lançamento de transações categorizadas (Entradas/Saídas) via **CBV**, com **validação de saldo**.
- **Dashboard** com gráfico de linha (evolução mensal do patrimônio) + gráfico de pizza (gastos por categoria) usando **Chart.js**.
- Exportação de **extrato mensal em CSV e PDF**.
- **API REST** (DRF) protegida por **TokenAuthentication**.
- Isolamento por usuário: `LoginRequiredMixin` + filtragem em `get_queryset()`.

### Stack fechada
| Camada | Escolha |
|---|---|
| Framework | Django **5.2** |
| Banco | **SQLite** |
| API | **Django REST Framework** + TokenAuthentication |
| Gráficos | **Chart.js** (front, via CDN) |
| PDF | **xhtml2pdf** (pisa) — mesmo do repo de referência |
| Ambiente | **GitHub Codespaces** + repo novo no GitHub |
| Design | **Claude Design** (telas HTML) → **Claude Code** (backend/API) |

### Espelhando o repo de referência
Arquitetura igual a `github.com/marcos-faino/ecommerce2026`:
- Projeto Django multi-app, **views 100% CBV**.
- Mixins reutilizáveis em `utils/my_mixins.py` (ex.: `GeraPDFMixin`).
- Cada app com seus próprios `templates/<app>/`, `base.html` central.
- `settings.py` central, URLs incluídas por app via `include()`.

---

## 2. Divisão de apps Django

| App | Responsabilidade |
|---|---|
| `usuario` | Cadastro, login/logout, perfil. Reaproveita auth nativo. |
| `financas` | Núcleo: models `Categoria`, `Transacao`, `MetaEconomia`, CBVs de CRUD + validação de saldo. |
| `dashboard` | Views agregadoras: cálculo de saldo, séries mensais, dados pros gráficos, exportação CSV/PDF. |
| `api` | DRF: serializers, viewsets, rotas, TokenAuthentication. |
| `utils` | Mixins compartilhados (`GeraPDFMixin`, `UsuarioQuerysetMixin`). |

> Pode-se mesclar `dashboard` dentro de `financas` se o professor preferir menos apps. Mantemos separado para clareza de responsabilidades (alinha com SOLID/SRP — bom argumento na arguição).

---

## 3. Milestones (com checklist)

### M0 — Setup (Dia 1)
- [ ] Criar repo novo no GitHub + abrir Codespace.
- [ ] `python -m venv venv` / `requirements.txt`.
- [ ] `django-admin startproject core .`
- [ ] Criar apps: `usuario`, `financas`, `dashboard`, `api`, pasta `utils`.
- [ ] Registrar apps + `rest_framework` + `rest_framework.authtoken` em `INSTALLED_APPS`.
- [ ] `.gitignore` (.env, db.sqlite3, staticfiles) + `.env.example`.
- [ ] Primeiro commit + push na `main`.

### M1 — Modelagem & banco (Dia 1-2)
- [ ] Models `Categoria`, `Transacao`, `MetaEconomia` (ver `02-modelagem-dados.md`).
- [ ] Manager customizado por usuário (espelha `ProdutosDisponiveisManager`).
- [ ] `makemigrations` + `migrate`.
- [ ] Registrar no `admin.py` de cada app.
- [ ] Criar superuser + dados de teste (categorias: alimentação, moradia, assinaturas, salário, saúde…).

### M2 — Auth & isolamento por usuário (Dia 2)
- [ ] Views de login/logout (auth nativo) + cadastro (`CreateView`).
- [ ] `LoginRequiredMixin` em todas as views privadas.
- [ ] `UsuarioQuerysetMixin` filtrando `get_queryset()` por `request.user`.
- [ ] `form_valid()` setando `usuario = request.user` no save.

### M3 — CRUD de transações + validação de saldo (Dia 2-3)
- [ ] `TransacaoListView`, `CreateView`, `UpdateView`, `DeleteView`.
- [ ] CRUD de `Categoria` e `MetaEconomia`.
- [ ] **Validação de saldo**: ao lançar Saída, recusar se saldo insuficiente (no `form.clean()` ou `form_valid()`), com `messages.error`.

### M4 — Dashboard + gráficos (Dia 3-4)
- [ ] `DashboardView (TemplateView)` calculando saldo, totais e séries.
- [ ] Agregações com `TruncMonth` + `Sum` (evolução mensal) e `values('categoria').annotate(Sum)` (pizza).
- [ ] Endpoints JSON (ou contexto serializado) consumidos pelo Chart.js.
- [ ] Front: Chart.js (linha + pizza) via CDN.

### M5 — Exportação CSV/PDF (Dia 4)
- [ ] Extrato CSV (`csv` + `HttpResponse content_type=text/csv`).
- [ ] Extrato PDF reaproveitando `GeraPDFMixin` (xhtml2pdf) — template `extrato_pdf.html`.
- [ ] Filtro por mês/ano.

### M6 — API DRF + Token (Dia 5)
- [ ] Serializers de `Transacao`/`Categoria`/`MetaEconomia`.
- [ ] ViewSets com `permission_classes=[IsAuthenticated]` e `authentication_classes=[TokenAuthentication]`.
- [ ] `get_queryset()` filtrando por `self.request.user`.
- [ ] Endpoint `obtain_auth_token` para emitir token.
- [ ] Testar com `curl`/Postman.

### M7 — Telas (Claude Design) + polish (Dia 5-6)
- [ ] Gerar HTML das telas no Claude Design → integrar nos templates.
- [ ] `base.html`, navbar, mensagens, responsivo.
- [ ] Revisar UX do dashboard.

### M9 — Variáveis de ambiente & deploy (Dia 7) — opcional
- [ ] `django-environ` + `.env` / `.env.example` (segredos fora do Git).
- [ ] `DATABASES` lendo `DATABASE_URL`; `STATIC_ROOT` + `collectstatic`.
- [ ] Deploy no **PythonAnywhere** (free, SQLite persistente). Ver `06-deploy-e-variaveis.md`.
- [ ] `DEBUG=False` + `ALLOWED_HOSTS` em produção.

### M8 — Testes, docs & ensaio da arguição (Dia 6-7)
- [ ] Testes básicos (`tests.py`): validação de saldo, isolamento de queryset, auth da API.
- [ ] Fechar a documentação iterativa (`04-documentacao-iterativa.md`).
- [ ] Cada integrante domina sua parte + simulação de perguntas (`05-perguntas-professor.md`).
- [ ] README com instruções de rodar.

---

## 4. Divisão entre as 3 pessoas (sugestão)

| Pessoa | Frente | Apps/arquivos |
|---|---|---|
| **Dev A** | Modelos + CRUD + validação de saldo | `financas/models.py`, `financas/views.py`, forms |
| **Dev B** | Dashboard + gráficos + exportação CSV/PDF | `dashboard/`, `utils/my_mixins.py`, templates de gráfico |
| **Dev C** | API DRF + Token + Auth/isolamento + testes | `api/`, `usuario/`, `tests.py` |

> Todos revisam o código dos outros (cada um precisa saber explicar **tudo** na arguição — ver doc 05).

---

## 5. Fluxo de trabalho com Claude Design + Claude Code

```
Claude Design  →  telas HTML simples (base, dashboard, lista, form, extrato)
        │
        ▼
Claude Code    →  backend Django (models, CBVs, mixins) + API DRF + Chart.js wiring
        │
        ▼
GitHub Codespaces  →  rodar, testar, commitar (push main)
```

1. **Claude Design**: usar o prompt do doc `03-prompt-claude-design.md` para gerar o HTML estático das telas.
2. **Claude Code**: usar o prompt do doc `03-prompt-claude-code.md` para implementar o backend e ligar os dados aos templates/gráficos.
3. Sempre commitar por milestone. Mensagens claras (servem de prova de autoria na arguição).

---

## 6. Critérios de avaliação → onde cada ponto é coberto

| Requisito do enunciado | Onde é atendido | Milestone |
|---|---|---|
| CBV para lançamento de transações categorizadas | `financas/views.py` (CreateView etc.) | M3 |
| Validação de saldo suficiente | `form.clean()` / `form_valid()` | M3 |
| Dashboard linha (patrimônio mensal) | `dashboard` + Chart.js | M4 |
| Pizza (gastos por categoria) | `dashboard` + Chart.js | M4 |
| Exportação CSV ou PDF | CSV + `GeraPDFMixin` | M5 |
| API consumível de transações | `api/` DRF ViewSet | M6 |
| Token Authentication | DRF `TokenAuthentication` | M6 |
| Cada usuário só vê seus dados | `LoginRequiredMixin` + `get_queryset` | M2 |

Cobrimos **100%** do enunciado, com folga (PDF **e** CSV).
