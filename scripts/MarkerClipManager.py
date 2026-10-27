# ============================================================
# MarkerClipManager.py
# Interfaccia unica per gestire Marker Timeline e Clip in DaVinci Resolve:
# tabella con grafica nativa, filtri, editing multiplo, export/import CSV.
#
# Autore: Tommaso Feraboli — Film Editor
# Versione: vedi VERSION nel codice (aggiornata ad ogni release, non duplicata qui)
# Compatibile con DaVinci Resolve 19/20 (macOS e Windows)
#
# Licenza MIT — vedi LICENSE.md
# Copyright (c) 2024-2026 Tommaso Feraboli
# Permesso concesso a chiunque di usare, copiare, modificare e
# distribuire questo software, a condizione che il presente
# avviso di copyright rimanga in tutti i file derivati.
#
# Sostieni il progetto: https://paypal.me/acoffeefortom
# ============================================================
#
# OGGETTO DI PARTENZA: resolve / project / timeline corrente (ruler + tutte le tracce video/audio)
# PREREQUISITI: Resolve aperto, un progetto con una timeline caricata, PySide6 installato (`pip3 install PySide6`)
# LIMITAZIONI NOTE:
# - "Marker" (grafica): ricreata a codice con QPainter (forma "shield/pin" come in Resolve). Colori in
#   MARKER_COLORS forniti dall'utente (valori hex esatti presi da Resolve, non dall'API - non esposti
#   dallo scripting). La sagoma dell'icona resta una ricostruzione approssimata, non l'icona ufficiale.
# - "Keyword": non e' un campo nativo dei marker Resolve (verificato empiricamente: GetMarkers() non lo
#   espone, nessun metodo nascosto trovato). Viene salvato nel campo customData del marker: invisibile al
#   pannello Marker nativo di Resolve, leggibile/scrivibile solo da questo script.
# - "Name": campo testuale nativo del marker. Se il marker nasce da un commento/nota di revisione, Resolve
#   lo popola gia' col nome dell'account di chi ha scritto (verificato su marker reali), altrimenti resta
#   libero.
# - Conversione frame->timecode: legge fps dal progetto (project.GetSetting("timelineFrameRate")) e
#   rileva Drop Frame vs Non-Drop Frame dal formato di timeline.GetStartTimecode() (";" = drop frame),
#   con fallback "drop frame assunto attivo" se il progetto e' a 29.97/59.94 e il formato non e'
#   determinabile. Algoritmo SMPTE drop-frame (Duncan/Heidelberger) verificato contro i checkpoint noti
#   (frame 1800 -> 00:01:00;02, frame 17982 -> 00:10:00;00, frame 107892 -> 01:00:00;00) prima di
#   integrarlo. Se il progetto usa un fps insolito/variabile non standard il calcolo resta approssimato.
# - Calcolo TC per marker su clip retimati/velocizzati puo' non essere preciso (si basa su
#   GetSourceStartFrame() assumendo velocita' 100%).
# - "Cambia traccia" verso una traccia video/audio richiede che in quella posizione esista gia' un clip;
#   altrimenti l'operazione fallisce con avviso esplicito (Resolve non permette marker "nel vuoto" su una
#   traccia). Verso "TIMELINE" invece funziona sempre (marker ruler non ha vincoli di questo tipo).
# - Import/Export EDL marker: NON implementato qui - Resolve lo fa gia' nativamente
#   (Timeline > Markers > Export/Import). Questo script gestisce solo CSV.
# - Undo/Redo (Cmd+Z / Shift+Cmd+Z, pulsanti, History): copre colore/traccia/editing
#   inline/cancellazione/import CSV di questa sessione. Non persiste tra un riavvio e
#   l'altro dello script (history sempre vuota all'apertura) e non copre modifiche fatte
#   ai marker direttamente da Resolve mentre lo script e' aperto.
# - Istanza singola: lock file con PID in ~/Library/Application Support/RepertoireDB/.
#   Se il processo termina in modo anomalo (kill -9, crash) il lock resta sul disco ma
#   viene riconosciuto come "stale" e ignorato al prossimo avvio (nessun blocco falso).

import os
import sys
import csv
import glob
import json
import locale
import platform
import re
import subprocess
import webbrowser
import atexit
from urllib.parse import quote

# Bootstrap: Resolve lancia gli script con il python3 di sistema, che non ha PySide6
# (installarlo li' romperebbe l'ambiente gestito da Homebrew). Se PySide6 non e'
# importabile, ci si rilancia usando il virtualenv dedicato creato con:
#   python3 -m venv ~/.venvs/resolve_pyside6
#   ~/.venvs/resolve_pyside6/bin/pip install PySide6
_VENV_PYTHON = os.path.expanduser("~/.venvs/resolve_pyside6/bin/python3")
try:
    import PySide6  # noqa: F401
except ImportError:
    if sys.executable != _VENV_PYTHON and os.path.exists(_VENV_PYTHON):
        os.execv(_VENV_PYTHON, [_VENV_PYTHON] + sys.argv)
    raise RuntimeError(
        "PySide6 not found in the current python nor in the expected virtualenv "
        f"({_VENV_PYTHON}). Create it with:\n"
        "  python3 -m venv ~/.venvs/resolve_pyside6\n"
        "  ~/.venvs/resolve_pyside6/bin/pip install PySide6"
    )

sys.path.insert(0, "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")


def _trova_libreria_resolve():
    """Trova fusionscript, la libreria con cui Resolve parla con gli script.

    Perche' serve: il modulo di Blackmagic la cerca in un percorso FISSO
    (/Applications/DaVinci Resolve/...). Chi tiene piu' versioni di Resolve
    installate le rinomina per forza ("DaVinci Resolve 20", "DaVinci Resolve 19"),
    e a quel punto quel percorso non esiste piu' e nessuno script parte - con un
    errore che parla di 'fusionscript' e non dice cosa fare.
    Blackmagic prevede la variabile RESOLVE_SCRIPT_LIB per indicarla a mano: qui
    la si compila da soli, cosi' l'utente non deve sapere niente di tutto questo.

    Ordine: 1) quello che l'utente ha gia' impostato, 2) il Resolve aperto in
    questo momento (se ne hai tre installati, e' quello giusto), 3) il percorso
    standard, 4) le altre installazioni, dalla versione piu' alta in giu'.
    """
    gia_impostata = os.environ.get("RESOLVE_SCRIPT_LIB")
    if gia_impostata and os.path.exists(gia_impostata):
        return gia_impostata

    if sys.platform == "win32":
        candidati = [
            os.path.join(os.environ.get("PROGRAMFILES", r"C:\Program Files"),
                         "Blackmagic Design", "DaVinci Resolve", "fusionscript.dll"),
        ]
    else:
        candidati = []
        # Il Resolve effettivamente in esecuzione: lo si ricava dal processo.
        try:
            uscita = subprocess.run(["ps", "-A", "-o", "command="],
                                    capture_output=True, text=True, timeout=5).stdout
            for riga in uscita.splitlines():
                marcatore = ".app/Contents/MacOS/Resolve"
                if riga.endswith(marcatore):
                    bundle = riga[:-len("/Contents/MacOS/Resolve")]
                    candidati.append(os.path.join(bundle, "Contents", "Libraries",
                                                  "Fusion", "fusionscript.so"))
                    break
        except Exception:
            pass

        candidati.append("/Applications/DaVinci Resolve/DaVinci Resolve.app"
                         "/Contents/Libraries/Fusion/fusionscript.so")

        # Installazioni rinominate: "DaVinci Resolve 20", "DaVinci Resolve_18_6"...
        # Vanno ordinate per NUMERO di versione, non alfabeticamente: in ordine
        # alfabetico "DaVinci Resolve_18_6" finisce dopo "DaVinci Resolve 20"
        # (l'underscore viene dopo lo spazio), e si sceglierebbe la piu' vecchia.
        def _numero_versione(percorso):
            nome = percorso.split("/Applications/", 1)[-1].split("/", 1)[0]
            numeri = re.findall(r"\d+", nome)
            return tuple(int(n) for n in numeri) if numeri else (0,)

        altre = glob.glob("/Applications/*/DaVinci Resolve.app"
                          "/Contents/Libraries/Fusion/fusionscript.so")
        candidati.extend(sorted(altre, key=_numero_versione, reverse=True))

    for percorso in candidati:
        if percorso and os.path.exists(percorso):
            return percorso
    return None


_LIBRERIA = _trova_libreria_resolve()
if _LIBRERIA:
    os.environ["RESOLVE_SCRIPT_LIB"] = _LIBRERIA

try:
    import DaVinciResolveScript as dvr_script
except Exception as _errore:
    raise RuntimeError(
        "Non riesco a collegarmi a DaVinci Resolve: manca la libreria "
        "'fusionscript'.\n"
        f"Cercata qui: {_LIBRERIA or 'nessun percorso valido trovato'}\n"
        "Di solito succede quando Resolve non e' installato in "
        "/Applications/DaVinci Resolve/ (per esempio perche' tieni piu' versioni "
        "e le hai rinominate).\n"
        "Soluzione: apri Resolve prima di lanciare lo script, oppure imposta la "
        "variabile RESOLVE_SCRIPT_LIB col percorso completo di fusionscript.so.\n"
        f"Dettaglio tecnico: {_errore}"
    )

from log_manager import log
from BugReportDialog import BugReportDialog

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QComboBox, QLineEdit, QLabel, QFileDialog, QMessageBox, QHeaderView,
    QAbstractItemView, QInputDialog, QCheckBox, QDialog, QListWidget, QListWidgetItem
)
from PySide6.QtGui import QColor, QIcon, QPainter, QPainterPath, QPixmap, QKeySequence, QShortcut
from PySide6.QtCore import Qt, QRectF, QSize

# ============================================================
# LOGGING
# ============================================================
import datetime
from pathlib import Path

def get_log_path():
    """Ritorna il percorso del file di log cross-platform."""
    if sys.platform == "win32":
        local_appdata = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA")
        if not local_appdata:
            local_appdata = os.path.join(os.getenv("USERPROFILE", "."), "AppData", "Local")
        log_dir = os.path.join(local_appdata, "Blackmagic Design", "DaVinci Resolve", "Logs", "RepertoireDB")
    else:  # macOS, Linux
        home = os.getenv("HOME", ".")
        log_dir = os.path.join(home, "Library", "Logs", "RepertoireDB")

    Path(log_dir).mkdir(parents=True, exist_ok=True)
    return os.path.join(log_dir, "repertoire_db.log")

def log_message(level, message):
    """Scrive nel file di log con timestamp e livello."""
    try:
        log_path = get_log_path()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{level}] MarkerClipManager.py: {message}\n")
    except Exception as e:
        print(f"Errore logging: {e}", file=sys.stderr)

def rotate_log():
    """Cancella il log se più vecchio di 7 giorni."""
    try:
        log_path = get_log_path()
        if os.path.exists(log_path):
            age_days = (datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(log_path))).days
            if age_days > 7:
                os.remove(log_path)
                log_message("INFO", "Log rotato (> 7 giorni)")
    except Exception as e:
        print(f"Errore rotazione log: {e}", file=sys.stderr)

# ============================================================
# ISTANZA SINGOLA
#
# Lock file con il PID del processo corrente. Ad ogni avvio si controlla se il
# PID nel lock e' ancora vivo (os.kill(pid, 0), non uccide nulla, solleva solo
# se il processo non esiste): se si', un'altra istanza e' gia' aperta e questo
# avvio si ferma. Se il PID e' morto (crash, kill -9) il lock e' considerato
# "stale" e viene sovrascritto. Rilasciato automaticamente all'uscita (atexit),
# quindi resta valido anche se lo script viene interrotto da un'eccezione.
# ============================================================

_LOCK_DIR = os.path.expanduser("~/Library/Application Support/RepertoireDB")
_LOCK_FILE = os.path.join(_LOCK_DIR, "marker_clip_manager.lock")


def _is_pid_running(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _release_instance_lock():
    try:
        os.remove(_LOCK_FILE)
    except OSError:
        pass


def acquire_instance_lock():
    """Ritorna True se questa e' l'unica istanza (lock acquisito), False se
    un'altra istanza e' gia' in esecuzione."""
    Path(_LOCK_DIR).mkdir(parents=True, exist_ok=True)
    if os.path.exists(_LOCK_FILE):
        try:
            with open(_LOCK_FILE) as f:
                existing_pid = int(f.read().strip())
            if _is_pid_running(existing_pid):
                return False
        except (ValueError, OSError):
            pass  # lock illeggibile/corrotto -> trattalo come stale
    with open(_LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
    atexit.register(_release_instance_lock)
    return True


# ============================================================
# LINGUA / STRINGHE
#
# Le stringhe tradotte vivono in strings/<CODICE>.json (generate da
# extract_translations.py in CLAUDE_WORKS/MarkerClipManager/ a partire dai file
# di traduzione letteraria in 12 lingue - non rigenerare qui, editare i .md e
# rilanciare quello script). La lingua attiva si sceglie cosi':
#   1. Se esiste un file di preferenze salvato, si usa quella lingua.
#   2. Altrimenti (primo avvio), si rileva la lingua di sistema e si salva.
# Il selettore lingua nell'interfaccia scrive nello stesso file di preferenze;
# il cambio richiede un riavvio dello script (le label statiche non si
# ridisegnano a caldo, scelta deliberata per non dover tracciare un riferimento
# a ogni singolo widget di testo).
# ============================================================

SUPPORTED_LANGUAGES = {"IT", "FR", "DE", "JA", "KO", "PT", "RU", "ES", "TH", "VI", "ZH", "EN"}
LANGUAGE_ORDER = ["EN", "IT", "FR", "DE", "ES", "PT", "RU", "JA", "KO", "ZH", "VI", "TH"]
LANGUAGE_NAMES = {
    "EN": "English", "IT": "Italiano", "FR": "Français", "DE": "Deutsch",
    "JA": "日本語", "KO": "한국어", "PT": "Português", "RU": "Русский",
    "ES": "Español", "TH": "ไทย", "VI": "Tiếng Việt", "ZH": "中文",
}

_STRINGS_DIR = Path(__file__).resolve().parent / "strings"
_SETTINGS_FILE = os.path.join(_LOCK_DIR, "marker_clip_manager_settings.json")
_strings_cache = {}
CURRENT_LANGUAGE = "EN"


def detect_system_language():
    """Rileva la lingua di sistema al primo avvio, mappata sui 12 codici
    supportati. Fallback su EN se non rilevabile o non supportata."""
    candidates = []
    if platform.system() == "Darwin":
        try:
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleLocale"],
                capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0 and result.stdout.strip():
                candidates.append(result.stdout.strip())
        except Exception:
            pass
    try:
        loc = locale.getlocale()[0]
        if loc:
            candidates.append(loc)
    except Exception:
        pass
    for env_var in ("LANG", "LANGUAGE", "LC_ALL"):
        val = os.environ.get(env_var)
        if val:
            candidates.append(val)

    for candidate in candidates:
        code = candidate[:2].upper()
        if code in SUPPORTED_LANGUAGES:
            return code
    return "EN"


def load_strings(lang_code):
    if lang_code in _strings_cache:
        return _strings_cache[lang_code]
    path = _STRINGS_DIR / f"{lang_code}.json"
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        data = {}
    _strings_cache[lang_code] = data
    return data


def t(key, **kwargs):
    """Ritorna la stringa tradotta per la lingua attiva. Fallback: inglese,
    poi la chiave stessa - non deve mai far crashare l'interfaccia per una
    traduzione mancante."""
    text = load_strings(CURRENT_LANGUAGE).get(key)
    if text is None:
        text = load_strings("EN").get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


def load_language_setting():
    global CURRENT_LANGUAGE
    try:
        with open(_SETTINGS_FILE, encoding="utf-8") as f:
            data = json.load(f)
        lang = data.get("language")
        if lang in SUPPORTED_LANGUAGES:
            CURRENT_LANGUAGE = lang
            return
    except (OSError, json.JSONDecodeError):
        pass
    CURRENT_LANGUAGE = detect_system_language()
    save_language_setting(CURRENT_LANGUAGE)


def save_language_setting(lang_code):
    global CURRENT_LANGUAGE
    CURRENT_LANGUAGE = lang_code
    try:
        Path(_LOCK_DIR).mkdir(parents=True, exist_ok=True)
        with open(_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({"language": lang_code}, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


_ICON_SIZE = 20
_icon_cache = {}


def marker_icon(color_hex):
    """Ricrea la sagoma "shield/pin" dei marker Resolve: rettangolo arrotondato
    che termina con una punta triangolare in basso al centro."""
    if color_hex in _icon_cache:
        return _icon_cache[color_hex]

    s = _ICON_SIZE
    pixmap = QPixmap(s, s)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor(color_hex))

    body = QRectF(s * 0.14, s * 0.08, s * 0.72, s * 0.58)
    path = QPainterPath()
    path.addRoundedRect(body, s * 0.16, s * 0.16)

    tip = QPainterPath()
    tip.moveTo(body.left(), body.bottom() - s * 0.05)
    tip.lineTo(body.right(), body.bottom() - s * 0.05)
    tip.lineTo(s * 0.5, s * 0.94)
    tip.closeSubpath()
    path.addPath(tip)

    painter.drawPath(path)
    painter.end()

    icon = QIcon(pixmap)
    _icon_cache[color_hex] = icon
    return icon

MARKER_COLORS = {
    "Blue": "#0081E2", "Cyan": "#00D3CF", "Green": "#00B20F", "Yellow": "#FF9718",
    "Red": "#FC000F", "Pink": "#FF00C7", "Purple": "#9C00FC", "Fuchsia": "#D6006F",
    "Rose": "#FF99B9", "Lavender": "#A391C7", "Sky": "#68E5FC", "Mint": "#2EE018",
    "Lemon": "#DAEA5F", "Sand": "#D08D60", "Cocoa": "#754F44", "Cream": "#F8EBE1",
}

COL_SWATCH, COL_TRACK, COL_TCIN, COL_TCOUT, COL_DUR, COL_COLOR, COL_NAME, COL_KEYWORD, COL_NOTE = range(9)
# Chiavi di traduzione delle intestazioni colonna (testo vero risolto a runtime via t(),
# dopo che la lingua e' stata caricata - vedi _build_table()).
HEADER_KEYS = [
    "label.marker_column", "label.track", "label.tc_in", "label.tc_out",
    "label.duration", "label.color", "label.name", "label.keyword", "label.note",
]
EDITABLE_COLS = (COL_NAME, COL_KEYWORD, COL_NOTE)
CSV_FIELDS = ["track", "tc_in", "tc_out", "duration", "color", "name", "keyword", "note"]

VERSION = "1.4.7"
BUG_EMAIL = "tomfilmeditor.tools@gmail.com"
COFFEE_URL = "https://paypal.me/acoffeefortom"


# ---------------------------------------------------------------------------
# Branding
# ---------------------------------------------------------------------------

def get_resolve_version(resolve):
    try:
        v = resolve.GetVersionString()
        if v:
            return v
    except Exception:
        pass
    try:
        v = resolve.GetVersion()
        if v and len(v) >= 2:
            return f"{v[0]}.{v[1]}"
    except Exception:
        pass
    return "Unknown"


def report_bug(resolve, script_name, version):
    """Apre il dialog di segnalazione bug con privacy notice. Il template
    (oggetto/corpo email) segue la lingua attiva dell'interfaccia: italiano se
    CURRENT_LANGUAGE è IT, altrimenti inglese - Tom legge italiano e inglese,
    non tutte le 12 lingue supportate dall'interfaccia."""
    log.info("MarkerClipManager.py", f"Segnalazione bug aperta - {script_name} v{version} - lingua: {CURRENT_LANGUAGE}")

    # Usa il modulo BugReportDialog per mostrare privacy notice e aprire il client email
    BugReportDialog.handle_bug_report(script_name, version, language=CURRENT_LANGUAGE)

    # Apri PayPal
    webbrowser.open(COFFEE_URL)


def offer_coffee():
    webbrowser.open(COFFEE_URL)


def open_readme():
    """Apre il README nella lingua attiva. Se non esiste (lingua non ancora
    generata/rimossa) ricade sull'inglese, che deve sempre esistere."""
    readme_dir = Path(__file__).resolve().parent
    readme_path = readme_dir / f"MarkerClipManager_README_{CURRENT_LANGUAGE}.txt"
    if not readme_path.is_file():
        readme_path = readme_dir / "MarkerClipManager_README_EN.txt"
    webbrowser.open(readme_path.as_uri())


# ---------------------------------------------------------------------------
# Connessione Resolve
# ---------------------------------------------------------------------------

def connect_resolve():
    resolve = dvr_script.scriptapp("Resolve")
    if not resolve:
        raise RuntimeError("Cannot reach Resolve. Make sure it is running.")
    project = resolve.GetProjectManager().GetCurrentProject()
    if not project:
        raise RuntimeError("No project open.")
    timeline = project.GetCurrentTimeline()
    if not timeline:
        raise RuntimeError("No current timeline.")
    log.info("MarkerClipManager.py", "Resolve connesso")
    return resolve, project, timeline


def get_fps(project):
    try:
        return float(project.GetSetting("timelineFrameRate"))
    except (TypeError, ValueError):
        return 25.0


def is_drop_frame_fps(fps):
    """Solo 29.97 e 59.94 supportano il drop-frame in SMPTE."""
    return abs(fps - 29.97) < 0.05 or abs(fps - 59.94) < 0.05


def timeline_uses_drop_frame(timeline, fps):
    """Rileva Drop Frame vs Non-Drop Frame dal formato di GetStartTimecode()
    (";" prima dei frame = drop frame, per convenzione SMPTE che Resolve segue).
    Se il fps del progetto non supporta il drop-frame, esclude subito senza
    bisogno di leggere il timecode."""
    if not is_drop_frame_fps(fps):
        return False
    try:
        tc = timeline.GetStartTimecode()
        if tc:
            return ";" in tc
    except Exception:
        pass
    return True  # fps 29.97/59.94 senza indicazione esplicita -> assumi drop frame (convenzione piu' comune)


# ---------------------------------------------------------------------------
# Timecode
#
# Formula semplice frame/fps per timeline non-drop-frame. Per 29.97/59.94 in
# drop frame usa l'algoritmo SMPTE drop-frame (Duncan/Heidelberger), verificato
# contro i checkpoint canonici prima di integrarlo:
#   frame 1800   -> 00:01:00;02  (salta le label ;00 e ;01 a inizio minuto)
#   frame 17982  -> 00:10:00;00  (ogni decimo minuto non droppa)
#   frame 107892 -> 01:00:00;00  (1 ora reale = 107892 frame, non 108000)
# ---------------------------------------------------------------------------

def _df_constants(fps):
    drop_frames = round(fps * 0.066666)
    frames_per_10min = round(fps * 60 * 10)
    fps_round = round(fps)
    frames_per_minute = fps_round * 60 - drop_frames
    frames_per_24h = round(fps * 3600) * 24
    return drop_frames, frames_per_10min, fps_round, frames_per_minute, frames_per_24h


def _frame_to_tc_dropframe(frame, fps):
    drop_frames, frames_per_10min, fps_round, frames_per_minute, frames_per_24h = _df_constants(fps)
    frame = frame % frames_per_24h
    d, m = divmod(frame, frames_per_10min)
    if m > drop_frames:
        frame = frame + (drop_frames * 9 * d) + drop_frames * ((m - drop_frames) // frames_per_minute)
    else:
        frame = frame + drop_frames * 9 * d
    ff = frame % fps_round
    ss = (frame // fps_round) % 60
    mm = (frame // fps_round // 60) % 60
    hh = frame // fps_round // 3600
    return f"{hh:02d}:{mm:02d}:{ss:02d};{ff:02d}"


def _tc_dropframe_to_frame(tc, fps):
    drop_frames, frames_per_10min, fps_round, frames_per_minute, frames_per_24h = _df_constants(fps)
    hh, mm, ss, ff = (int(x) for x in tc.strip().replace(";", ":").split(":"))
    total_minutes = 60 * hh + mm
    frame_number = (fps_round * 3600 * hh) + (fps_round * 60 * mm) + (fps_round * ss) + ff
    frame_number -= drop_frames * (total_minutes - total_minutes // 10)
    return frame_number


def frame_to_tc(frame, fps, drop_frame=False):
    frame = max(0, int(frame))
    if drop_frame:
        return _frame_to_tc_dropframe(frame, fps)
    fps_i = max(1, int(round(fps)))
    ff = frame % fps_i
    total_sec = frame // fps_i
    hh = total_sec // 3600
    mm = (total_sec % 3600) // 60
    ss = total_sec % 60
    return f"{hh:02d}:{mm:02d}:{ss:02d}:{ff:02d}"


def tc_to_frame(tc, fps, drop_frame=False):
    if drop_frame or ";" in tc:
        return _tc_dropframe_to_frame(tc, fps)
    fps_i = max(1, int(round(fps)))
    hh, mm, ss, ff = (int(x) for x in tc.strip().split(":"))
    return ((hh * 3600 + mm * 60 + ss) * fps_i) + ff


# ---------------------------------------------------------------------------
# Scansione marker
# ---------------------------------------------------------------------------

def scan_markers(timeline):
    rows = []
    tl_start = timeline.GetStartFrame()

    for frame_id, data in (timeline.GetMarkers() or {}).items():
        rows.append({
            "scope_obj": timeline, "frame_id": frame_id,
            "abs_frame": tl_start + frame_id, "track": "TIMELINE",
            "color": data.get("color", ""), "duration": data.get("duration", 1),
            "name": data.get("name", ""), "note": data.get("note", ""),
            "keyword": data.get("customData", ""),
        })

    for track_type, prefix in (("video", "V"), ("audio", "A")):
        for idx in range(1, timeline.GetTrackCount(track_type) + 1):
            for item in (timeline.GetItemListInTrack(track_type, idx) or []):
                markers = item.GetMarkers() or {}
                if not markers:
                    continue
                src_start = item.GetSourceStartFrame()
                item_start = item.GetStart()
                for frame_id, data in markers.items():
                    rows.append({
                        "scope_obj": item, "frame_id": frame_id,
                        "abs_frame": item_start + (frame_id - src_start),
                        "track": f"{prefix}{idx}",
                        "color": data.get("color", ""), "duration": data.get("duration", 1),
                        "name": data.get("name", ""), "note": data.get("note", ""),
                        "keyword": data.get("customData", ""),
                    })

    rows.sort(key=lambda r: r["abs_frame"])
    return rows


def find_item_at(timeline, track_type, track_index, abs_frame):
    for item in (timeline.GetItemListInTrack(track_type, track_index) or []):
        if item.GetStart() <= abs_frame <= item.GetEnd():
            return item
    return None


# ---------------------------------------------------------------------------
# Azioni sui marker (cancellazione + ricreazione, unico modo garantito dall'API
# per modificare colore/nome/nota/traccia di un marker esistente)
# ---------------------------------------------------------------------------

def replace_marker(row, new_scope_obj, new_frame_id, color=None, name=None, note=None,
                    duration=None, keyword=None):
    color = row["color"] if color is None else color
    name = row["name"] if name is None else name
    note = row["note"] if note is None else note
    duration = row["duration"] if duration is None else duration
    keyword = row["keyword"] if keyword is None else keyword

    row["scope_obj"].DeleteMarkerAtFrame(row["frame_id"])
    ok = new_scope_obj.AddMarker(new_frame_id, color, name, note, duration, keyword or "")
    if ok:
        row["scope_obj"] = new_scope_obj
        row["frame_id"] = new_frame_id
        row["color"], row["name"], row["note"] = color, name, note
        row["duration"], row["keyword"] = duration, keyword
    return ok


def change_track(timeline, row, target_label):
    abs_frame = row["abs_frame"]
    tl_start = timeline.GetStartFrame()

    if target_label == "TIMELINE":
        new_frame_id = abs_frame - tl_start
        if replace_marker(row, timeline, new_frame_id):
            row["track"] = "TIMELINE"
            return True
        return False

    track_type = "video" if target_label.startswith("V") else "audio"
    track_index = int(target_label[1:])
    target_item = find_item_at(timeline, track_type, track_index, abs_frame)
    if target_item is None:
        return False
    new_frame_id = target_item.GetSourceStartFrame() + (abs_frame - target_item.GetStart())
    if replace_marker(row, target_item, new_frame_id):
        row["track"] = target_label
        return True
    return False


def delete_marker(row):
    return row["scope_obj"].DeleteMarkerAtFrame(row["frame_id"])


# ---------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------

def export_csv(path, rows, fps, drop_frame):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                "track": r["track"],
                "tc_in": frame_to_tc(r["abs_frame"], fps, drop_frame),
                "tc_out": frame_to_tc(r["abs_frame"] + r["duration"] - 1, fps, drop_frame),
                "duration": r["duration"], "color": r["color"], "name": r["name"],
                "keyword": r["keyword"], "note": r["note"],
            })


def import_csv(path, timeline, fps, drop_frame):
    tl_start = timeline.GetStartFrame()
    added, skipped, created = 0, [], []
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                abs_frame = tc_to_frame(row["tc_in"], fps, drop_frame)
            except (KeyError, ValueError):
                skipped.append(row)
                continue
            duration = int(row.get("duration") or 1)
            color = row.get("color") or "Blue"
            name = row.get("name") or ""
            note = row.get("note") or ""
            keyword = row.get("keyword") or ""
            track = (row.get("track") or "TIMELINE").strip()

            if track == "TIMELINE":
                scope_obj, frame_id = timeline, abs_frame - tl_start
            else:
                track_type = "video" if track.upper().startswith("V") else "audio"
                try:
                    track_index = int(track[1:])
                except ValueError:
                    skipped.append(row)
                    continue
                item = find_item_at(timeline, track_type, track_index, abs_frame)
                if item is None:
                    skipped.append(row)
                    continue
                scope_obj = item
                frame_id = item.GetSourceStartFrame() + (abs_frame - item.GetStart())

            ok = scope_obj.AddMarker(frame_id, color, name, note, duration, keyword)
            if ok:
                added += 1
                created.append({
                    "scope_obj": scope_obj, "frame_id": frame_id, "color": color,
                    "name": name, "note": note, "duration": duration, "keyword": keyword,
                })
            else:
                skipped.append(row)
    return added, skipped, created


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

class MarkerManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        load_language_setting()
        log.info("MarkerClipManager.py", f"GUI inizializzata - PySide6 caricato - lingua: {CURRENT_LANGUAGE}")
        self.resolve, self.project, self.timeline = connect_resolve()
        self.fps = get_fps(self.project)
        self.drop_frame = timeline_uses_drop_frame(self.timeline, self.fps)
        self.rows = []

        self.confirm_actions = True
        # Modello history lineare con puntatore (stile "History panel"): self.history
        # e' la lista completa delle azioni fatte, self.history_pos indica quante ne
        # sono applicate in questo momento. Undo/redo/jump muovono solo il puntatore
        # e applicano gli snapshot prima/dopo attraversati - non due stack separati.
        self.history = []
        self.history_pos = 0

        self.setWindowTitle(
            f"MarkerClipManager v{VERSION} — {t('app.subtitle')}"
            f"  |  © Tommaso Feraboli Film Editor"
        )
        self.resize(1200, 600)

        root = QVBoxLayout(self)
        root.addLayout(self._build_header())
        root.addLayout(self._build_toolbar())
        root.addLayout(self._build_filters())
        self.table = self._build_table()
        root.addWidget(self.table)
        self._build_shortcuts()

        self.refresh()

    # -- costruzione UI ----------------------------------------------------

    def _build_shortcuts(self):
        # QKeySequence.Undo/Redo mappano automaticamente a Cmd+Z / Shift+Cmd+Z su
        # macOS e Ctrl+Z / Ctrl+Shift+Z su Windows - non serve hardcodare i tasti.
        QShortcut(QKeySequence(QKeySequence.StandardKey.Undo), self, activated=self.undo)
        QShortcut(QKeySequence(QKeySequence.StandardKey.Redo), self, activated=self.redo)
        # Tasto Delete della tastiera = comando "Delete" della UI. Scoped alla tabella
        # (Qt.WidgetShortcut) cosi' non scatta mentre si scrive nel campo filtro Keyword
        # o durante l'editing inline di una cella (l'editor del campo intercetta prima
        # il tasto per cancellare caratteri, come atteso).
        for key in (Qt.Key_Delete, Qt.Key_Backspace):
            sc = QShortcut(QKeySequence(key), self.table, activated=self.action_delete)
            sc.setContext(Qt.WidgetShortcut)

    def _build_header(self):
        bar = QHBoxLayout()

        title = QLabel(f"MarkerClipManager v{VERSION}")
        title_font = title.font()
        title_font.setPixelSize(20)
        title.setFont(title_font)
        title.setStyleSheet("color: #DCDCDC;")
        bar.addWidget(title)
        bar.addStretch()

        credit = QVBoxLayout()
        credit.setSpacing(0)
        credit_line = QLabel("© Tommaso Feraboli Film Editor")
        credit_line.setAlignment(Qt.AlignRight)
        credit_font = credit_line.font()
        credit_font.setPixelSize(13)
        credit_line.setFont(credit_font)
        credit_line.setStyleSheet("color: #D2D2D2;")
        license_line = QLabel("Licenza MIT")
        license_line.setAlignment(Qt.AlignRight)
        license_font = license_line.font()
        license_font.setPixelSize(10)
        license_font.setItalic(True)
        license_line.setFont(license_font)
        license_line.setStyleSheet("color: #828282;")
        credit.addWidget(credit_line)
        credit.addWidget(license_line)
        bar.addLayout(credit)

        self.language_combo = QComboBox()
        for code in LANGUAGE_ORDER:
            self.language_combo.addItem(LANGUAGE_NAMES[code], code)
        idx = self.language_combo.findData(CURRENT_LANGUAGE)
        self.language_combo.setCurrentIndex(idx if idx >= 0 else 0)
        self.language_combo.setToolTip("Interface language (restart required after changing)")
        self.language_combo.currentIndexChanged.connect(
            lambda: self._on_language_changed(self.language_combo.currentData())
        )
        bar.addWidget(self.language_combo)

        guide_btn = QPushButton("📖")
        guide_btn.setFixedSize(44, 44)
        guide_btn.setToolTip(t("tooltip.guide"))
        guide_btn.clicked.connect(open_readme)
        guide_btn.setStyleSheet(
            "QPushButton{font-size:22px;"
            "background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #8B7B1A,stop:1 #5A4E0A);"
            "color:#FFFFFF;border-radius:5px;border:1px solid #5A4E0A;}"
            "QPushButton:hover{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #9F8F2E,stop:1 #8B7B1A);}"
        )
        bar.addWidget(guide_btn)

        bug_btn = QPushButton("🐛")
        bug_btn.setFixedSize(44, 44)
        bug_btn.setToolTip(t("tooltip.bug", BUG_EMAIL=BUG_EMAIL))
        bug_btn.clicked.connect(lambda: report_bug(self.resolve, "MarkerClipManager.py", VERSION))
        bug_btn.setStyleSheet(
            "QPushButton{font-size:22px;"
            "background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #B03020,stop:1 #7A1E10);"
            "color:#FFFFFF;border-radius:5px;border:1px solid #7A1E10;}"
            "QPushButton:hover{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #C84030,stop:1 #B03020);}"
        )
        bar.addWidget(bug_btn)

        coffee_btn = QPushButton("☕")
        coffee_btn.setFixedSize(44, 44)
        coffee_btn.setToolTip(t("tooltip.coffee"))
        coffee_btn.clicked.connect(offer_coffee)
        coffee_btn.setStyleSheet(
            "QPushButton{font-size:22px;"
            "background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #2196C0,stop:1 #1565A0);"
            "color:#FFFFFF;border-radius:5px;border:1px solid #1565A0;}"
            "QPushButton:hover{background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #2AA8D8,stop:1 #2196C0);}"
        )
        bar.addWidget(coffee_btn)

        return bar

    def _build_toolbar(self):
        bar = QHBoxLayout()
        specs = [
            (t("label.refresh"), self.refresh),
            (t("label.change_color"), self.action_change_color),
            (t("label.change_track"), self.action_change_track),
            (t("label.delete"), self.action_delete),
            (t("label.export_csv"), self.action_export_csv),
            (t("label.import_csv"), self.action_import_csv),
        ]
        for label, slot in specs:
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            bar.addWidget(btn)

        self.undo_btn = QPushButton(t("label.undo"))
        self.undo_btn.clicked.connect(self.undo)
        bar.addWidget(self.undo_btn)
        self.redo_btn = QPushButton(t("label.redo"))
        self.redo_btn.clicked.connect(self.redo)
        bar.addWidget(self.redo_btn)
        history_btn = QPushButton(t("label.history"))
        history_btn.clicked.connect(self.show_history_dialog)
        bar.addWidget(history_btn)

        confirm_check = QCheckBox(t("label.confirm_checkbox"))
        confirm_check.setChecked(self.confirm_actions)
        confirm_check.toggled.connect(self._set_confirm_actions)
        bar.addWidget(confirm_check)

        bar.addStretch()
        return bar

    def _set_confirm_actions(self, enabled):
        self.confirm_actions = enabled
        log.info("MarkerClipManager.py", f"Confirm before delete: {'ON' if enabled else 'OFF'}")

    def _on_language_changed(self, lang_code):
        if lang_code == CURRENT_LANGUAGE:
            return
        save_language_setting(lang_code)
        log.info("MarkerClipManager.py", f"Language preference changed to {lang_code}")
        QMessageBox.information(
            self, "MarkerClipManager",
            "Language preference saved. Restart MarkerClipManager for the change to take effect."
        )

    def _build_filters(self):
        bar = QHBoxLayout()
        self.filter_color = QComboBox()
        self.filter_track = QComboBox()
        self.filter_name = QComboBox()
        self.filter_keyword = QLineEdit()
        self.filter_keyword.setPlaceholderText(t("placeholder.keyword_filter"))

        for label, combo in ((t("label.color"), self.filter_color), (t("label.track"), self.filter_track),
                              (t("label.author_name"), self.filter_name)):
            bar.addWidget(QLabel(label))
            bar.addWidget(combo)
            combo.currentIndexChanged.connect(self.apply_filters)
        bar.addWidget(QLabel(t("label.keyword")))
        bar.addWidget(self.filter_keyword)
        self.filter_keyword.textChanged.connect(self.apply_filters)

        reset_btn = QPushButton(t("label.reset_filters"))
        reset_btn.clicked.connect(self.reset_filters)
        bar.addWidget(reset_btn)
        bar.addStretch()
        return bar

    def _build_table(self):
        table = QTableWidget(0, len(HEADER_KEYS))
        table.setHorizontalHeaderLabels([t(k) for k in HEADER_KEYS])
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        table.setSortingEnabled(True)
        table.setIconSize(QSize(_ICON_SIZE, _ICON_SIZE))
        table.horizontalHeader().setSectionResizeMode(COL_NOTE, QHeaderView.Stretch)
        table.itemChanged.connect(self.on_item_changed)
        table.cellClicked.connect(self.on_cell_clicked)
        return table

    # -- popolazione tabella -------------------------------------------------

    def refresh(self):
        self.rows = scan_markers(self.timeline)
        log.info("MarkerClipManager.py", f"Timeline caricata - {len(self.rows)} marker trovati")
        self._populate_filter_options()
        self._populate_table(self.rows)

    def _populate_filter_options(self):
        for combo, key, extra in (
            (self.filter_color, "color", t("label.all_colors")),
            (self.filter_track, "track", t("label.all_tracks")),
            (self.filter_name, "name", t("label.all_authors")),
        ):
            current = combo.currentText()
            combo.blockSignals(True)
            combo.clear()
            values = sorted({r[key] for r in self.rows if r[key]})
            combo.addItem(extra)
            combo.addItems(values)
            idx = combo.findText(current)
            combo.setCurrentIndex(idx if idx >= 0 else 0)
            combo.blockSignals(False)

    def _populate_table(self, rows):
        self.table.blockSignals(True)
        self.table.setSortingEnabled(False)  # evita riordino/scarto dati durante setItem() riga per riga
        self.table.setRowCount(0)
        for r in rows:
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)

            swatch = QTableWidgetItem()
            swatch.setFlags(swatch.flags() & ~Qt.ItemIsEditable)
            swatch.setIcon(marker_icon(MARKER_COLORS.get(r["color"], "#888888")))
            self.table.setItem(row_idx, COL_SWATCH, swatch)

            values = {
                COL_TRACK: r["track"],
                COL_TCIN: frame_to_tc(r["abs_frame"], self.fps, self.drop_frame),
                COL_TCOUT: frame_to_tc(r["abs_frame"] + r["duration"] - 1, self.fps, self.drop_frame),
                COL_DUR: str(r["duration"]),
                COL_COLOR: r["color"],
                COL_NAME: r["name"],
                COL_KEYWORD: r["keyword"],
                COL_NOTE: r["note"],
            }
            for col, text in values.items():
                item = QTableWidgetItem(text)
                if col not in EDITABLE_COLS:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row_idx, col, item)
            self.table.item(row_idx, 0).setData(Qt.UserRole, r)
        self.table.setSortingEnabled(True)
        self.table.blockSignals(False)
        self.apply_filters()

    # -- filtri ---------------------------------------------------------------

    def apply_filters(self):
        # Indice 0 = sempre la voce "tutti/e" (qualunque sia il testo tradotto),
        # non un confronto sul testo - altrimenti si rompe in ogni lingua diversa
        # dall'inglese (il testo non inizia piu' per forza con "All ").
        color, color_active = self.filter_color.currentText(), self.filter_color.currentIndex() > 0
        track, track_active = self.filter_track.currentText(), self.filter_track.currentIndex() > 0
        name, name_active = self.filter_name.currentText(), self.filter_name.currentIndex() > 0
        keyword = self.filter_keyword.text().strip().lower()

        for row_idx in range(self.table.rowCount()):
            r = self.table.item(row_idx, 0).data(Qt.UserRole)
            visible = True
            if color_active and r["color"] != color:
                visible = False
            if track_active and r["track"] != track:
                visible = False
            if name_active and r["name"] != name:
                visible = False
            if keyword and keyword not in r["keyword"].lower():
                visible = False
            self.table.setRowHidden(row_idx, not visible)

    def reset_filters(self):
        self.filter_color.setCurrentIndex(0)
        self.filter_track.setCurrentIndex(0)
        self.filter_name.setCurrentIndex(0)
        self.filter_keyword.clear()

    # -- selezione --------------------------------------------------------

    def _selected_rows(self):
        rows_data = []
        seen = set()
        for item in self.table.selectedItems():
            if item.row() in seen:
                continue
            seen.add(item.row())
            rows_data.append((item.row(), self.table.item(item.row(), 0).data(Qt.UserRole)))
        return rows_data

    # -- undo/redo/history --------------------------------------------------
    #
    # Ogni azione che modifica marker registra uno snapshot "prima" e uno "dopo"
    # per ciascun marker toccato. before[i]/after[i] possono essere None:
    #   before=None -> il marker non esisteva ancora (es. creato da un import)
    #   after=None  -> il marker non esiste piu' (es. cancellato)
    # Cosi' un'unica coppia di primitive (_apply_state/_remove_state) copre
    # colore, traccia, editing di Name/Keyword/Note, cancellazione e import CSV.

    @staticmethod
    def _snapshot(row):
        return {
            "scope_obj": row["scope_obj"], "frame_id": row["frame_id"],
            "color": row["color"], "name": row["name"], "note": row["note"],
            "duration": row["duration"], "keyword": row["keyword"],
        }

    @staticmethod
    def _apply_state(state):
        state["scope_obj"].AddMarker(
            state["frame_id"], state["color"], state["name"],
            state["note"], state["duration"], state["keyword"] or ""
        )

    @staticmethod
    def _remove_state(state):
        state["scope_obj"].DeleteMarkerAtFrame(state["frame_id"])

    def _push_history(self, label, before, after):
        """before/after: liste parallele di snapshot (o None). Registra l'azione
        gia' eseguita e scarta qualunque ramo redo precedente (comportamento
        standard: fare una nuova azione dopo un undo invalida i redo pendenti)."""
        self.history = self.history[:self.history_pos]
        self.history.append({"label": label, "before": before, "after": after})
        self.history_pos = len(self.history)

    def undo(self):
        if self.history_pos == 0:
            return
        self.history_pos -= 1
        entry = self.history[self.history_pos]
        for before, after in zip(entry["before"], entry["after"]):
            if after is not None:
                self._remove_state(after)
            if before is not None:
                self._apply_state(before)
        log.info("MarkerClipManager.py", f"Undo: {entry['label']}")
        self.refresh()

    def redo(self):
        if self.history_pos >= len(self.history):
            return
        entry = self.history[self.history_pos]
        for before, after in zip(entry["before"], entry["after"]):
            if before is not None:
                self._remove_state(before)
            if after is not None:
                self._apply_state(after)
        self.history_pos += 1
        log.info("MarkerClipManager.py", f"Redo: {entry['label']}")
        self.refresh()

    def jump_to_history(self, target_pos):
        target_pos = max(0, min(target_pos, len(self.history)))
        while self.history_pos > target_pos:
            self.undo()
        while self.history_pos < target_pos:
            self.redo()

    def show_history_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle(t("label.history"))
        dlg.resize(420, 400)
        layout = QVBoxLayout(dlg)
        listw = QListWidget()
        listw.addItem(QListWidgetItem(t("dlg.history.initial_state")))
        for entry in self.history:
            listw.addItem(QListWidgetItem(entry["label"]))
        listw.setCurrentRow(self.history_pos)

        def on_double_click(item):
            self.jump_to_history(listw.row(item))
            listw.setCurrentRow(self.history_pos)

        listw.itemDoubleClicked.connect(on_double_click)
        layout.addWidget(QLabel(t("dlg.history.instructions")))
        layout.addWidget(listw)
        dlg.exec()

    # -- azioni toolbar -----------------------------------------------------

    def action_change_color(self):
        selected = self._selected_rows()
        if not selected:
            QMessageBox.information(self, t("label.change_color"), t("dlg.none_selected"))
            return
        color, ok = QInputDialog.getItem(self, t("label.change_color"), t("dlg.change_color.prompt"),
                                          list(MARKER_COLORS.keys()), 0, False)
        if not ok:
            return
        before, after = [], []
        for _, r in selected:
            before.append(self._snapshot(r))
            replace_marker(r, r["scope_obj"], r["frame_id"], color=color)
            after.append(self._snapshot(r))
        self._push_history(t("history.change_color", color=color, n=len(selected)), before, after)
        self.refresh()

    def action_change_track(self):
        selected = self._selected_rows()
        if not selected:
            QMessageBox.information(self, t("label.change_track"), t("dlg.none_selected"))
            return
        options = ["TIMELINE"]
        options += [f"V{i}" for i in range(1, self.timeline.GetTrackCount("video") + 1)]
        options += [f"A{i}" for i in range(1, self.timeline.GetTrackCount("audio") + 1)]
        target, ok = QInputDialog.getItem(self, t("label.change_track"), t("dlg.change_track.prompt"),
                                           options, 0, False)
        if not ok:
            return
        failed = 0
        before, after = [], []
        for _, r in selected:
            b = self._snapshot(r)
            if change_track(self.timeline, r, target):
                before.append(b)
                after.append(self._snapshot(r))
            else:
                failed += 1
        if before:
            self._push_history(t("history.change_track", target=target, n=len(before)), before, after)
        self.refresh()
        if failed:
            QMessageBox.warning(self, t("label.change_track"),
                                 t("dlg.change_track.warning", failed=failed, target=target))

    def action_delete(self):
        selected = self._selected_rows()
        if not selected:
            QMessageBox.information(self, t("label.delete"), t("dlg.none_selected"))
            return
        if self.confirm_actions:
            if QMessageBox.question(self, t("label.delete"),
                                     t("dlg.delete.confirm", n=len(selected))) != QMessageBox.Yes:
                return
        before = [self._snapshot(r) for _, r in selected]
        for _, r in selected:
            delete_marker(r)
        self._push_history(t("history.delete", n=len(selected)), before, [None] * len(before))
        self.refresh()

    def action_export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, t("label.export_csv"), "", "CSV (*.csv)")
        if not path:
            return
        try:
            export_csv(path, self.rows, self.fps, self.drop_frame)
            log.info("MarkerClipManager.py", f"Export CSV completato - {len(self.rows)} marker scritti")
            QMessageBox.information(self, t("label.export_csv"),
                                     t("dlg.export_csv.success", n=len(self.rows), path=path))
        except Exception as e:
            log.error("MarkerClipManager.py", "Errore durante export CSV", {"error": str(e)})
            QMessageBox.critical(self, t("label.export_csv"), t("dlg.export_csv.error", error=str(e)))

    def action_import_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, t("label.import_csv"), "", "CSV (*.csv)")
        if not path:
            return
        try:
            added, skipped, created = import_csv(path, self.timeline, self.fps, self.drop_frame)
            log.info("MarkerClipManager.py", f"Import CSV completato - {added} marker importati")
            if created:
                self._push_history(t("history.import_csv", n=added), [None] * len(created), created)
            self.refresh()
            msg = t("dlg.import_csv.success", n=added)
            if skipped:
                msg += "\n" + t("dlg.import_csv.skipped", n=len(skipped))
            QMessageBox.information(self, t("label.import_csv"), msg)
        except Exception as e:
            log.error("MarkerClipManager.py", "Errore durante import CSV", {"error": str(e)})
            QMessageBox.critical(self, t("label.import_csv"), t("dlg.import_csv.error", error=str(e)))

    # -- click su un marker: calamita la testina timeline sulla sua posizione --

    def on_cell_clicked(self, row, column):
        item = self.table.item(row, 0)
        if item is None:
            return
        r = item.data(Qt.UserRole)
        if r is None:
            return
        self.timeline.SetCurrentTimecode(frame_to_tc(r["abs_frame"], self.fps, self.drop_frame))

    # -- editing inline colonne ipertestuali (Name/Keyword/Note) -----------

    def on_item_changed(self, item):
        col = item.column()
        if col not in EDITABLE_COLS:
            return
        row_idx = item.row()
        r = self.table.item(row_idx, 0).data(Qt.UserRole)
        new_value = item.text()

        target_rows = [rr for ridx, rr in self._selected_rows() if ridx != row_idx] if \
            row_idx in [ridx for ridx, _ in self._selected_rows()] else []
        target_rows.append(r)

        field_name = {COL_KEYWORD: t("history.field.keyword"), COL_NAME: t("history.field.name"),
                      COL_NOTE: t("history.field.note")}[col]
        before, after = [], []
        self.table.blockSignals(True)
        try:
            for rr in target_rows:
                before.append(self._snapshot(rr))
                if col == COL_KEYWORD:
                    rr["scope_obj"].UpdateMarkerCustomData(rr["frame_id"], new_value)
                    rr["keyword"] = new_value
                    log.debug("MarkerClipManager.py", f"Marker modificato: {rr['frame_id']}", {"keyword": new_value})
                elif col == COL_NAME:
                    replace_marker(rr, rr["scope_obj"], rr["frame_id"], name=new_value)
                    log.debug("MarkerClipManager.py", f"Marker modificato: {rr['frame_id']}", {"name": new_value})
                elif col == COL_NOTE:
                    replace_marker(rr, rr["scope_obj"], rr["frame_id"], note=new_value)
                    log.debug("MarkerClipManager.py", f"Marker modificato: {rr['frame_id']}", {"note": new_value})
                after.append(self._snapshot(rr))
            self._push_history(t("history.edit_field", field=field_name, n=len(target_rows)), before, after)
        except Exception as e:
            log.error("MarkerClipManager.py", "Impossibile modificare marker", {"error": str(e)})
        finally:
            self.table.blockSignals(False)
            self.refresh()


def main():
    load_language_setting()
    if not acquire_instance_lock():
        app = QApplication.instance() or QApplication(sys.argv)
        QMessageBox.warning(None, "MarkerClipManager", t("dlg.single_instance.message"))
        log.info("MarkerClipManager.py", "Avvio bloccato: istanza gia' in esecuzione")
        return
    app = QApplication.instance() or QApplication(sys.argv)
    win = MarkerManagerWindow()
    win.show()
    app.exec()
    log.info("MarkerClipManager.py", "Applicazione chiusa normalmente")


if __name__ == "__main__":
    main()
