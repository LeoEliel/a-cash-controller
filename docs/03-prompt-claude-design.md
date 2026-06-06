# Prompt — Claude Design (telas HTML)

> Cole no Claude Design. Gera o HTML estático das telas; depois o Claude Code integra com Django.

---

```
You are designing the HTML/CSS screens for a Django academic project:
a Personal Finance Control Dashboard called ACashController (single user, in Brazilian Portuguese).

Goal: clean, simple, responsive static HTML screens (HTML + plain CSS, no
framework required, but Bootstrap 5 via CDN is acceptable). These will later be
wired to Django templates ({% block %}, {{ variables }}, {% for %}), so keep the
markup semantic and easy to templatize. All visible text in pt-BR.

Design language:
- Modern, light, professional fintech look. Generous whitespace.
- Primary color #1D9E75 (green), accent #2E6FB7 (blue), warning/expense #C25E3A.
- Cards with subtle shadow, rounded corners. Sans-serif (e.g. Poppins via CDN).
- Money in BRL (R$). Entradas in green, Saídas in red.

Produce these 9 screens as separate HTML files, each extending a shared base
layout with a top navbar (Dashboard, Transações, Categorias, Metas, Sair):

1. base.html — navbar + content area + flash message area (placeholders).
2. login.html — login form (usuário, senha) + link para cadastro.
3. cadastro.html — registration form (usuário, e-mail, senha, confirmar senha).
4. dashboard.html — the main screen:
   - 3 summary cards on top: Saldo atual, Total de Entradas, Total de Saídas (mês).
   - a LINE chart placeholder (canvas#chartPatrimonio) "Evolução do Patrimônio".
   - a PIE chart placeholder (canvas#chartCategorias) "Gastos por Categoria".
   - Include Chart.js via CDN and a <script> with SAMPLE data so the charts render
     in the static preview (Django will later replace the data via JSON).
   - buttons: "Exportar CSV" and "Exportar PDF".
5. transacoes.html — table of transactions (data, descrição, categoria, tipo,
   valor) with a "Nova Transação" button; filter by month/year; edit/delete icons.
   NOTE: the "tipo" column is display-only (Entrada/Saída) and is derived from the
   transaction's categoria — color the row/badge green for Entrada, red for Saída.
6. transacao_form.html — form to create/edit a transaction (descrição, valor,
   categoria [select], data). NOTE: there is NO separate Entrada/Saída field — the
   type comes from the chosen categoria. Show an inline error area for "Saldo
   insuficiente".
7. categorias.html — list of categories as a table/cards (nome, tipo [Entrada/Saída
   badge, green/red], a color swatch from `cor`, icon) with a "Nova Categoria" button
   and edit/delete icons.
8. categoria_form.html — form to create/edit a category: nome (text), tipo (select
   Entrada/Saída), cor (color picker / hex input), icone (optional text). This is the
   screen where the Entrada/Saída type is actually defined — transactions inherit it.
9. metas.html — list of saving goals as cards with a progress bar (valor_atual /
   valor_alvo), prazo, and a "Nova Meta" button.

Constraints:
- Keep CSS in a single <style> or one styles.css; avoid heavy JS beyond Chart.js.
- Use placeholder/sample data so every screen looks complete in preview.
- Mark obvious dynamic spots with HTML comments like <!-- {% for t in transacoes %} -->
  so the Django integration is easy.
- Mobile responsive (cards stack, table scrolls horizontally).

Deliver each screen as a complete standalone HTML file.
```

---

### Depois de gerar
1. Baixe os HTML.
2. Coloque o layout em `templates/base.html` e cada tela em `templates/<app>/`.
3. O Claude Code (próximo doc) converte os placeholders em tags Django reais.
