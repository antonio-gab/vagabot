# 🤖 VagaBot

Bot pessoal de monitoramento de vagas de emprego. Ele acessa sites como **Gupy, CIEE, Vagas.com.br, Programathor e LinkedIn RSS**, filtra as vagas com base no seu perfil (skills, área, nível, localização) e envia notificações por **Gmail**.

---

## ✅ Status do projeto

| Componente | Status |
|---|---|
| Dashboard (frontend) | ✅ Pronto — dados mockados |
| Coleta GitHub Issues | ✅ Integrada e validada |
| RSS Gupy, Vagas.com.br e Programathor | ⚠️ Preservados, desativados até URLs válidas |
| Scraping CIEE | 🔲 A fazer |
| Algoritmo de match | ✅ Implementado |
| Notificações Gmail | ✅ Implementadas (requer Senha de app) |
| Deploy Railway/Render | 🔲 A fazer |
| Dashboard conectado ao backend | 🔲 A fazer |

---

## 🗂 Estrutura do projeto

```
vagabot/
├── frontend/
│   ├── dashboard.jsx        # Dashboard React (interface principal)
│   └── index.html           # Entrada HTML para rodar localmente
├── backend/
│   ├── main.py              # Ponto de entrada — agenda as buscas
│   ├── matcher.py           # Calcula score de compatibilidade
│   ├── notifier.py          # Envia e-mail via Gmail SMTP
│   ├── config.py            # Perfil do usuário e configurações
│   ├── vagas_vistas.json    # Controle de vagas já enviadas
│   ├── scrapers/
│   │   ├── gupy.py          # RSS do Gupy
│   │   ├── ciee.py          # Scraping do CIEE
│   │   ├── vagas_com.py     # RSS do Vagas.com.br
│   │   ├── programathor.py  # RSS do Programathor
│   │   └── linkedin_rss.py  # RSS de busca salva do LinkedIn
│   └── requirements.txt
└── README.md
```

---

## 🚀 Como rodar localmente

### Frontend

Abra `frontend/index.html` no navegador — ou cole `dashboard.jsx` em qualquer sandbox React (stackblitz.com, codesandbox.io).

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
python main.py --agora --sem-email  # valida coleta, deduplicação e match sem enviar
python main.py --agora              # envia e-mail para vagas novas
```

---

## ⚙️ Configuração

Crie `.env` em `backend/`:

```env
GMAIL_USER=seu@gmail.com
GMAIL_APP_PASSWORD=sua_senha_de_app
DESTINATARIO=seu@gmail.com
INTERVALO_HORAS=6
MATCH_MINIMO=70

# RSS históricos: deixe false. As URLs atuais não respondem mais como feeds.
ATIVAR_GUPY=false
ATIVAR_VAGAS_COM=false
ATIVAR_PROGRAMATHOR=false
```

> **Senha de app Gmail:** myaccount.google.com → Segurança → Senhas de app

---

## 📋 Fontes monitoradas

| Fonte | Método | Viabilidade |
|---|---|---|
| Gupy | RSS | ✅ Fácil |
| Vagas.com.br | RSS | ✅ Fácil |
| Programathor | RSS | ✅ Fácil |
| CIEE | Scraping | 🟡 Médio |
| LinkedIn | RSS salvo | 🟡 Médio |
| Indeed | Scraping | 🔴 Difícil |
| Glassdoor | — | ⛔ Bloqueado |

---

## 📦 Dependências Python

```
requests==2.31.0
beautifulsoup4==4.12.2
schedule==1.2.1
python-dotenv==1.0.0
```

---

Desenvolvido por [Antonio Gabriel](https://github.com/antonio-gab)

### Testes

```bash
cd backend
python -m unittest discover -s tests -v
```

`--sem-email` não envia nem registra vagas como vistas, por isso é seguro repetir
durante a configuração. Uma vaga só entra em `backend/vagas_vistas.json` após o
Gmail confirmar o envio. O arquivo é ignorado pelo Git, assim como `.env`.

### Limitações atuais das fontes

A coleta padrão usa os repositórios de vagas em GitHub Issues e foi validada com
vagas reais. Na validação de 15/09/2026, os endereços RSS mantidos para Gupy e
Programathor retornaram 404; os de Vagas.com.br retornaram HTML em vez de XML.
Por isso eles estão opt-in, sem impedir o fluxo principal. CIEE ainda é um
esqueleto e LinkedIn exige uma URL RSS pessoal; nenhum dos dois é executado.
