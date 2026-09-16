"""
Envia e-mail HTML com as novas vagas encontradas via Gmail SMTP.

Pré-requisito: crie uma Senha de App no Google:
  myaccount.google.com → Segurança → Senhas de app
"""

import smtplib
import ssl
from html import escape
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

from config import GMAIL_USER, GMAIL_APP_PASSWORD, DESTINATARIO


# ── Templates HTML ────────────────────────────────────────────────────────────

def _badge_match(score: int) -> str:
    if score >= 85:
        cor_bg, cor_txt = "#d1fae5", "#065f46"
    elif score >= 70:
        cor_bg, cor_txt = "#fef3c7", "#92400e"
    else:
        cor_bg, cor_txt = "#f3f4f6", "#374151"
    return (
        f'<span style="background:{cor_bg};color:{cor_txt};'
        f'font-weight:700;padding:3px 10px;border-radius:12px;font-size:13px">'
        f'{score}% compatível</span>'
    )


def _card_vaga(vaga: dict) -> str:
    skills_ok    = ", ".join(vaga.get("skills_match", [])) or "—"
    skills_falta = ", ".join(vaga.get("skills_faltando", [])) or "—"
    labels       = vaga.get("labels", [])
    labels_html  = " ".join(
        f'<span style="background:#e0e7ff;color:#3730a3;'
        f'font-size:11px;padding:2px 7px;border-radius:10px">{escape(str(l))}</span>'
        for l in labels[:5]
    )
    return f"""
<div style="border:1px solid #e5e7eb;border-radius:10px;padding:20px;
            margin-bottom:14px;background:#ffffff">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;
              margin-bottom:8px">
    <div>
      <div style="font-size:16px;font-weight:600;color:#111827;margin-bottom:3px">
        {escape(str(vaga.get('titulo','')))}
      </div>
      <div style="font-size:13px;color:#2563eb;margin-bottom:6px">
        {escape(str(vaga.get('empresa','') or vaga.get('fonte','')))}
      </div>
      <div style="font-size:12px;color:#6b7280">
        📍 {escape(str(vaga.get('local','Não informado')))} &nbsp;·&nbsp;
        🏷 {escape(str(vaga.get('fonte','')))} &nbsp;·&nbsp;
        📅 {escape(str(vaga.get('data',''))[:10])}
      </div>
    </div>
    <div style="flex-shrink:0;margin-left:12px">{_badge_match(vaga.get('match',0))}</div>
  </div>

  <div style="margin:10px 0;line-height:1.6">{labels_html}</div>

  <div style="font-size:12px;color:#374151;margin-bottom:4px">
    ✅ <b>Skills que você já tem:</b> {skills_ok}
  </div>
  <div style="font-size:12px;color:#374151;margin-bottom:14px">
    📚 <b>Para aprender:</b> {skills_falta}
  </div>

  <a href="{escape(str(vaga.get('url','#')), quote=True)}"
     style="display:inline-block;background:#2563eb;color:#ffffff;
            padding:9px 18px;border-radius:7px;text-decoration:none;
            font-size:13px;font-weight:500">
    Ver vaga →
  </a>
</div>
"""


def _montar_html(vagas: list[dict]) -> str:
    hoje = datetime.now().strftime("%d/%m/%Y")
    cards = "".join(_card_vaga(v) for v in vagas)
    return f"""
<html>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
             background:#f9fafb;margin:0;padding:0">
  <div style="max-width:620px;margin:32px auto;padding:0 16px">

    <!-- Cabeçalho -->
    <div style="background:#1e3a5f;border-radius:12px 12px 0 0;
                padding:24px 28px;text-align:center">
      <div style="font-size:28px;font-weight:700;color:#ffffff;letter-spacing:-0.5px">
        🤖 VagaBot
      </div>
      <div style="color:#93c5fd;font-size:14px;margin-top:4px">
        {len(vagas)} nova(s) vaga(s) encontrada(s) — {hoje}
      </div>
    </div>

    <!-- Corpo -->
    <div style="background:#f3f4f6;padding:20px 24px">
      <p style="color:#374151;font-size:14px;margin-bottom:16px">
        Olá! O bot encontrou vagas que combinam com o seu perfil.
        As skills <b>em verde</b> você já tem — as <b>para aprender</b>
        são uma dica do que estudar.
      </p>
      {cards}
    </div>

    <!-- Rodapé -->
    <div style="background:#e5e7eb;border-radius:0 0 12px 12px;
                padding:14px 24px;text-align:center">
      <div style="font-size:12px;color:#9ca3af">
        VagaBot · github.com/antonio-gab/vagabot
        &nbsp;·&nbsp; Para parar os avisos, desligue o bot no dashboard.
      </div>
    </div>

  </div>
</body>
</html>
"""


# ── Envio ─────────────────────────────────────────────────────────────────────

def enviar_email(vagas: list[dict]) -> bool:
    """
    Envia e-mail com as vagas encontradas.
    Retorna True se enviou com sucesso.
    """
    if not vagas:
        print("[Notifier] Nenhuma vaga para enviar.")
        return False

    if not all((GMAIL_USER, GMAIL_APP_PASSWORD, DESTINATARIO)):
        print("[Notifier] Configure GMAIL_USER, GMAIL_APP_PASSWORD e DESTINATARIO no .env — e-mail não enviado.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🤖 VagaBot — {len(vagas)} nova(s) vaga(s) para você"
    msg["From"]    = GMAIL_USER
    msg["To"]      = DESTINATARIO
    msg.attach(MIMEText(_montar_html(vagas), "html", "utf-8"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, DESTINATARIO, msg.as_string())
        print(f"[Notifier] ✓ E-mail enviado para {DESTINATARIO} com {len(vagas)} vaga(s).")
        return True
    except smtplib.SMTPAuthenticationError:
        print("[Notifier] ✗ Erro de autenticação — verifique GMAIL_USER e GMAIL_APP_PASSWORD no .env")
    except Exception as e:
        print(f"[Notifier] ✗ Erro ao enviar: {e}")
    return False
