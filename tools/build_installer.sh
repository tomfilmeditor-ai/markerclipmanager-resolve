#!/bin/bash
# ============================================================
# build_installer.sh — Genera gli installer MarkerClipManager
# Produce due file autoscompattanti (macOS .command + Windows .cmd) a
# partire dai file reali installati in DaVinci Resolve: un tar.gz
# codificato in base64 incorporato dentro uno script, più le istruzioni
# bilingui EN/IT generate da INSTALL.txt.template.
#
# Questo è l'UNICO generatore ufficiale del progetto. Il ramo Windows è
# stato integrato qui il 22 settembre 2026 dalla cartella INSTALLER/
# (contributo di un'altra conversazione), che è poi stata rimossa.
#
# Adattato da RepertoireDB/ARCHIVE/INSTALLER_RepertoireDB/build_installer.sh
# Differenze rispetto a quello:
#   - una sola cartella di destinazione (tutto Python, niente Modules/Lua)
#   - nessun dato utente dentro la cartella dello script (lock, preferenza
#     lingua e log vivono in ~/Library/..., fuori dal raggio dell'installer)
#   - passo opzionale per l'ambiente Python (PySide6), che qui serve
#
# Uso:
#   ./build_installer.sh                  → versione letta da MarkerClipManager.py
#   ./build_installer.sh --version 1.5.0  → forza un numero di versione
#
# Autore: Tommaso Feraboli — Film Editor
# ============================================================

set -euo pipefail

SRC="$HOME/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Comp/MarkerClipManager"
OUT_DIR="$(cd "$(dirname "$0")" && pwd)"

VERSION=""
while [ $# -gt 0 ]; do
    case "$1" in
        --version)  VERSION="$2"; shift 2 ;;
        *) echo "Opzione sconosciuta: $1"; exit 1 ;;
    esac
done

[ -d "$SRC" ] || { echo "ERRORE: cartella sorgente non trovata:"; echo "  $SRC"; exit 1; }

# ── Versione: letta da MarkerClipManager.py se non forzata ──────────────
if [ -z "$VERSION" ]; then
    VERSION=$(grep -m1 '^VERSION' "$SRC/MarkerClipManager.py" | sed 's/.*"\(.*\)".*/\1/')
fi
[ -n "$VERSION" ] || { echo "ERRORE: versione non rilevata"; exit 1; }

echo "== Generazione installer MarkerClipManager v$VERSION =="
echo ""

# ── Coerenza versioni: script, CHANGELOG, 12 README ─────────────────────
# Gate volutamente rigido: se qualcosa non torna ci si ferma PRIMA di
# produrre un pacchetto che dichiara una versione e ne contiene un'altra.
CHANGELOG_V=$(grep -m1 -E '^## \[' "$SRC/CHANGELOG.md" | sed 's/.*\[\(.*\)\].*/\1/')
if [ "$CHANGELOG_V" != "$VERSION" ]; then
    echo "ERRORE: CHANGELOG.md ha come prima voce v$CHANGELOG_V, atteso v$VERSION."
    echo "        Aggiungi la voce di questa versione prima di generare il pacchetto."
    exit 1
fi

BAD=0
for f in "$SRC"/MarkerClipManager_README_*.txt; do
    v=$(grep -m1 '^Version:' "$f" | awk '{print $2}')
    if [ "$v" != "$VERSION" ]; then
        echo "ERRORE: $(basename "$f") dichiara v$v, atteso v$VERSION."
        BAD=1
    fi
done
if [ "$BAD" -ne 0 ]; then
    echo "        Rigenera i README con generate_readmes.py (prende la versione"
    echo "        direttamente da MarkerClipManager.py) e riprova."
    exit 1
fi
echo "Versioni allineate (script + CHANGELOG + 12 README): OK"

# ── Staging ─────────────────────────────────────────────────────────────
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
mkdir -p "$STAGE/payload/MarkerClipManager/strings"

# Codice eseguibile + moduli di cui lo script ha bisogno per partire.
# LICENSE.md e' citato nell'intestazione di MarkerClipManager.py ("vedi
# LICENSE.md"): se non viaggia col pacchetto, quel rimando punta al nulla.
for f in MarkerClipManager.py BugReportDialog.py log_manager.py \
         MarkerClipManager_Setup.command MarkerClipManager_Setup_Windows.cmd \
         CHANGELOG.md LICENSE.md; do
    [ -f "$SRC/$f" ] || { echo "ERRORE: manca $f nella cartella sorgente"; exit 1; }
    cp "$SRC/$f" "$STAGE/payload/MarkerClipManager/"
done

# Documentazione tradotta (12 lingue)
cp "$SRC"/MarkerClipManager_README_*.txt "$STAGE/payload/MarkerClipManager/"

# Stringhe dell'interfaccia (12 lingue) — senza queste l'interfaccia
# ricade tutta sull'inglese
cp "$SRC"/strings/*.json "$STAGE/payload/MarkerClipManager/strings/"

# Conteggi attesi: se una lingua manca me ne accorgo qui, non dall'utente
N_README=$(ls "$STAGE/payload/MarkerClipManager"/MarkerClipManager_README_*.txt | wc -l | tr -d ' ')
N_STRINGS=$(ls "$STAGE/payload/MarkerClipManager/strings"/*.json | wc -l | tr -d ' ')
if [ "$N_README" -ne 12 ] || [ "$N_STRINGS" -ne 12 ]; then
    echo "ERRORE: attese 12 lingue, trovati $N_README README e $N_STRINGS file di stringhe."
    exit 1
fi

chmod +x "$STAGE/payload/MarkerClipManager/MarkerClipManager_Setup.command"

# Roba che NON deve uscire: spazzatura di sistema, cache compilate Python,
# e la cartella OLDV/ (una copia vecchia tenuta da Tommaso per comodita',
# non fa parte del prodotto).
find "$STAGE/payload" -name '.DS_Store' -delete
find "$STAGE/payload" -name '__pycache__' -type d -prune -exec rm -rf {} +
rm -rf "$STAGE/payload/MarkerClipManager/OLDV"

echo ""
echo "File nel pacchetto:"
find "$STAGE/payload" -type f | sed "s|$STAGE/payload/|  |" | sort

# ── Archivio ────────────────────────────────────────────────────────────
TARBALL="$STAGE/payload.tar.gz"
tar -czf "$TARBALL" -C "$STAGE/payload" --exclude='.DS_Store' MarkerClipManager
B64=$(base64 < "$TARBALL" | tr -d '\n')

cp "$TARBALL" "$OUT_DIR/MarkerClipManager_${VERSION}.tar.gz"

# ── Installer macOS ─────────────────────────────────────────────────────
MAC_OUT="$OUT_DIR/MarkerClipManager_${VERSION}_Install_macOS.command"
{
cat <<'MACHEAD'
#!/bin/bash
# MarkerClipManager — Installer macOS
set -e

DEST="$HOME/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Comp/MarkerClipManager"
VENV_DIR="$HOME/.venvs/resolve_pyside6"

echo ""
echo "== Installazione MarkerClipManager =="
echo ""

mkdir -p "$DEST"

TEMP_DIR=$(mktemp -d)
TEMP_TAR="$TEMP_DIR/payload.tar.gz"
MACHEAD

printf "echo '%s' | base64 -D > \"\$TEMP_TAR\"\n" "$B64"

cat <<'MACFOOT'
tar -xzf "$TEMP_TAR" -C "$TEMP_DIR"

# 1) Script, moduli, documentazione e stringhe -> una sola cartella.
#    Si sovrascrivono solo i file del pacchetto: eventuali file tuoi
#    presenti nella stessa cartella restano dove sono.
cp -R "$TEMP_DIR/MarkerClipManager/." "$DEST/"
chmod +x "$DEST/MarkerClipManager_Setup.command" 2>/dev/null || true
rm -rf "$TEMP_DIR"

echo "Script installato in:"
echo "  $DEST"
echo ""

# 2) Ambiente Python (PySide6).
#    E' l'unico passo che richiede internet e che puo' fallire per motivi
#    fuori dal pacchetto (Python 3 assente, rete, proxy aziendale): se non
#    riesce NON si annulla l'installazione, si spiega come completarla dopo.
ENV_OK="no"
if [ -n "${MCM_SKIP_ENV:-}" ]; then
    echo "Ambiente Python: passo saltato (MCM_SKIP_ENV attivo)."
elif [ -x "$VENV_DIR/bin/python3" ] && "$VENV_DIR/bin/python3" -c "import PySide6" >/dev/null 2>&1; then
    echo "Ambiente Python gia' pronto: nessuna installazione necessaria."
    ENV_OK="yes"
elif ! command -v python3 >/dev/null 2>&1; then
    echo "ATTENZIONE: python3 non risulta installato su questo Mac."
    echo "            Installalo da https://www.python.org/downloads/ e poi"
    echo "            fai doppio clic su MarkerClipManager_Setup.command"
    echo "            nella cartella qui sopra."
else
    echo "Preparazione ambiente Python (richiede internet, circa un minuto)..."
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv "$VENV_DIR" || true
    fi
    if [ -x "$VENV_DIR/bin/pip" ] && "$VENV_DIR/bin/pip" install --upgrade pip PySide6; then
        ENV_OK="yes"
        echo "Ambiente Python pronto."
    else
        echo ""
        echo "ATTENZIONE: non e' stato possibile preparare l'ambiente Python."
        echo "            I file sono installati correttamente: quando hai"
        echo "            connessione, fai doppio clic su"
        echo "            MarkerClipManager_Setup.command nella cartella qui sopra."
    fi
fi

echo ""
echo "Fatto. Avvia da DaVinci Resolve:"
echo "  Workspace > Scripts > Comp > MarkerClipManager > MarkerClipManager"
echo ""
if [ "$ENV_OK" != "yes" ]; then
    echo "Ricorda: manca ancora l'ambiente Python (vedi avviso sopra)."
    echo ""
fi
echo "Nota: le tue preferenze (lingua) e i log non sono stati toccati."
echo ""
read -p "Premi INVIO per chiudere..." _ || true
MACFOOT
} > "$MAC_OUT"
chmod +x "$MAC_OUT"

# ── Installer Windows ───────────────────────────────────────────────────
# Ramo nato nella conversazione "RepertoireDB — Manutenzione Script" e
# integrato qui il 22 settembre 2026 (vedi STATO.md). Strategia diversa da
# macOS e obbligata: su Windows il bootstrap del virtualenv dentro
# MarkerClipManager.py non funziona (cerca .../bin/python3, percorso POSIX),
# quindi PySide6 va installato direttamente nel Python dell'utente, cosi'
# l'import riesce e quel ramo non viene mai eseguito.
# NOTA ONESTA': mai provato su una macchina Windows reale.
WIN_OUT="$OUT_DIR/MarkerClipManager_${VERSION}_Install_Windows.cmd"
{
cat <<'WINHEAD'
@echo off
REM MarkerClipManager - Installer Windows (file + ambiente Python)
setlocal enabledelayedexpansion

REM Resolve usa due possibili percorsi per gli script utente, a seconda della
REM versione e di come e' stato installato. Si usa quello gia' presente sul
REM computer; se non ce n'e' nessuno, si crea il primo.
set "BASE_A=%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Comp"
set "BASE_B=%APPDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Comp"

if exist "!BASE_A!" (
    set "DEST=!BASE_A!\MarkerClipManager"
) else if exist "!BASE_B!" (
    set "DEST=!BASE_B!\MarkerClipManager"
) else (
    set "DEST=!BASE_A!\MarkerClipManager"
)

echo.
echo ======================================================
echo   MarkerClipManager - Installazione / Installation
echo ======================================================
echo.

if not exist "!DEST!" mkdir "!DEST!"
set "TMPDIR=%TEMP%\mcm_install"
if exist "!TMPDIR!" rmdir /s /q "!TMPDIR!"
mkdir "!TMPDIR!"

WINHEAD

printf 'powershell -Command "$b64='"'"'%s'"'"'; $bytes=[System.Convert]::FromBase64String($b64); [System.IO.File]::WriteAllBytes('"'"'!TMPDIR!\\payload.tar.gz'"'"',$bytes)"\n' "$B64"

cat <<'WINFOOT'
powershell -Command "cd '!TMPDIR!'; tar -xzf payload.tar.gz"
xcopy /E /I /Y /Q "!TMPDIR!\MarkerClipManager" "!DEST!" >nul
rmdir /s /q "!TMPDIR!"

echo [1/2] File installati in:
echo       !DEST!
echo.

REM ---- 2. Ambiente Python (PySide6) ----
REM Stessa filosofia del ramo macOS: se questo passo fallisce NON si annulla
REM l'installazione, i file restano installati e si spiega come completare.
echo [2/2] Preparazione ambiente Python (PySide6).
echo       Richiede connessione a internet e qualche minuto.
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo   ATTENZIONE: python non trovato su questo computer.
    echo   I file dello script SONO stati installati correttamente,
    echo   ma manca Python per farli funzionare.
    echo.
    echo   Installa Python 3 da https://www.python.org/downloads/
    echo   spuntando "Add Python to PATH" durante l'installazione,
    echo   poi rilancia questo installer.
    echo.
    pause
    exit /b 0
)

for /f "delims=" %%v in ('python --version 2^>^&1') do echo   %%v

echo   Installazione di PySide6 in corso...
python -m pip install --user --quiet --upgrade pip PySide6
if errorlevel 1 (
    echo.
    echo   ATTENZIONE: installazione di PySide6 non riuscita
    echo   ^(probabile assenza di connessione a internet^).
    echo.
    echo   I file dello script SONO installati correttamente.
    echo   Quando torni online, apri nella cartella installata:
    echo     MarkerClipManager_Setup_Windows.cmd
    echo.
    pause
    exit /b 0
)

echo   PySide6 pronto.
echo.
echo ======================================================
echo   Installazione completata.
echo.
echo   Avvia da DaVinci Resolve:
echo     Workspace ^> Scripts ^> Comp ^> MarkerClipManager
echo ======================================================
echo.
pause
WINFOOT
} > "$WIN_OUT"

# ── Istruzioni per chi riceve il pacchetto ──────────────────────────────
# Generate dal modello INSTALL.txt.template (bilingue EN/IT, entrambi i
# sistemi): il modello e' un file vero, diffabile, e la versione ci viene
# sostituita dentro qui — non si scrive a mano in tre punti diversi.
TEMPLATE="$OUT_DIR/INSTALL.txt.template"
INSTR="$OUT_DIR/INSTALL.txt"
if [ -f "$TEMPLATE" ]; then
    # L'indirizzo per le segnalazioni viene da BUG_EMAIL in MarkerClipManager.py:
    # un posto solo. Era sfuggito al cambio di indirizzo perche' questo file e'
    # scritto a mano e non generato da una traduzione.
    BUG_EMAIL=$(grep -m1 '^BUG_EMAIL' "$SRC/MarkerClipManager.py" | sed 's/.*"\(.*\)".*/\1/')
    [ -n "$BUG_EMAIL" ] || { echo "ERRORE: BUG_EMAIL non trovata in MarkerClipManager.py"; exit 1; }
    sed -e "s/__VERSION__/$VERSION/g" -e "s/__BUG_EMAIL__/$BUG_EMAIL/g" "$TEMPLATE" > "$INSTR"
    REMAINING=$(grep -c '__VERSION__\|__BUG_EMAIL__' "$INSTR" || true)
    [ "$REMAINING" -eq 0 ] || { echo "ERRORE: segnaposto rimasti in $INSTR"; exit 1; }
else
    echo "ERRORE: manca $TEMPLATE"; exit 1
fi


echo ""
echo "Generati:"
ls -lh "$MAC_OUT" "$WIN_OUT" "$INSTR" "$OUT_DIR/MarkerClipManager_${VERSION}.tar.gz" | awk '{print "  " $9 "  (" $5 ")"}'
echo ""
echo "Nota: il ramo Windows non e' mai stato provato su una macchina Windows"
echo "      reale — testato solo il ramo macOS. Vedi STATO.md."
echo ""
