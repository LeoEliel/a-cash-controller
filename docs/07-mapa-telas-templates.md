# Mapa: Telas (Claude Design) → Templates Django + URLs

> **Decisão do grupo:** os docs mandam na convenção de nomes (Django). As telas geradas pelo Claude Design serão **renomeadas/adaptadas** para bater com esta tabela — NÃO o contrário.
> Cada arquivo HTML entregue já traz comentários `<!-- Django: ... -->` com os `{% url %}`, `{% block %}` e variáveis de contexto. Use-os como guia ao integrar.

---

## 1. Renomeação dos arquivos HTML → templates

| Arquivo entregue (Claude Design) | Template Django (destino) | App / pasta |
|---|---|---|
| `base.html` | `templates/base.html` | projeto (central) |
| `login.html` | `usuario/templates/registration/login.html` | usuario |
| `cadastro.html` | `usuario/templates/usuario/cadusuario.html` | usuario |
| `dashboard.html` | `dashboard/templates/dashboard/dashboard.html` | dashboard |
| `transacoes.html` | `financas/templates/financas/transacao_list.html` | financas |
| `transacao_form.html` | `financas/templates/financas/transacao_form.html` | financas |
| `categorias.html` | `financas/templates/financas/categoria_list.html` | financas |
| `categoria_form.html` | `financas/templates/financas/categoria_form.html` | financas |
| `metas.html` | `financas/templates/financas/meta_list.html` | financas |
| `transacao_confirm_delete.html` | `financas/templates/financas/transacao_confirm_delete.html` | financas |
| `meta_form.html` | `financas/templates/financas/meta_form.html` | financas |
| `extrato_pdf.html` | `dashboard/templates/dashboard/extrato_pdf.html` | dashboard |
| `styles.css` | `static/css/styles.css` | projeto |

> **12 telas geradas (completas).** As 3 últimas (`transacao_confirm_delete`, `meta_form`, `extrato_pdf`) já vieram consistentes com o design system. Originais ficam em `telas/` no repo.

> O CSS já tem classes para tudo: `.filter-bar`, `.pagination`, `.page-btn`, `.goals-grid`, `.goal-card`, `.dashboard-split`, `.chart-card`, `.charts-bottom`, `.cat-row/.progress-fill`, `.color-swatch`, `.badge-entrada/-saida`, `.stat-card.green/.blue/.red`. Não inventar classes novas.

---

## 2. URLs esperadas pelas telas (já nos comentários `Django:`)

Crie estes `name=` nos `urls.py`. A navbar (`base.html`) e os botões dependem deles.

### usuario
| name | view | nota |
|---|---|---|
| `login` | LoginView | `registration/login.html` |
| `logout` | LogoutView | link "Sair" na navbar |
| `cadastro` | CreateView (UserCreationForm) | template `cadusuario.html` |

### financas — Transação
| name | view | usado em |
|---|---|---|
| `transacoes` | TransacaoListView | navbar, filtro `<form action>` |
| `transacao_nova` | TransacaoCreateView | botão "+ Nova Transação" |
| `transacao_editar <pk>` | TransacaoUpdateView | ícone ✎ na linha |
| `transacao_excluir <pk>` | TransacaoDeleteView (POST) | ícone ✕ na linha |

> `transacao_form.html` usa `<form method="post">` único pra criar e editar (`{% if form.instance.pk %}`). Os docs antigos citavam `transacao_salvar` — **substituído** por `transacao_nova` + `transacao_editar`.

### financas — Categoria
| name | view | usado em |
|---|---|---|
| `categoria_list` | CategoriaListView | navbar (hoje está `href="#"` → trocar) |
| `categoria_nova` | CategoriaCreateView | botão "+ Nova Categoria" |
| `categoria_editar <pk>` | CategoriaUpdateView | ícone ✎ |
| `categoria_excluir <pk>` | CategoriaDeleteView (POST) | ícone ✕ |
| `categoria_salvar` | (action do form) | a tela usa `action="{% url 'categoria_salvar' %}"` — pode apontar pro mesmo create/update ou trocar o action por `transacao_form`-style. **Recomendado:** trocar o `action` da tela para `categoria_nova`/`categoria_editar` e dispensar `categoria_salvar`. |

### financas — Meta
| name | view | usado em |
|---|---|---|
| `meta_nova` | MetaCreateView | botão "+ Nova Meta" (dashboard + metas) |
| `meta_editar <pk>` | MetaUpdateView | botão "Editar" no card |
| `meta_excluir <pk>` | MetaDeleteView (POST) | botão "Excluir" no card |

> `meta_list.html` (metas.html) não tem botão de listagem na navbar com url própria além de `metas` — adicionar `name='metas'` na ListView se quiser link direto; a navbar aponta pra `metas.html`.

### dashboard
| name | view | usado em |
|---|---|---|
| `dashboard` | DashboardView (TemplateView) | navbar brand + link |
| `exportar_csv` | ExportarCSVView | botão "↓ Exportar CSV" (sidebar) |
| `exportar_pdf` | ExportarPDFView (GeraPDFMixin) | botão "↓ Exportar PDF" (sidebar) |

---

## 3. Campos de formulário (ids = `id_<campo>`) por tela

> Django gera `id_<nome_do_campo>` automaticamente. As telas já usam esses ids — manter os mesmos `name=` no Form garante o casamento.

**login.html** → `id_username`, `id_password`
**cadusuario.html** (cadastro) → `id_username`, `id_email`, `id_password1`, `id_password2` (UserCreationForm)
**transacao_form.html** → `id_descricao`, `id_valor`, `id_data`, `id_categoria`
  - `id_categoria` é um `<select>` com `<optgroup label="Saídas">` / `<optgroup label="Entradas">`.
  - **NÃO há campo `tipo`** — hint na tela: "o tipo é definido pela categoria". Consistente com o model.
**categoria_form.html** → `id_nome`, `id_tipo` (select E/S), `id_cor` (`<input type="color">`), `id_icone` (opcional)
  - JS da tela só faz preview do swatch e do badge — a validação real é no `form.clean()`.
**meta_form.html** → `id_nome`, `id_valor_alvo` (number step 0.01), `id_valor_atual` (number, default 0), `id_prazo` (date, opcional)
  - `valor_alvo`+`valor_atual` ficam num `.form-row` (2 colunas). Campo é **`nome`** (não titulo).
  - JS opcional faz preview do progresso reusando `.goal-track`/`.goal-fill`. `action` condicional `meta_nova`/`meta_editar`.

**transacao_confirm_delete.html** → sem form fields; usa `object.*` (padrão `DeleteView`): `{{ object.descricao }}`, `{{ object.categoria.nome }}`, `{{ object.data|date:"d/m/Y" }}`, `{{ object.valor|floatformat:2 }}`, tipo via `{% if object.categoria.tipo == 'E' %}` (lembrando: `tipo` é `@property`). POST form → `{% url 'transacao_excluir' object.pk %}` + `{% csrf_token %}`, botões `.btn-danger` (Excluir) + `.btn-outline` (Cancelar). Reusar este mesmo padrão para `categoria_confirm_delete` e `meta_confirm_delete` se preferir confirmação dedicada (as telas de categoria/meta usam botão ✕/Excluir direto — pode ser POST inline OU redirecionar pra esta tela de confirmação).

**extrato_pdf.html** (renderizado por xhtml2pdf/pisa — NÃO é tela de browser) → standalone, **sem** base.html/navbar/JS/CDN, layout 100% em `<table>` com unidades `pt`. Context vars: `mes_nome`, `ano`, `saldo`, `total_entradas`, `total_saidas`, `transacoes` (loop com `{% empty %}`), `gerado_em` (`{{ gerado_em|date:"d/m/Y H:i" }}`), `user`. Classes próprias do PDF (`.badge-pdf`, `.val-saida-pdf` etc.) — NÃO dependem do styles.css. Render: `pisa.CreatePDF(render_to_string('dashboard/extrato_pdf.html', ctx), dest=response)`.

---

## 4. Erros de validação

As telas mostram erro via `.alert-inline` (`#erroValidacao`) e `.form-hint` em vermelho por campo:
```django
{% if form.errors %}
  <div class="alert-inline"><span>⚠</span><span>Corrija os erros abaixo antes de salvar.</span></div>
{% endif %}
...
{% if form.valor.errors %}<span class="form-hint" style="color:var(--red);">{{ form.valor.errors|join:", " }}</span>{% endif %}
```
A mensagem de **"Saldo insuficiente"** (regra de negócio) cai aqui como erro de form (`non_field_errors` ou erro no campo `valor`).

---

## 5. Flash messages (toda tela)

`base.html` já tem o bloco. As classes batem com `messages`:
```django
{% if messages %}{% for m in messages %}
  <div class="alert-container"><div class="alert alert-{{ m.tags }}">{{ m }}</div></div>
{% endfor %}{% endif %}
```
`m.tags` → `success` / `error` / `info` (classes `.alert-success/.alert-error/.alert-info` existem no CSS).
