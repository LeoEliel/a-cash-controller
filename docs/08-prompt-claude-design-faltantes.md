# Prompt — Claude Design (3 telas faltantes)

> Cole no Claude Design, **no mesmo projeto** onde já foram geradas as 9 telas + `styles.css`.
> Objetivo: gerar APENAS os 3 templates que faltam, 100% consistentes com o que já existe.

---

```
You already generated the ACashController screens (base.html, login, cadastro,
dashboard, transacoes, transacao_form, categorias, categoria_form, metas) and a
shared styles.css. Now generate the 3 MISSING screens. Be STRICTLY CONSISTENT with
everything already created — same design system, same markup patterns, same CSS
classes, same Django comment style. DO NOT invent new CSS classes or restyle
anything; reuse the existing styles.css.

CONSISTENCY RULES (must follow exactly — these match the existing screens):
- Reuse styles.css as-is. Allowed classes only: .navbar/.navbar-brand/.logo-mark/
  .navbar-nav (a.active)/.navbar-end/.avatar/.navbar-username/.navbar-sair,
  .page/.page-header/.page-title, .card, .form-group/.form-label/.form-control
  (.is-invalid)/.form-hint/.form-row, .alert-inline, .form-actions,
  .btn/.btn-primary/.btn-secondary/.btn-outline/.btn-danger/.btn-inline/.btn-sm,
  .badge/.badge-entrada/.badge-saida, .table-container/.table-scroll, .td-muted.
- Design system: green #1D9E75 (primary), blue #2E6FB7 (accent), red/expense
  #C25E3A, font Poppins, CSS vars (--green/--blue/--red/--text/--text-muted/--border/
  --radius/--surface). Use var(--red) for destructive accents.
- Every screen (except the PDF one) extends base.html and includes the SAME navbar
  block + flash messages block as the other screens, with the correct nav item set
  to class="active". Keep the dual markup style: static preview HTML PLUS
  "<!-- Django: ... -->" comments showing the real template tags ({% extends %},
  {% block title %}, {% block content %}, {% csrf_token %}, {% url %}, {{ ... }}).
- pt-BR for all user-facing text.

SCREEN 1 — transacao_confirm_delete.html (DeleteView confirmation)
- Extends base.html, title "Excluir Transação — ACashController", nav "Transações"
  active.
- Centered narrow .card (max-width ~480px) inside .page, with a .page-header
  ("Excluir Transação" + a "← Voltar" .btn .btn-outline .btn-sm pointing to
  transacoes).
- Show the transaction being deleted using the SAME visual language as
  transacoes.html rows: descrição (bold), categoria (.td-muted), a .badge
  (badge-entrada/badge-saida) for tipo, the date (.td-muted), and the value using
  .td-val-saida / .td-val-entrada. Use static example data + Django comments
  ({{ object.descricao }}, {{ object.categoria.nome }}, {{ object.data|date:"d/m/Y" }},
  {{ object.valor|floatformat:2 }}, {{ object.tipo_display }} — remember tipo is a
  @property read from the category, there is NO tipo field).
- A confirmation question: "Tem certeza que deseja excluir esta transação? Esta
  ação não pode ser desfeita."
- A POST form: <!-- Django: <form method="post" action="{% url 'transacao_excluir'
  object.pk %}">{% csrf_token %} --> with .form-actions containing a
  .btn.btn-danger "Excluir" (submit) and a .btn.btn-outline "Cancelar" linking to
  transacoes. Static preview action="#".

SCREEN 2 — meta_form.html (create/edit a savings goal)
- Extends base.html, title "{% if form.instance.pk %}Editar{% else %}Nova{% endif %}
  Meta — ACashController", nav "Metas" active.
- Same layout pattern as categoria_form.html: a max-width ~520px wrapper, a
  .page-header (dynamic title + "← Voltar" .btn-outline .btn-sm to metas) and a
  .card holding the form.
- Include the validation error block exactly like categoria_form.html:
  <!-- Django: {% if form.errors %} --> .alert-inline with ⚠ ... <!-- {% endif %} -->
- Form fields matching the MetaEconomia model (field names → ids generated as
  id_<name>):
    * Nome (required) — id_nome, name="nome", maxlength="120", placeholder
      "Ex.: Fundo de Emergência, Viagem...". This is the model field `nome`
      (NOT titulo).
    * Valor Alvo (required) — id_valor_alvo, name="valor_alvo", type="number"
      step="0.01" min="0", placeholder "20000.00". Prefix hint "R$".
    * Valor Atual — id_valor_atual, name="valor_atual", type="number" step="0.01"
      min="0", default value 0, hint "Quanto você já juntou".
    * Prazo (opcional) — id_prazo, name="prazo", type="date".
  Use the .form-row (two-column) grid for Valor Alvo + Valor Atual, like the
  reference layout, collapsing on mobile (already handled by CSS).
- Per-field error hints in red exactly like categoria_form.html
  ({% if form.<campo>.errors %}<span class="form-hint" style="color:var(--red);">
  {{ form.<campo>.errors|join:", " }}</span>{% endif %}).
- .form-actions: .btn.btn-primary submit ("{% if form.instance.pk %}Salvar
  Alterações{% else %}Salvar Meta{% endif %}") + .btn.btn-outline "Cancelar" to
  metas. Static action="#"; Django comment shows the form posts to
  {% url 'meta_nova' %} / {% url 'meta_editar' meta.pk %} as appropriate.
- Optional: a tiny live progress preview (valor_atual / valor_alvo %) reusing the
  .goal-track/.goal-fill classes from metas.html, with minimal inline JS — same
  style as the color/badge preview JS in categoria_form.html (self-invoking
  function in {% block extra_js %}). Keep it optional and unobtrusive.

SCREEN 3 — extrato_pdf.html (monthly statement, rendered by xhtml2pdf/pisa — NOT a
browser screen)
- This is for server-side PDF generation with xhtml2pdf (pisa), so it must be a
  STANDALONE html (does NOT extend base.html, no navbar, no external CDN, no JS).
- IMPORTANT xhtml2pdf constraints: use simple inline CSS or a small <style> block
  with only well-supported properties (no flexbox/grid; use tables for layout, fixed
  widths, basic borders/padding/background-color, font-family). Keep it print-clean.
- Header: ACashController title + "AC" logo mark (simple colored box/table cell,
  green #1D9E75), the report title "Extrato Mensal", and the period
  ({{ mes_nome }} {{ ano }}) and the user ({{ usuario }} / {{ user.username }}).
- A summary table (Saldo, Total de Entradas, Total de Saídas) using the brand colors
  for the values (green entradas, red #C25E3A saídas, blue #2E6FB7 saldo).
- The main transactions table: columns Data | Descrição | Categoria | Tipo | Valor.
  Use a Django loop comment <!-- Django: {% for t in transacoes %} --> with one
  static example row per type. Entrada values in green with "+", Saída in red with
  "−". Right-align the value column. Add an {% empty %} comment row for "Nenhuma
  transação no período.".
- A footer line with generation date ({{ gerado_em|date:"d/m/Y H:i" }}) and a small
  "Gerado por ACashController" note.
- Use pt-BR currency formatting hints (R$, floatformat:2) in the Django comments.

OUTPUT: deliver the 3 HTML files named exactly transacao_confirm_delete.html,
meta_form.html, extrato_pdf.html. Keep them self-explanatory with the Django
comments so they can be dropped into the Django templates folders later.
```
