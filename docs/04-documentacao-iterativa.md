# Documentação Iterativa do Projeto

> Documento vivo. Atualizem a cada milestone concluído. Serve para que **os 3** entendam
> o projeto inteiro e consigam responder o professor (20 pts da arguição).
>
> Regra do grupo: ninguém commita uma feature sem registrar aqui **o que faz, onde está e por quê**.

---

## Como funciona o projeto (visão de cima)

O usuário se cadastra e faz login. A partir daí, ele:
1. Cria **categorias** (Entrada ou Saída): Salário, Alimentação, Moradia…
2. Lança **transações** vinculadas a uma categoria. Saídas só passam se houver **saldo**.
3. Vê o **dashboard**: saldo, gráfico de linha (patrimônio mês a mês) e pizza (gastos por categoria).
4. Define **metas de economia** com barra de progresso.
5. Exporta o **extrato mensal** em CSV ou PDF.
6. (Opcional) Consome os dados via **API REST**, autenticando com **token**.

Tudo é isolado por usuário: ninguém vê dado de ninguém.

---

## Fluxo de uma requisição (request → response)

```
Navegador
   │  GET /transacoes/
   ▼
core/urls.py  ──include──►  financas/urls.py  ──►  TransacaoListView (CBV)
   │
   ├─ LoginRequiredMixin  → exige usuário logado (senão redireciona p/ login)
   ├─ get_queryset()      → filtra Transacao.objects.filter(usuario=request.user)
   ▼
template financas/transacao_list.html  →  HTML renderizado
```

Para um POST de nova transação:
```
POST /transacoes/nova/ → TransacaoCreateView
   ├─ get_form_kwargs() injeta usuario=request.user no form
   ├─ form.clean()  → se categoria.tipo='S' e saldo < valor → ValidationError("Saldo insuficiente")
   ├─ form_valid()  → seta instance.usuario = request.user e salva
   ▼
redirect para a lista + messages.success
```

---

## Decisões de arquitetura (e o porquê)

| Decisão | Por quê (argumento na arguição) |
|---|---|
| **CBV em tudo** | Reuso e organização; mixins evitam repetição (DRY/SRP). Enunciado exige CBV. |
| **Saldo derivado, não armazenado** | Fonte única de verdade; impossível ficar inconsistente. Recalculado com `Sum`. |
| **Validação no Form, não no Model** | A regra depende do **usuário logado** (contexto da request), que o model não conhece. O form recebe `usuario` da view. |
| **Mixin `UsuarioQuerysetMixin`** | Centraliza o isolamento por usuário em um lugar só (DRY). |
| **`GeraPDFMixin` (xhtml2pdf)** | Reaproveitado do repo de referência; gera PDF a partir de template HTML. |
| **DRF para a API** | Token auth pronto, serializers e viewsets reduzem boilerplate. |
| **Chart.js no front** | Gráficos leves; o Django só fornece o JSON, separando dados de apresentação. |
| **Apps separados** | Cada app tem uma responsabilidade (SRP): `financas` (domínio), `dashboard` (relatórios), `api` (integração), `usuario` (auth). |

---

## Mapa: requisito do enunciado → arquivo/linha

| Requisito | Onde está |
|---|---|
| CBV de lançamento categorizado | `financas/views.py → TransacaoCreateView` |
| Validação de saldo | `financas/forms.py → TransacaoForm.clean()` + `financas/services.py → saldo_usuario()` |
| Gráfico de linha (patrimônio) | `dashboard/views.py → DashboardView` + `static/js/charts.js` |
| Gráfico de pizza (categorias) | idem |
| Exportar CSV | `dashboard/views.py → ExportarCSVView` |
| Exportar PDF | `dashboard/views.py → ExportarPDFView` + `utils/my_mixins.py → GeraPDFMixin` |
| API de transações | `api/views.py → TransacaoViewSet` + `api/serializers.py` |
| Token Authentication | `api/views.py (authentication_classes)` + `/api/token/` |
| Isolamento por usuário (web) | `LoginRequiredMixin` + `get_queryset()` em `financas/views.py` |
| Isolamento por usuário (API) | `TransacaoViewSet.get_queryset()` filtra por `request.user` |

> **Atualizem a coluna "Onde está" com os nomes/linhas reais** conforme implementam.

---

## Glossário rápido (pra não travar na pergunta)

- **CBV (Class-Based View):** view escrita como classe; herda comportamento de classes prontas do Django (ListView, CreateView…).
- **Mixin:** classe pequena com um comportamento isolado que você "mistura" em outras classes via herança múltipla.
- **`get_queryset()`:** método que define **quais objetos** a view enxerga. Filtramos por `request.user`.
- **`LoginRequiredMixin`:** bloqueia a view para quem não está logado.
- **Serializer (DRF):** converte objetos do model em JSON (e valida JSON de entrada).
- **TokenAuthentication:** cada usuário tem um token; a API exige `Authorization: Token <chave>`.
- **`TruncMonth` / `Sum`:** funções de agregação do ORM para somar valores por mês.

---

## Log de progresso (preencher por milestone)

| Data | Milestone | Quem | Notas / decisões |
|---|---|---|---|
| | M1 modelos | | |
| | M2 auth/isolamento | | |
| | M3 CRUD + saldo | | |
| | M4 dashboard | | |
| | M5 export CSV/PDF | | |
| | M6 API DRF | | |
| | M7 testes | | |
