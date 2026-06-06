# ACashController

**Dashboard de Controle Financeiro Pessoal** — trabalho final (Django).

Aplicação web para controle de finanças pessoais: lançamento de transações (Entradas/Saídas) por categoria, dashboard com gráficos de evolução patrimonial e gastos por categoria, metas de economia, exportação de extrato (CSV/PDF) e API REST autenticada.

## Stack

- **Backend:** Django 5.x (100% Class-Based Views)
- **Banco:** SQLite
- **API:** Django REST Framework + TokenAuthentication
- **Gráficos:** Chart.js 4.4.0
- **Fonte/UI:** Poppins, design system verde `#1D9E75`
- **Deploy:** PythonAnywhere (free tier, SQLite persistente)

## Requisitos do trabalho

- CBVs para transações categorizadas (Entradas/Saídas) com validação de saldo
- Dashboard: gráfico de linha (patrimônio mensal) + pizza (gastos por categoria)
- Exportação de extrato mensal em CSV e PDF
- API DRF com TokenAuthentication
- Isolamento de dados por usuário (`LoginRequiredMixin` + `get_queryset` filtrado)

## Estrutura do repositório

```
docs/    → documentação completa do projeto (ler README de docs primeiro)
telas/   → protótipos HTML das telas + styles.css (gerados no Claude Design)
```

> O projeto Django ainda **não foi scaffoldado**. Ele será criado do zero seguindo os
> milestones em `docs/03-prompt-claude-code.md`, usando os prompts de cada etapa.

## Como começar (no Codespaces)

1. Abra este repo em um **Codespace** (Code → Codespaces → Create codespace on main).
2. Leia `docs/README.md` para a ordem de leitura.
3. Rode os milestones com o Claude Code, começando pela **M0** (setup do ambiente).

## Documentação

Veja [`docs/README.md`](docs/README.md) para a ordem de leitura completa.
O PDF consolidado está em `Documentacao-Trabalho-ACashController.pdf`.

## Equipe

Grupo de 3 pessoas — trabalho final da disciplina.
