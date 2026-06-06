# Deploy e Variáveis de Ambiente — ACashController

> Hospedagem escolhida: **PythonAnywhere** (free tier), mantendo **SQLite**.
> Grátis, disco persistente (dados não somem), feito pra Django acadêmico.
> URL pública é desejável mas **não obrigatória** — serve só pra mostrar.

---

## Parte 1 — Variáveis de ambiente (`django-environ`)

Mesmo padrão do repo de referência (`ecommerce2026` usa `.env` + `.env_vazio`).
Objetivo: **nada de segredo no código nem no GitHub**.

### 1.1 Instalar
```
pip install django-environ
```
Adicionar ao `requirements.txt`:
```
django-environ==0.11.2
```

### 1.2 `.gitignore` (na raiz)
```
.env
db.sqlite3
__pycache__/
*.pyc
/staticfiles/
```
> **Nunca** commitar `.env` nem `db.sqlite3`.

### 1.3 `.env.example` (ESTE sim vai pro Git — é só o modelo, sem valores reais)
```
SECRET_KEY=troque-por-uma-chave-secreta
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
```

### 1.4 `.env` (cada integrante cria o seu localmente, copiando do .example)
```
SECRET_KEY=django-insecure-COLOQUE-ALGO-LONGO-E-ALEATORIO
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,.app.github.dev
DATABASE_URL=sqlite:///db.sqlite3
```
> Gerar uma SECRET_KEY:
> ```
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 1.5 `core/settings.py`
```python
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}

# Arquivos estáticos (necessário pro deploy)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'      # destino do collectstatic
STATICFILES_DIRS = [BASE_DIR / 'static']    # seus css/js de dev
```

> **Ponto de arguição:** "Por que `.env`?" → para não versionar segredos (SECRET_KEY),
> permitir config diferente por ambiente (dev vs prod) sem mudar código, e seguir
> o padrão 12-factor.

---

## Parte 2 — Deploy no PythonAnywhere (passo a passo)

> Plano **Beginner é grátis**. Roda Django + SQLite com disco persistente.
> Dá uma URL tipo `https://SEUUSUARIO.pythonanywhere.com`.

### 2.1 Pré-requisitos
- Projeto já no GitHub (repo do grupo).
- Conta grátis em https://www.pythonanywhere.com (Beginner).

### 2.2 Subir o código (console Bash do PythonAnywhere)
No dashboard → **Consoles → Bash**:
```bash
git clone https://github.com/SEU-USUARIO/SEU-REPO.git
cd SEU-REPO

# ambiente virtual
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2.3 Criar o `.env` no servidor
O `.env` não veio do Git (está no .gitignore), então criar lá:
```bash
nano .env
```
Conteúdo (ATENÇÃO: DEBUG=False e o host do PythonAnywhere):
```
SECRET_KEY=uma-chave-secreta-bem-longa-de-producao
DEBUG=False
ALLOWED_HOSTS=SEUUSUARIO.pythonanywhere.com
DATABASE_URL=sqlite:///db.sqlite3
```

### 2.4 Migrações, superuser e estáticos
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
# (opcional) rodar o seed de categorias:
python manage.py seed_categorias
```

### 2.5 Criar a Web App
No dashboard → aba **Web** → **Add a new web app**:
1. Escolher **Manual configuration** (não o "Django" automático) → Python 3.10.
2. Na seção **Virtualenv**, apontar para:
   `/home/SEUUSUARIO/SEU-REPO/venv`
3. Editar o **WSGI configuration file** (link na aba Web) e deixar assim:
```python
import os, sys

path = '/home/SEUUSUARIO/SEU-REPO'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
4. Na seção **Static files** da aba Web, mapear:
   | URL | Directory |
   |---|---|
   | `/static/` | `/home/SEUUSUARIO/SEU-REPO/staticfiles` |

5. Clicar em **Reload** (botão verde no topo da aba Web).

Pronto → `https://SEUUSUARIO.pythonanywhere.com`

### 2.6 Atualizar depois de mudanças (workflow de re-deploy)
Toda vez que vocês fizerem push no GitHub:
```bash
# no console Bash do PythonAnywhere
cd ~/SEU-REPO
source venv/bin/activate
git pull
pip install -r requirements.txt        # só se mudou dependência
python manage.py migrate               # só se mudou model
python manage.py collectstatic --noinput
```
Depois → aba **Web** → botão **Reload**.

> É "manual", mas são 4 comandos + 1 clique. Os **dados no SQLite persistem**
> entre deploys (diferente do Render).

---

## Parte 3 — Checklist de segurança pra produção

- [ ] `DEBUG=False` no `.env` do servidor.
- [ ] `ALLOWED_HOSTS` com o domínio do PythonAnywhere.
- [ ] `SECRET_KEY` de produção diferente da de dev.
- [ ] `.env` e `db.sqlite3` no `.gitignore` (confirmar que NÃO foram commitados).
- [ ] `collectstatic` rodado (senão o CSS/JS não carrega com DEBUG=False).
- [ ] (Opcional) `CSRF_TRUSTED_ORIGINS = ['https://SEUUSUARIO.pythonanywhere.com']` no settings.

---

## Parte 4 — Resumo dev vs prod

| | Desenvolvimento (Codespace/local) | Produção (PythonAnywhere) |
|---|---|---|
| `DEBUG` | `True` | `False` |
| `ALLOWED_HOSTS` | localhost, `.app.github.dev` | `SEUUSUARIO.pythonanywhere.com` |
| Banco | SQLite (`db.sqlite3`) | SQLite (`db.sqlite3`) — persistente |
| Estáticos | servidos pelo runserver | `collectstatic` + mapeamento na aba Web |
| Servidor | `manage.py runserver` | WSGI do PythonAnywhere |

> O código é o **mesmo**; só o `.env` muda entre ambientes. Esse é o ponto-chave.
