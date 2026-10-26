"""
BugReportDialog.py — Dialog di segnalazione bug con Privacy Notice
Per: MarkerClipManager.py
"""

import os
import sys
import subprocess
import platform
import webbrowser
from datetime import datetime
from typing import Dict


class BugReportDialog:
    """Gestore del dialog di bug report con privacy notice"""
    
    RECIPIENT = "tomfilmeditor.tools@gmail.com"
    PAYPAL_LINK = "https://paypal.me/acoffeefortom"
    
    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """Raccoglie info di sistema (senza dati sensibili)"""
        return {
            'os': platform.system(),
            'os_version': platform.release(),
            'python_version': platform.python_version(),
            'arch': platform.machine(),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    @staticmethod
    def create_privacy_notice(language: str = "IT") -> str:
        """Crea il testo della privacy notice. language="IT" -> italiano,
        qualunque altro valore -> inglese (vedi create_email_template)."""
        if language == "IT":
            return """
⚠️  PRIVACY NOTICE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Questo report contiene:
  ✓ Versione OS e Python
  ✓ Versione dello script
  ✓ Nomi dei tuoi timeline
  ✓ Timestamp delle operazioni
  ✓ Messaggi di errore (se presenti)

Questo report NON contiene:
  ✗ Password o credenziali
  ✗ API key o token
  ✗ Indirizzi IP
  ✗ Dettagli finanziari personali

Inviando il report, autorizzi Tom a usare questi dati
SOLO per diagnosticare il bug segnalato.

Se ci sono informazioni sensibili, puoi editarle
nell'email prima di inviare.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return """
⚠️  PRIVACY NOTICE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This report contains:
  ✓ OS and Python version
  ✓ Script version
  ✓ Your timeline names
  ✓ Operation timestamps
  ✓ Error messages (if any)

This report does NOT contain:
  ✗ Passwords or credentials
  ✗ API keys or tokens
  ✗ IP addresses
  ✗ Personal financial details

By sending this report, you authorize Tom to use this data
ONLY to diagnose the reported bug.

If there is any sensitive information, you can edit it
in the email before sending.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    @classmethod
    def create_email_template(cls, script_name: str, script_version: str, language: str = "IT") -> Dict[str, str]:
        """Crea il template dell'email pre-compilata. language="IT" -> italiano
        (comportamento originale, invariato). Qualunque altra lingua (le altre
        11 supportate dall'interfaccia) -> template in inglese, con una prima
        riga che chiede esplicitamente di scrivere in inglese: Tom legge
        italiano e inglese, non tutte e 12 le lingue dell'interfaccia."""
        sysinfo = cls.get_system_info()

        if language == "IT":
            subject = (
                f"Segnalazione Bug {script_name} v{script_version} | "
                f"{sysinfo['os']} {sysinfo['os_version']} | "
                f"Python {sysinfo['python_version']}"
            )
            body = f"""Script          : {script_name} v{script_version}
OS              : {sysinfo['os']} {sysinfo['os_version']}
Python          : {sysinfo['python_version']}
Data/Ora        : {sysinfo['timestamp']}

--- Descrizione del problema ---
[Descrivi qui quello che è accaduto]

--- Comportamento atteso ---
[Descrivi come dovrebbe funzionare]

--- Step per riprodurre il problema ---
1. [primo step]
2. [secondo step]
3. [terzo step]

--- Messaggio di errore (se presente) ---
[Copia qui il messaggio di errore esatto da console]

--- Screenshot o log ---
[Se disponibile, puoi allegare file di log]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Grazie per il bug report! Se puoi supportare lo sviluppo:
{cls.PAYPAL_LINK}

⚠️  Privacy: questo report contiene OS, timeline.
    Non contiene password o API key. Vedi il notice sopra.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        else:
            subject = (
                f"Bug Report {script_name} v{script_version} | "
                f"{sysinfo['os']} {sysinfo['os_version']} | "
                f"Python {sysinfo['python_version']}"
            )
            body = f"""Please write your bug report in English - this lets the developer
understand and act on it (reports in other languages unfortunately
cannot be processed).

Script          : {script_name} v{script_version}
OS              : {sysinfo['os']} {sysinfo['os_version']}
Python          : {sysinfo['python_version']}
Date/Time       : {sysinfo['timestamp']}

--- Description of the problem ---
[Describe here what happened]

--- Expected behavior ---
[Describe how it should work]

--- Steps to reproduce ---
1. [first step]
2. [second step]
3. [third step]

--- Error message (if any) ---
[Paste here the exact error message from the console]

--- Screenshot or log ---
[If available, you can attach a log file]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Thank you for the bug report! If you'd like to support development:
{cls.PAYPAL_LINK}

⚠️  Privacy: this report contains OS and timeline names.
    It does not contain passwords or API keys. See the notice above.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        return {
            'subject': subject,
            'body': body,
            'recipient': cls.RECIPIENT
        }

    @classmethod
    def show_privacy_notice(cls, script_name: str, script_version: str, language: str = "IT") -> Dict[str, str]:
        """Mostra la privacy notice e ritorna il template"""
        print(cls.create_privacy_notice(language))

        email_template = cls.create_email_template(script_name, script_version, language)
        
        print("\n📧 EMAIL PRE-COMPILATA PRONTA")
        print("━" * 60)
        print(f"\nOggetto: {email_template['subject']}")
        print(f"\nDestinatario: {email_template['recipient']}")
        print("\nCopia il testo qui sotto e incollalo nella tua email:\n")
        print(email_template['body'])
        print("\n" + "━" * 60)
        print("\n✉️  Metodi per inviare:")
        print("   1. Apri il tuo client email e incolla il testo sopra")
        print("   2. Oppure usa mailto: (clic sotto se disponibile)")
        
        return email_template
    
    @classmethod
    def send_email_macos(cls, script_name: str, script_version: str, language: str = "IT") -> bool:
        """Apre il client email su macOS (Mail.app)"""
        try:
            email_template = cls.create_email_template(script_name, script_version, language)
            
            # Escape per AppleScript
            subject = email_template['subject'].replace('"', '\\"')
            body = email_template['body'].replace('"', '\\"').replace('\n', '\\n')
            recipient = email_template['recipient']
            
            # AppleScript per Mail.app
            applescript = f"""
tell application "Mail"
    activate
    set newMessage to make new outgoing message with properties {{subject:"{subject}", content:"{body}", visible:true}}
    tell newMessage
        make new to recipient at end of to recipients with properties {{address:"{recipient}"}}
    end tell
end tell
            """
            
            # Esegui AppleScript
            subprocess.run(['osascript', '-e', applescript], check=True)
            return True
            
        except Exception as e:
            print(f"❌ Errore nell'apertura di Mail: {e}")
            return False
    
    @classmethod
    def send_email_windows(cls, script_name: str, script_version: str, language: str = "IT") -> bool:
        """Apre il client email su Windows"""
        try:
            email_template = cls.create_email_template(script_name, script_version, language)
            
            # Crea URL mailto: (con escape per spazi e caratteri speciali)
            subject = email_template['subject'].replace(' ', '%20')
            body_first_line = email_template['body'].split('\n')[0].replace(' ', '%20')
            
            mailto_link = (
                f"mailto:{email_template['recipient']}"
                f"?subject={subject}"
                f"&body={body_first_line}"
            )
            
            # Apri con browser
            webbrowser.open(mailto_link)
            return True
            
        except Exception as e:
            print(f"❌ Errore nell'apertura del client email: {e}")
            return False
    
    @classmethod
    def send_email(cls, script_name: str, script_version: str, language: str = "IT") -> bool:
        """Apre il client email (OS-specifico)"""
        system = platform.system()

        if system == 'Darwin':  # macOS
            return cls.send_email_macos(script_name, script_version, language)
        elif system == 'Windows':
            return cls.send_email_windows(script_name, script_version, language)
        else:  # Linux
            # Su Linux, mostra solo il template
            print("\n⚠️  Su Linux, copia il template e invia manualmente.")
            print(f"A: {cls.RECIPIENT}")
            return False
    
    @classmethod
    def create_button(cls, script_name: str, script_version: str) -> Dict[str, callable]:
        """
        Crea un bottone "Segnala Bug" per la GUI.
        Ritorna dict con 'label' e 'on_click' callback.
        """
        return {
            'label': '🐛 Segnala Bug',
            'tooltip': 'Segnala un bug — si aprirà un template email',
            'on_click': lambda: cls.handle_bug_report(script_name, script_version)
        }
    
    @classmethod
    def handle_bug_report(cls, script_name: str, script_version: str, language: str = "IT") -> None:
        """
        Handler per il bottone di bug report.
        Mostra privacy notice e prova ad aprire l'email client.
        language: lingua attiva dell'interfaccia al momento del click. "IT" ->
        template in italiano (comportamento originale). Qualunque altra lingua
        -> template in inglese, con richiesta esplicita di scrivere in inglese
        (Tom legge italiano e inglese, non tutte le lingue dell'interfaccia).
        """
        print("\n" + "=" * 70)
        print("🐛 SEGNALAZIONE BUG" if language == "IT" else "🐛 BUG REPORT")
        print("=" * 70)

        # Mostra privacy notice e template
        email_template = cls.show_privacy_notice(script_name, script_version, language)

        # Tenta di aprire il client email
        success = cls.send_email(script_name, script_version, language)
        
        if success:
            print("\n✅ Il tuo client email si è aperto con il template.")
            print("   Completa i dettagli e invia!")
        else:
            print("\n❌ Non è stato possibile aprire il client email automaticamente.")
            print("   Copia il template sopra e invia manualmente a:")
            print(f"   {email_template['recipient']}")
            print("\n💡 Suggerimento: puoi anche usare un mailto: link:")
            mailto = f"mailto:{email_template['recipient']}?subject={email_template['subject'].replace(' ', '%20')}"
            print(f"   {mailto}")


# Istanza globale per uso veloce
bug_report = BugReportDialog()
