"""
Envia e-mail com as novas vagas encontradas via Gmail SMTP.

Pré-requisito: crie uma Senha de App no Google:
myaccount.google.com → Segurança → Senhas de app
"""

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import GMAIL_USER, GMAIL_APP_PASSWORD, DESTINATARIO


def _vaga_para_html(vaga: dict) -> str:
    skills_ok = ", ".join(vaga.get("skills_match", [])) or "—"
    skills_falta = ", ".join(vaga.get("skills_faltando", [])) or "—"
    return f"""
    <div style="border:1px solid #e5e7eb;border-radius:10px;padding:18px;margin-bottom:16px;font-family:sans-serif">
      <div style="font-size:16px;font-weight:600;color:#111827">{vaga['titulo']}</div>
      <div style="font-size:14px;color:#2563EB;margin:4px 0">{vaga.get('empresa','')}</div>
      <div style="font-size:13px;color:#6b7280;margin-bottom:10px">
        {vaga.get('fonte','')} · {vaga.get('local','')}
      </div>
      <div style="display:inline-block;background:#d1fae5;color:#065f46;
                  font-weight:700;padding:4px 12px;border-radius:20px;font-size:13px;margin-bottom:10px">
        {vaga['match']}% compatível
      </div>
      <div style="font-size:12px;color:#374151">✅ Skills que você tem: <b>{skills_ok}</b></div>
      <div style="font-size:12px;color:#374151;margin-bottom:10px">📚 Para estudar: <b>{skills_falta}</b></div>
      <a href="{vaga.get('url','#')}"
         style="background:#2563EB;color:white;padding:8px 16px;border-radius:6px;
                text-decoration:none;font-size:13px;font-weight:500">
        Ver vaga
      </a>
    </div>
    """


def enviar_email(vagas: list[dict]) -> None:
    if not vagas:
        print("[Notifier] Nenhuma vaga nova para enviar.")
        return

    corpo_vagas = "".join([_vaga_para_html(v) for v in vagas])
    html = f"""
    <html><body style="font-family:sans-serif;max-width:600px;margin:auto;padding:20px">
      <h1 style="font-size:22px;color:#111827">🤖 VagaBot — {len(vagas)} vaga(s) nova(s)</h1>
      <p style="color:#6b7280">Vagas encontradas que combinam com seu perfil:</p>
      {corpo_vagas}
      <p style="font-size:12px;color:#9ca3af;margin-top:24px">VagaBot · github.com/antonio-gab/vagabot</p>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🤖 VagaBot — {len(vagas)} nova(s) vaga(s) para você"
    msg["From"] = GMAIL_USER
    msg["To"] = DESTINATARIO
    msg.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, DESTINATARIO, msg.as_string())
        print(f"[Notifier] E-mail enviado com {len(vagas)} vaga(s).")
    except Exception as e:
        print(f"[Notifier] Erro ao enviar e-mail: {e}")
