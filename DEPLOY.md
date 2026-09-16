# 🚀 Deploy no Railway — passo a passo

## 1. Criar conta e projeto

1. Acesse [railway.app](https://railway.app) e entre com sua conta GitHub
2. Clique em **New Project**
3. Escolha **Deploy from GitHub repo**
4. Selecione o repositório `antonio-gab/vagabot`
5. Clique em **Deploy Now**

O Railway detecta o `Procfile` e `runtime.txt` automaticamente.

---

## 2. Configurar variáveis de ambiente

No painel do Railway, vá em **Variables** e adicione:

| Variável | Valor | Obrigatório |
|---|---|---|
| `GMAIL_USER` | seu@gmail.com | ✅ |
| `GMAIL_APP_PASSWORD` | senha de app do Google | ✅ |
| `DESTINATARIO` | seu@gmail.com | ✅ |
| `GITHUB_TOKEN` | seu token do GitHub | ✅ (mais vagas) |
| `INTERVALO_HORAS` | `6` | opcional |
| `MATCH_MINIMO` | `60` | opcional |

> **Como gerar a Senha de App do Gmail:**
> 1. Acesse [myaccount.google.com](https://myaccount.google.com)
> 2. Segurança → Verificação em duas etapas (precisa estar ativa)
> 3. Segurança → Senhas de app
> 4. Selecione "Outro" → digite "VagaBot" → Gerar
> 5. Copie a senha de 16 caracteres gerada

---

## 3. Verificar o deploy

Após o deploy, o Railway fornece uma URL pública. Acesse:

- `https://sua-url.railway.app/` → dashboard do VagaBot
- `https://sua-url.railway.app/api/status` → healthcheck (deve retornar `{"status":"ok"}`)

---

## 4. Como funciona em produção

```
Railway (24h/dia)
├── Gunicorn (servidor web)
│   ├── GET  /           → dashboard
│   ├── GET  /api/vagas  → vagas em cache
│   ├── POST /api/buscar → busca manual
│   └── GET  /api/status → healthcheck
└── Thread do scheduler (dentro do mesmo processo)
    └── Busca vagas a cada X horas e envia e-mail
```

O bot busca automaticamente assim que o servidor sobe,
e depois repete a cada `INTERVALO_HORAS` horas.

---

## 5. Rodar localmente

```bash
# Instalar dependências
cd backend
pip install -r requirements.txt

# Criar .env com suas credenciais
cp .env.example .env
# edite o .env com seus dados

# Rodar
python app.py
# Acesse http://localhost:5000
```
