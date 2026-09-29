import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr, parseaddr
from config import Config


def _send(to_email, to_name, subject, html_body, reply_to=None):
    """Envoie un email HTML via SMTP."""
    if not Config.SMTP_USER or not Config.SMTP_PASSWORD:
        print("[SMTP] Identifiants manquants.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject

    from_name, from_email = parseaddr(Config.MAIL_FROM)
    msg["From"] = formataddr((from_name or "Portfolio", from_email))

    if reply_to:
        msg["Reply-To"] = reply_to

    msg["To"] = formataddr((to_name, to_email))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"[SMTP] Erreur envoi : {e}")
        return False


def send_reply_email(to_email, to_name, original_subject, original_message, reply_text):
    """Envoie une réponse HTML élégante au visiteur."""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ margin:0; padding:0; background:#0a0a0f; font-family:'Inter',Arial,sans-serif; }}
        .wrapper {{ max-width:600px; margin:0 auto; padding:40px 20px; }}
        .card {{ background:#131320; border:1px solid rgba(255,255,255,0.06); border-radius:16px; overflow:hidden; }}
        .header {{ background:linear-gradient(135deg,#6366f1,#8b5cf6); padding:32px; text-align:center; }}
        .header h1 {{ color:#fff; margin:0; font-size:22px; font-weight:700; }}
        .body {{ padding:32px; color:#e5e7eb; line-height:1.6; font-size:15px; }}
        .body p {{ margin:0 0 16px; }}
        .reply-box {{ background:#1a1a2e; border-left:3px solid #6366f1; padding:20px; border-radius:8px; margin:24px 0; white-space:pre-wrap; }}
        .quote {{ background:#0f0f1a; border-radius:8px; padding:16px; margin-top:24px; color:#9ca3af; font-size:13px; }}
        .footer {{ text-align:center; padding:24px; color:#6b7280; font-size:12px; }}
      </style>
    </head>
    <body>
      <div class="wrapper">
        <div class="card">
          <div class="header">
            <h1>Reponse a votre message</h1>
          </div>
          <div class="body">
            <p>Bonjour <strong>{to_name}</strong>,</p>
            <p>Merci pour votre message. Voici ma reponse :</p>
            <div class="reply-box">{reply_text}</div>
            <div class="quote">
              <strong>Votre message initial :</strong><br>
              {original_message}
            </div>
            <p style="margin-top:24px;">N'hesitez pas a me repondre directement a cet email.</p>
            <p style="color:#9ca3af; font-size:13px; margin-top:32px;">
              Cordialement,<br>
              <strong style="color:#e5e7eb;">Josue Adagbe</strong>
            </p>
          </div>
          <div class="footer">
            Cet email a ete envoye depuis le portfolio de Josue Adagbe
          </div>
        </div>
      </div>
    </body>
    </html>
    """

    subject = f"Re: {original_subject}" if original_subject else "Reponse a votre message"

    return _send(
        to_email=to_email,
        to_name=to_name,
        subject=subject,
        html_body=html,
        reply_to=Config.ADMIN_NOTIFY_EMAIL,
    )


def send_admin_notification(name, email, subject, message):
    """Notifie l'admin qu'un nouveau message est arrive."""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ margin:0; padding:0; background:#0a0a0f; font-family:'Inter',Arial,sans-serif; }}
        .wrapper {{ max-width:600px; margin:0 auto; padding:40px 20px; }}
        .card {{ background:#131320; border:1px solid rgba(255,255,255,0.06); border-radius:16px; overflow:hidden; }}
        .header {{ background:linear-gradient(135deg,#6366f1,#8b5cf6); padding:24px; text-align:center; }}
        .header h1 {{ color:#fff; margin:0; font-size:18px; }}
        .body {{ padding:28px; color:#e5e7eb; font-size:15px; line-height:1.6; }}
        .field {{ margin-bottom:14px; }}
        .label {{ color:#9ca3af; font-size:12px; text-transform:uppercase; letter-spacing:0.5px; }}
        .value {{ color:#e5e7eb; font-size:15px; margin-top:2px; }}
        .message-box {{ background:#1a1a2e; border-left:3px solid #6366f1; padding:16px; border-radius:8px; margin:20px 0; white-space:pre-wrap; }}
        .btn {{ display:inline-block; padding:12px 24px; background:linear-gradient(135deg,#6366f1,#8b5cf6); color:#fff !important; text-decoration:none; border-radius:999px; font-weight:600; }}
      </style>
    </head>
    <body>
      <div class="wrapper">
        <div class="card">
          <div class="header">
            <h1>Nouveau message recu</h1>
          </div>
          <div class="body">
            <div class="field">
              <div class="label">De</div>
              <div class="value">{name} &lt;{email}&gt;</div>
            </div>
            <div class="field">
              <div class="label">Sujet</div>
              <div class="value">{subject or 'Sans sujet'}</div>
            </div>
            <div class="label">Message</div>
            <div class="message-box">{message}</div>
            <div style="text-align:center; margin-top:24px;">
              <a href="{Config.SITE_URL}/admin/messages" class="btn">Voir dans le panel admin</a>
            </div>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

    return _send(
        to_email=Config.ADMIN_NOTIFY_EMAIL,
        to_name="Josue Adagbe",
        subject=f"Nouveau message: {subject or name}",
        html_body=html,
        reply_to=email,
    )