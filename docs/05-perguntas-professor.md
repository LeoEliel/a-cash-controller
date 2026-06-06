# Banco de Perguntas do Professor (20 pts) — com respostas

> Simulem isto antes do dia 11/06. Cada integrante deve saber responder **todas**, não só a sua parte.

---

## Bloco 1 — CBV e arquitetura

**P: Por que vocês usaram Class-Based Views em vez de function views?**
R: CBVs trazem comportamento pronto (ListView, CreateView, etc.), reduzem repetição e permitem reutilizar regras via **mixins**. O enunciado também exige CBV. Ex.: nossa `TransacaoCreateView` herda de `CreateView` e só sobrescrevemos `get_form_kwargs()` e `form_valid()`.

**P: O que é um mixin? Onde vocês usaram?**
R: É uma classe pequena com um comportamento isolado, "misturada" por herança múltipla. Usamos `UsuarioQuerysetMixin` (isola dados por usuário) e `GeraPDFMixin` (gera PDF). Vantagem: o mesmo código serve para várias views (DRY).

**P: Por que vários apps Django?**
R: Separação de responsabilidades (SRP): `usuario` (auth), `financas` (domínio), `dashboard` (relatórios/gráficos), `api` (integração REST). Facilita manutenção e teste.

---

## Bloco 2 — Validação de saldo (provável foco)

**P: Onde e como vocês validam se há saldo suficiente?**
R: No método `clean()` do `TransacaoForm`. O tipo (E/S) **não fica na transação** — é derivado da `categoria` escolhida. Quando `categoria.tipo == 'S'`, comparamos `saldo_usuario(user)` com o valor; se for menor, levantamos `ValidationError("Saldo insuficiente")`. O formulário recebe o `usuario` da view via `get_form_kwargs()`.

**P: Por que validar no Form e não no Model?**
R: A regra depende do **usuário logado**, que é contexto da requisição. O Model não conhece a request; o Form/View conhece. Colocar no Form mantém a regra perto do contexto certo e exibe o erro na tela corretamente.

**P: O saldo fica salvo no banco?**
R: Não. É **derivado**: `soma(Entradas) - soma(Saídas)` do usuário, calculado com `aggregate(Sum('valor'))`. Assim nunca fica inconsistente — a fonte da verdade são as transações.

**P: E se duas saídas forem feitas ao mesmo tempo?**
R: Para o escopo acadêmico, validamos por request. (Se quiser blindar concorrência: usar `select_for_update()` numa transação atômica — bom mencionar como melhoria futura.)

---

## Bloco 3 — Isolamento por usuário

**P: Como garantem que um usuário não vê dados de outro?**
R: Duas camadas: `LoginRequiredMixin` (exige login) e `get_queryset()` filtrando por `request.user` em **todas** as views privadas. Na API, o `get_queryset()` do ViewSet também filtra por `request.user`.

**P: O que acontece se eu trocar o ID na URL para acessar a transação de outro usuário?**
R: Não aparece. Como o `get_queryset()` já filtra por `request.user`, o objeto de outro usuário simplesmente não está no queryset → retorna 404.

**P: Onde definem para onde vai um usuário não logado?**
R: `LOGIN_URL` no settings; o `LoginRequiredMixin` redireciona para lá.

---

## Bloco 4 — Dashboard e gráficos

**P: Como os dados chegam ao Chart.js?**
R: A `DashboardView` calcula as séries no backend (ORM, com `TruncMonth` + `Sum`), passa como JSON ao template (json_script), e o `charts.js` lê esse JSON e desenha. O Django cuida dos **dados**; o Chart.js, da **apresentação**.

**P: Como calculam a evolução mensal do patrimônio?**
R: Agrupamos transações por mês (`TruncMonth`), somamos entradas e saídas de cada mês e **acumulamos** (entradas − saídas) mês a mês → patrimônio acumulado.

**P: E o gráfico de pizza?**
R: `Transacao` do tipo Saída, agrupado por categoria (`values('categoria__nome').annotate(Sum('valor'))`). Cada fatia usa a cor da categoria (`Categoria.cor`).

---

## Bloco 5 — Exportação CSV/PDF

**P: Como geram o CSV?**
R: Módulo `csv` do Python escrevendo num `HttpResponse` com `content_type='text/csv'` e header `Content-Disposition: attachment`. Filtrado por mês/ano e por usuário.

**P: E o PDF?**
R: `GeraPDFMixin` (xhtml2pdf/pisa): renderiza um template HTML (`extrato_pdf.html`) e converte para PDF. Mesmo padrão do repo de referência.

---

## Bloco 6 — API e Token Authentication

**P: Como funciona a autenticação da API?**
R: DRF `TokenAuthentication`. Cada usuário tem um token (tabela `authtoken`). O cliente envia `Authorization: Token <chave>`. Sem token válido → 401. O token é obtido no endpoint `/api/token/` (`obtain_auth_token`) enviando usuário e senha.

**P: Qual a diferença entre Token e Session auth?**
R: Session usa cookie e é pensada para o navegador; Token é stateless, ideal para clientes externos (apps, scripts). Usamos Session no site e Token na API.

**P: A API também isola por usuário?**
R: Sim. O `get_queryset()` do ViewSet filtra por `request.user`, e `perform_create()` seta `usuario=request.user`. Permissão `IsAuthenticated`.

**P: Mostre como pegar um token.**
R:
```bash
curl -X POST http://localhost:8000/api/token/ \
  -d "username=ana&password=senha"
# → {"token":"abc123..."}
curl http://localhost:8000/api/transacoes/ \
  -H "Authorization: Token abc123..."
```

---

## Bloco 7 — Banco, models e ORM

**P: Por que `DecimalField` para valor e não Float?**
R: Dinheiro exige precisão exata; Float tem erro de ponto flutuante. `DecimalField` evita isso.

**P: Para que serve o `related_name`?**
R: Permite acessar o lado inverso da relação: `user.transacoes.all()`, `user.metas.all()`.

**P: O que é uma migração?**
R: Arquivo que descreve mudanças no schema do banco. `makemigrations` gera; `migrate` aplica.

**P: Por que `on_delete=PROTECT` na categoria da transação?**
R: Impede apagar uma categoria que ainda tem transações, evitando perda de histórico.

---

## Bloco 8 — Pegadinhas comuns

- **"Quem escreveu essa parte?"** → todos sabem explicar tudo (combinar antes quem fala o quê, mas qualquer um responde).
- **"Mostra rodando."** → tenham o servidor pronto, um usuário com dados de exemplo e os gráficos populados.
- **"E se eu logar com outro usuário?"** → demonstrar que os dados mudam (isolamento).
- **"Cadê o commit dessa feature?"** → histórico do Git limpo, um commit por milestone.

---

## Checklist final antes da apresentação

- [ ] Servidor roda sem erro (`manage.py runserver`).
- [ ] 2 usuários com dados → provar isolamento ao vivo.
- [ ] Dashboard com os 2 gráficos populados.
- [ ] Exportar CSV e PDF funcionando.
- [ ] API: obter token + listar transações no Postman/curl.
- [ ] Tentar lançar Saída sem saldo → erro aparece.
- [ ] Cada integrante respondeu o banco de perguntas em simulação.
- [ ] README com passos de instalação.
