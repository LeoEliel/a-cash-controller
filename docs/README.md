# ACashController — Documentação do Trabalho

> Trabalho final de Django • Grupo de 3 • Entrega 11/06/2026 (30 pts projeto + 20 pts arguição)

## Índice dos documentos

| # | Arquivo | O que tem |
|---|---|---|
| 00 | [00-estrutura-projeto.md](00-estrutura-projeto.md) | Estrutura de pastas espelhando o repo `ecommerce2026` |
| 01 | [01-plano-execucao.md](01-plano-execucao.md) | Plano, milestones, divisão entre as 3 pessoas |
| 02 | [02-modelagem-dados.md](02-modelagem-dados.md) | Models, relacionamentos, regra de saldo, dados dos gráficos |
| — | `diagrama_er.png` | Diagrama ER visual |
| 03a | [03-prompt-claude-design.md](03-prompt-claude-design.md) | Prompt pronto pro Claude Design (telas HTML) |
| 03b | [03-prompt-claude-code.md](03-prompt-claude-code.md) | Prompts pro Claude Code (backend + API), por milestone |
| 04 | [04-documentacao-iterativa.md](04-documentacao-iterativa.md) | Doc vivo: como o projeto funciona (pra arguição) |
| 05 | [05-perguntas-professor.md](05-perguntas-professor.md) | Banco de perguntas + respostas (os 20 pts) |
| 06 | [06-deploy-e-variaveis.md](06-deploy-e-variaveis.md) | Deploy (PythonAnywhere) + variáveis de ambiente (.env) |
| 07 | [07-mapa-telas-templates.md](07-mapa-telas-templates.md) | Mapa telas (Claude Design) → templates Django + URL names + ids dos campos |
| 08 | [08-prompt-claude-design-faltantes.md](08-prompt-claude-design-faltantes.md) | Prompt usado pra gerar as 3 telas faltantes (confirm_delete, meta_form, extrato_pdf) |

## Stack
Django 5.2 · SQLite · DRF + TokenAuthentication · Chart.js · xhtml2pdf · django-environ · GitHub Codespaces · Deploy: PythonAnywhere.

## Ordem sugerida de leitura
01 → 02 (+ diagrama) → 00 → 07 → 03a → 03b → 04 → 05 → 06. (08 é referência do prompt de design.)

> **Status das telas:** **12 telas completas** geradas no Claude Design + `styles.css` (design system: green #1D9E75, blue #2E6FB7, red/expense #C25E3A, fonte Poppins). HTMLs originais em `telas/`. Decisão do grupo: docs mandam na convenção de nomes Django — as telas são renomeadas pra bater (ver doc 07). Pacote pronto pra alimentar o **Claude Code** (doc 03b).
