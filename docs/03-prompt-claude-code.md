# Prompt — Claude Code (backend + API)

> Cole no Claude Code, dentro do Codespace com os HTML do Claude Design já presentes.
> Use de forma iterativa: peça **um milestone por vez** (M1, depois M2…), revisando o código.

---

## Prompt mestre (contexto inicial — cole uma vez)

```
We are building a Django 5.2 academic project: a "Dashboard de Controle Financeiro
(a Personal Finance Dashboard called ACashController) for a 3-person group. UI text in pt-BR.
Database: SQLite. API: Django REST Framework with TokenAuthentication.
Charts: Chart.js (CDN, front-end only). PDF export: xhtml2pdf (pisa).

ARCHITECTURE (mirror the reference repo github.com/marcos-faino/ecommerce2026):
- 100% Class-Based Views (CBV). No function views.
- Reusable mixins in utils/my_mixins.py (e.g. GeraPDFMixin from the reference,
  plus a UsuarioQuerysetMixin that filters get_queryset by request.user and sets
  usuario = request.user on form_valid).
- Per-app templates folders + a central templates/base.html.
- Central core/urls.py using include() per app.
- Managers/Meta/__str__ on models, like the reference repo.

APPS:
- usuario  : registration (CreateView) + login/logout (Django auth views).
- financas : models Categoria, Transacao, MetaEconomia; CBV CRUD; balance validation.
- dashboard: aggregation views, Chart.js data, CSV + PDF export.
- api      : DRF serializers, viewsets, token auth, router.
- utils    : shared mixins.

MODELS (financas/models.py):
- Categoria(usuario FK, nome, tipo[E/S], cor hex, icone).
- Transacao(usuario FK, categoria FK, descricao, valor Decimal, data, criado).
  NOTE: Transacao has NO `tipo` field — the Entrada/Saída type is DERIVED from
  categoria.tipo (expose `tipo` and `tipo_display` as @property reading the
  category). clean() rejects valor <= 0.
- MetaEconomia(usuario FK, nome, valor_alvo, valor_atual, prazo, concluida) with
  a `progresso` property (used by the .goal-fill width and "% concluído" text).

TEMPLATES: the HTML screens from Claude Design already exist in the repo. Wire them
1:1 — do NOT redesign. Rename the files to Django convention and keep the CSS classes
and field ids as-is. See docs/07-mapa-telas-templates.md for the full screen→template
→url-name mapping. Generated `id_<field>` must match the form field names.

KEY BUSINESS RULES (the professor WILL ask about these — implement clearly):
1. Balance is DERIVED, never stored: saldo = sum(Entradas) - sum(Saídas) for the user, filtering by categoria__tipo.
2. Balance validation: when creating a SAÍDA, reject in TransacaoForm.clean() if
   saldo_usuario(user) < valor, raising ValidationError("Saldo insuficiente...").
   The type comes from the chosen categoria (categoria.tipo == 'S'), NOT from a
   field on Transacao. The form receives `usuario` via the view's get_form_kwargs().
3. Per-user isolation EVERYWHERE: LoginRequiredMixin on all private views +
   get_queryset() filtered by request.user. Same in DRF viewsets.

Always: keep code readable, in pt-BR for user-facing strings, with comments on the
tricky parts. Ask me before large refactors. Implement ONE milestone at a time when
I ask. Confirm you understood this context and wait for my first milestone request.
```

---

## Prompts por milestone (peça um de cada vez)

**M1 — modelos & admin**
```
Implement financas/models.py exactly as specified (Categoria[nome max_length=100,
tipo E/S, cor hex default #1D9E75, icone max_length=50 blank], Transacao,
MetaEconomia[nome, valor_alvo, valor_atual, prazo, concluida] with choices, Meta,
__str__, progresso property). Register all in financas/admin.py. Add a helper
saldo_usuario(user) in financas/services.py using aggregate(Sum) filtered by
categoria__tipo. Generate migrations. Seed example categories with colors/icons:
Salário(#1D9E75,briefcase) Freelance(#2E6FB7,laptop) [Entrada]; Alimentação
(#C25E3A,cart) Moradia(#7C3AED,home) Assinaturas(#D97706) Saúde(#DC2626,heart-pulse)
Transporte(#2E6FB7) Lazer(#8B5CF6) [Saída].
```

**M2 — auth & isolamento**
```
Implement usuario app: registration CreateView + login/logout via Django auth.
Create utils/my_mixins.py with UsuarioQuerysetMixin (filters get_queryset by
request.user; sets instance.usuario = request.user in form_valid). Keep the
GeraPDFMixin from the reference repo (xhtml2pdf). Wire URLs and LOGIN_URL.
```

**M3 — CRUD transações + validação de saldo**
```
Implement financas CBV CRUD for Transacao, Categoria, MetaEconomia using
ListView/CreateView/UpdateView/DeleteView + LoginRequiredMixin +
UsuarioQuerysetMixin. Build TransacaoForm with clean() that rejects a SAÍDA when
balance is insufficient (uses saldo_usuario). Pass `usuario` via get_form_kwargs().
URL names (used by the screens): transacoes, transacao_nova, transacao_editar<pk>,
transacao_excluir<pk>; categoria_list, categoria_nova, categoria_editar<pk>,
categoria_excluir<pk>; meta_nova, meta_editar<pk>, meta_excluir<pk>. The transacao
list has a GET filter form (mes/ano/q) + pagination (.pagination/.page-btn) — use
Django Paginator (page_obj). Integrate the existing HTML screens 1:1 (see doc 07).
```

**M4 — dashboard + Chart.js**
```
Implement dashboard.views.DashboardView (TemplateView) feeding dashboard.html.
The template ALREADY exists and expects EXACTLY these context vars (do not rename):
  saldo, total_entradas, total_saidas, mes_nome, ano,
  patrimonio_labels, patrimonio_data, cat_labels, cat_data, top_categorias.
- saldo derived (sum Entradas - sum Saídas, filter categoria__tipo).
- patrimonio_*: monthly accumulated net worth (TruncMonth + Sum).
- cat_*: expenses by category (values+annotate Sum), feed the doughnut (#chartCategorias).
- top_categorias: list of {nome, pct} for the "Top Categorias" progress bars (5 max).
Charts are Chart.js 4.4.0 (CDN) — the JS is inline in dashboard.html with canvas ids
chartPatrimonio (line) and chartCategorias (doughnut, cutout 62%). Just replace the
example arrays with {{ patrimonio_labels|safe }} etc. Use Categoria.cor for colors.
```

**M5 — exportação CSV + PDF**
```
Add dashboard ExportarCSVView (csv module, HttpResponse text/csv, monthly
statement) and ExportarPDFView using the GeraPDFMixin (template extrato_pdf.html).
Both filtered by month/year and by request.user. Add buttons on the dashboard.
```

**M6 — API DRF + Token**
```
Implement the api app: serializers for Transacao, Categoria, MetaEconomia.
ModelViewSets with authentication_classes=[TokenAuthentication],
permission_classes=[IsAuthenticated], and get_queryset filtered by request.user
(perform_create sets usuario=request.user). Register a DRF router. Add
obtain_auth_token endpoint at /api/token/. Add rest_framework and
rest_framework.authtoken to INSTALLED_APPS, run migrate. Show me curl examples to
get a token and list transactions.
```

**M7 — testes**
```
Write tests.py: (1) creating a SAÍDA above balance is rejected; (2) a user cannot
see another user's transactions (get_queryset isolation); (3) the API returns 401
without a token and 200 with a valid token. Keep them runnable with `manage.py test`.
```

---

### Boas práticas durante o uso
- Um milestone por vez, **commit a cada milestone** (mensagens claras = prova de autoria na arguição).
- Sempre rode `manage.py runserver` e teste manualmente antes de commitar.
- Se o Claude propuser refatoração grande, peça pra explicar antes — vocês precisam entender o código pra arguição.
