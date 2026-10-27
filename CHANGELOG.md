# MarkerClipManager — Changelog

Questo file non esisteva prima del 9 agosto 2026: creato in seguito alla
riorganizzazione multi-progetto (vedi `CLAUDE_WORKS/MarkerClipManager/STATO.md`),
che ha reso obbligatorio tenerne uno. Le versioni precedenti a 1.2.14 non hanno
voci dettagliate qui perché non tracciate al momento — vedi comunque gli
snapshot in `CLAUDE_WORKS/MarkerClipManager/ARCHIVE/` (v1.0, v1.1, v1.2.13,
v1.2.14) come riferimento.

## [1.4.7] — 2026-10-27

### Cambiato
- **`LICENSE.md` ora contiene il testo MIT verbatim.** GitHub classificava la
  licenza come "Other" invece di MIT: la causa non erano le sezioni in fondo al
  file, ma un paragrafo esplicativo inserito **dentro** il corpo della licenza
  ("This means: ..."), che porta il riconoscimento automatico sotto soglia.
  La spiegazione in parole semplici non e' andata persa: e' nei README, sotto
  i crediti. La nota sulle traduzioni automatiche e il link per le donazioni
  erano gia' presenti nei 12 README tradotti, quindi toglierli dalla licenza
  non toglie niente a chi scarica.

## [1.4.6] — 2026-10-26

### Cambiato
- **Indirizzo per le segnalazioni**: si passa dall'indirizzo personale
  dell'autore a una casella dedicata agli strumenti. Il pulsante 🐛 e la
  documentazione in tutte e 12 le lingue puntano ora li'. Il link PayPal non
  e' toccato: non contiene nessun indirizzo.
- `extract_translations.py` riscrive l'indirizzo nei file di stringhe
  prendendolo da `BUG_EMAIL`. Serviva: l'indirizzo era testo congelato dentro
  le traduzioni, e i file di stringhe vengono distribuiti — cambiarlo solo nel
  codice avrebbe lasciato quello vecchio dentro dodici file.

### Aggiornato — documentazione in 12 lingue
- **Istruzioni di installazione riscritte.** Descrivevano la vecchia procedura
  manuale (doppio clic sullo script di setup, che pero' prepara solo
  l'ambiente Python e non copia nulla): chi le seguiva dopo aver scaricato il
  pacchetto si ritrovava l'ambiente e nessuno script. Ora descrivono
  l'installer, il clic destro > Apri su macOS, l'avviso SmartScreen su
  Windows, e cosa fare se la preparazione dell'ambiente non riesce.
- **Elenco delle funzioni aggiornato**: era fermo alla 1.2.x. Ora comprende
  Undo/Redo e il pannello History, il tasto Delete con la conferma
  disattivabile, e il fatto che l'interfaccia esista in 12 lingue con
  selettore.

### Corretto
- **Documenti di traduzione malformati dall'agosto 2026**: il blocco con
  l'avviso sulle traduzioni automatiche era stato inserito *dentro* il blocco
  precedente, lasciandolo non chiuso. I file risultavano di 70 blocchi invece
  di 71 e l'avviso non sarebbe sopravvissuto a una rigenerazione. Ricostruiti
  tutti e 12.

## [1.4.5] — 2026-10-14

### Corretto
- **Lo script non si apriva piu' se Resolve non e' installato in
  `/Applications/DaVinci Resolve/`.** Il modulo di Blackmagic cerca la libreria
  `fusionscript` in un percorso fisso: chi tiene piu' versioni installate le
  rinomina per forza (`DaVinci Resolve 20`, `DaVinci Resolve 19`...), quel
  percorso smette di esistere e nessuno script parte. L'errore parlava di un
  modulo `fusionscript` mancante, senza dire cosa fare.
  Ora lo script cerca la libreria da solo e compila la variabile
  `RESOLVE_SCRIPT_LIB` che Blackmagic prevede proprio per questo, nell'ordine:
  quella gia' impostata dall'utente, poi quella del **Resolve effettivamente
  aperto** (se ne hai tre installati e' quello giusto), poi il percorso standard,
  poi le altre installazioni dalla versione piu' alta in giu'.
  Se davvero non la trova, il messaggio ora spiega il problema e la soluzione
  invece di mostrare solo l'errore di import.
  Verificato dal vivo: prima non partiva, ora si apre senza impostare nulla.

## [1.4.4] — 2026-09-22

### Aggiunto
- **Installer Windows** (`MarkerClipManager_X.Y.Z_Install_Windows.cmd`) e
  `MarkerClipManager_Setup_Windows.cmd` nel pacchetto. Il ramo era nato in
  un'altra conversazione, in una seconda cartella installer: è stato
  integrato nel generatore ufficiale (l'unico con i controlli di coerenza
  versioni) e la cartella doppia è stata rimossa.
  Su Windows PySide6 va installato nel Python dell'utente
  (`pip install --user`), non in un virtualenv: il bootstrap dentro
  `MarkerClipManager.py` cerca `.../bin/python3`, percorso che su Windows non
  esiste, quindi si fa in modo che `import PySide6` riesca subito e quel ramo
  non venga mai eseguito. **Mai provato su una macchina Windows reale.**
- **Istruzioni bilingui EN/IT** (`INSTALL.txt`) per entrambi i sistemi,
  generate da un modello versionato — prima erano solo italiane e solo macOS,
  incoerente con un'app tradotta in 12 lingue.
- **`LICENSE.md`**: l'intestazione di `MarkerClipManager.py` rimandava a
  "vedi LICENSE.md" da sempre, ma il file non esisteva — chi riceveva il
  pacchetto trovava un rimando a vuoto. Stessa forma del `LICENSE.md` di
  RepertoireDB (MIT, con la clausola sull'obbligo di mantenere l'attribuzione
  spiegata anche in parole semplici), più una nota sulle traduzioni:
  sono generate automaticamente e verificate nella struttura, non nella
  qualità linguistica di ogni lingua. Ora viaggia dentro il pacchetto.

## [1.4.3] — 2026-09-21

### Aggiunto
- **Installer di distribuzione per macOS**: un unico file autoscompattante
  (`MarkerClipManager_X.Y.Z_Install_macOS.command`) che copia script, moduli,
  documentazione in 12 lingue e file di stringhe nella cartella di Resolve, e
  poi prepara da solo l'ambiente Python (PySide6). Prima bisognava copiare a
  mano 5 elementi e lanciare separatamente lo script di setup.
  Generato da `ARCHIVE/INSTALLER_MarkerClipManager/build_installer.sh`, che
  legge i file veri installati in Resolve — l'installer non si scrive né si
  modifica a mano. Accanto viene prodotto anche
  `ISTRUZIONI_INSTALLAZIONE.txt` per chi riceve il pacchetto.
- Il generatore si ferma se le versioni dichiarate da `MarkerClipManager.py`,
  `CHANGELOG.md` e dai 12 README non coincidono, o se le lingue non sono 12.

### Corretto
- **`MarkerClipManager_Setup.command` usciva con codice di errore** anche
  quando l'installazione riusciva: `set -e` insieme al `read` finale fa
  fallire lo script quando gira senza terminale interattivo. Stesso difetto
  già corretto a suo tempo sull'installer di RepertoireDB.
- **La riga `Version:` dei 12 README tornava indietro a ogni rigenerazione**:
  il numero era testo congelato dentro le traduzioni, quindi rigenerarli (per
  esempio per aggiungere il disclaimer in 1.4.2) riportava i README a 1.3.2
  mentre il codice era 1.4.2. Ora `generate_readmes.py` scrive la versione
  leggendola da `MarkerClipManager.py`: non può più sfasarsi.

## [1.4.2] — 2026-08-09

### Aggiunto
- **Disclaimer su traduzione automatica nei README**: tutti e 12 i README
  (una per lingua) ora terminano con un avviso che la traduzione è stata
  generata automaticamente, con invito a segnalare errori/refusi alla contact
  listed in SUPPORT section. Omessa inizialmente perché il documento sorgente
  di traduzione era stato completato prima di introdurre questo requisito nel
  progetto di traduzione stesso.

## [1.4.1] — 2026-08-09

### Corretto
- **`BugReportDialog.py` non aveva mai avuto consapevolezza della lingua
  dell'interfaccia**: la mail di segnalazione bug era sempre in italiano,
  qualunque fosse la lingua attiva dello script (bug preesistente
  all'introduzione del multilingua in v1.4.0, mai notato perché il modulo è
  stato scritto da un'altra sessione prima che esistesse una lingua diversa
  dall'italiano). Ora: se la lingua attiva è italiano, la mail resta in
  italiano (comportamento invariato); per qualunque altra delle 12 lingue
  supportate (inglese incluso), la mail passa in inglese, con la prima riga
  del corpo che chiede esplicitamente di scrivere in inglese — Tom legge
  italiano e inglese, non tutte le lingue dell'interfaccia. Oggetto, privacy
  notice e struttura del corpo tradotti in inglese allo stesso modo; email
  destinatario e link PayPal invariati in entrambe le versioni.

## [1.4.0] — 2026-08-09

### Aggiunto — Interfaccia multilingua (12 lingue)
- **Sistema di stringhe**: le ~54 stringhe dell'interfaccia non sono più
  scritte a mano nel codice, ma lette da `strings/<CODICE>.json` (uno per
  lingua) tramite una funzione `t("chiave", **variabili)` con fallback
  automatico all'inglese se una chiave manca in una lingua
- **12 lingue supportate**: EN, IT, FR, DE, ES, PT, RU, JA, KO, ZH, VI, TH —
  tradotte letterariamente (non a macchina) a partire da
  `CLAUDE_WORKS/MarkerClipManager/MarkerClipManager_TRANSLATION_SOURCE.md`,
  verificate strutturalmente (70/70 blocchi, nessun placeholder perso, nessuna
  voce vuota) prima dell'integrazione
- **Rilevamento lingua al primo avvio**: legge la lingua di sistema (macOS
  `AppleLocale`, con fallback al modulo `locale` di Python), la mappa su una
  delle 12 supportate o ricade sull'inglese; salvata in
  `~/Library/Application Support/RepertoireDB/marker_clip_manager_settings.json`
- **Selettore lingua in-app** (menu a tendina nell'header, mostra i nomi
  nativi: Italiano, Français, 日本語...): cambia la preferenza salvata; il
  cambio richiede un riavvio dello script (le label statiche non si
  ridisegnano a caldo — scelta deliberata per non dover tracciare un
  riferimento a ogni singolo widget di testo)
- **README in tutte e 12 le lingue**: `MarkerClipManager_README_<CODICE>.txt`,
  generati automaticamente dalle traduzioni con sottolineature `===`/`---`
  ricalcolate sulla larghezza visiva reale del testo (i caratteri CJK contano
  doppio in un font monospace: gestito con `unicodedata.east_asian_width`).
  Il pulsante 📖 apre il README della lingua attiva, con fallback automatico
  all'inglese se quel file non esiste
- **`MarkerClipManager_Setup.command` resta solo in inglese** (deciso con
  l'utente: passaggio tecnico una tantum, non giustifica 12 varianti bash)

### Corretto durante lo sviluppo (trovato dai test, non dall'uso)
- `apply_filters()` riconosceva "nessun filtro" controllando se il testo
  iniziasse con `"All "` — funzionava solo in inglese. Corretto per usare
  l'indice del menu a tendina (posizione 0 = sempre "tutti/e", qualunque sia
  la lingua) invece del confronto testuale
- Verificato con rendering diretto (`QWidget.grab()`, non screenshot dello
  schermo) che testi più lunghi dell'inglese (tedesco, francese, russo) non
  rompono il layout: la finestra si allarga automaticamente, nessun controllo
  si sovrappone o viene tagliato

### Strumenti aggiunti (non distribuiti con l'app, restano in CLAUDE_WORKS)
- `extract_translations.py` — estrae le 12 lingue dai file di traduzione in
  `strings/*.json`, riusabile per aggiornamenti futuri delle traduzioni
- `generate_readmes.py` — rigenera i 12 README dalle stringhe estratte

## [1.3.2] — 2026-08-09

### Corretto
- Numero di versione nei README (IT ed EN) fermo a "1.0", allineato a 1.3.2
- `MarkerClipManager_Setup.command` tradotto da italiano a inglese (era
  rimasto l'unico file ancora interamente in italiano) — stessa logica delle
  correzioni di coerenza già fatte in v1.3.1

### Aggiunto
- `CLAUDE_WORKS/MarkerClipManager/MarkerClipManager_TRANSLATION_SOURCE.md` —
  testo sorgente completo (interfaccia + README + script di setup, 70 stringhe
  uniche) pronto per traduzione letteraria in altre lingue, con formato a
  blocchi pensato per essere ricomposto in automatico una volta tradotto

## [1.3.1] — 2026-08-09

### Corretto
- 2 stringhe rimaste in italiano nonostante l'interfaccia sia in inglese dal
  22 luglio 2026 (dialogo History, avviso istanza già aperta) — trovate
  preparando `CLAUDE_WORKS/MarkerClipManager/I18N-TRANSLATIONS.md`, l'inventario
  completo di tutte le stringhe dell'interfaccia e dei README in vista di una
  futura versione multilingue

## [1.3.0] — 2026-08-09

### Aggiunto
- **Tasto Delete/Backspace della tastiera** — agisce come il pulsante Delete della
  UI (stesso comando, stessa conferma), scoped alla tabella per non interferire
  con il campo filtro Keyword o l'editing inline di una cella
- **Toggle "Confirm before delete"** in toolbar — se disattivato, Delete diventa
  diretto senza dialogo di conferma
- **Undo/Redo** — Cmd+Z / Shift+Cmd+Z (mappatura nativa Qt, funziona anche
  Ctrl+Z/Ctrl+Shift+Z su Windows), pulsanti Undo/Redo in toolbar, copre: cambio
  colore, cambio traccia, cancellazione, editing inline (Name/Keyword/Note),
  import CSV
- **Pannello History** (pulsante "History" in toolbar) — lista di tutte le
  azioni della sessione corrente, doppio clic su una voce per saltare
  direttamente a quel punto (stile "History panel" di Photoshop, non due stack
  separati undo/redo ma un'unica lista con puntatore di posizione)
- **Blocco istanze multiple** — lock file con PID; se MarkerClipManager è già
  aperto, un nuovo avvio mostra un avviso invece di aprire una seconda finestra.
  Lock riconosciuto come "stale" e ignorato se il processo precedente non esiste
  più (crash, kill -9) — nessun falso blocco permanente

### Bug corretto durante lo sviluppo
- `jump_to_history()` andava in loop infinito se il target superava la history
  disponibile (es. doppio clic rapido, o indice fuori range) — `redo()` non
  incrementa il puntatore oltre la fine della history, quindi il ciclo `while`
  non terminava mai. Corretto con un clamp del target su `[0, len(history)]`.
  Trovato da un test automatico dedicato prima di qualunque uso reale.

## [1.2.14] — 2026-08-09

### Aggiunto
- **Bottone 📖 Guida** nell'header, terzo bottone dello standard
  `shared-knowledge/PYTHON-LUA-PATTERNS.md` (📖/☕/🐛) — mancava, solo 🐛 e ☕
  erano presenti. Apre `MarkerClipManager_README_IT.txt` (stesso stile
  gradiente/dimensione 44×44 dei due bottoni esistenti: oro `#8B7B1A→#5A4E0A`)

### Nota
- I bottoni 🐛 (bug via `BugReportDialog` + PayPal) e ☕ (solo PayPal) erano già
  conformi allo standard shared-knowledge da una revisione precedente (6 agosto
  2026, insieme all'introduzione di `log_manager.py` e `BugReportDialog.py`) —
  non modificati in questa release.

## [1.2.13] — 2026-08-06 (ricostruito da ARCHIVE, non documentato a suo tempo)

### Aggiunto
- `log_manager.py` — logging centralizzato su file (`~/Library/Logs/RepertoireDB/marker_clip_manager.log`)
- `BugReportDialog.py` — dialog di segnalazione bug con privacy notice esplicita
  prima dell'invio, template email con info di sistema, integrazione AppleScript
  su macOS per Mail.app
- Bottoni header ridimensionati a 44×44 con stylesheet a gradiente (prima 34×34
  senza stile)
