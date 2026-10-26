# MarkerClipManager

**Gestione dei marcatori per DaVinci Resolve.**
Una finestra per vedere e modificare tutti i marcatori di una timeline — quelli
sul righello e quelli attaccati ai singoli clip, su tutte le tracce video e
audio, insieme.

🇬🇧 [Read in English](README.md)

![Versione](https://img.shields.io/badge/versione-1.4.6-blue)
![Sistema](https://img.shields.io/badge/sistema-macOS%20%7C%20Windows-lightgrey)
![Resolve](https://img.shields.io/badge/DaVinci%20Resolve-19%20%7C%2020-orange)
![Interfaccia](https://img.shields.io/badge/interfaccia-12%20lingue-brightgreen)
![Licenza](https://img.shields.io/badge/licenza-MIT-green)

![MarkerClipManager — tutti i marcatori della timeline in una tabella](docs/images/main-window.png)

*Tutti i marcatori della timeline in una tabella sola — quelli del righello e
quelli dei clip insieme. Dati di esempio.*

---

## Il problema che risolve

Su un montaggio lungo i marcatori si accumulano. Note di revisione, segnalazioni
per gli effetti, attacchi musicali, promemoria — alcuni sul righello della
timeline, altri attaccati ai singoli clip, sparsi su una dozzina di tracce.

Resolve te li mostra, ma uno alla volta. Non c'è modo di vedere nella stessa
lista i marcatori dei clip e quelli del righello, non c'è modo di filtrarli, e
non c'è modo di agire su quaranta insieme. Ricolorare un giro di note di
revisione significa aprire quaranta finestre.

MarkerClipManager li mette tutti in una tabella sola: filtri, selezioni quello
che ti serve, lo cambi in un colpo.

Scritto da un montatore per i propri montaggi.

---

## Cosa fa

Tutti i marcatori della timeline in una tabella ordinabile: grafica del
marcatore, traccia, TC inizio, TC fine, durata, colore, nome, parola chiave, nota.

**Modificare, uno o quaranta alla volta**

- Colore, traccia (compreso spostare i marcatori da e verso il righello
  `TIMELINE`), eliminazione
- Nome, Parola chiave e Nota si modificano direttamente in tabella — doppio clic
  su una cella, e la modifica si applica a tutti i marcatori che hai selezionato
- Il tasto `Canc` fa lo stesso del pulsante Elimina, con una conferma che puoi
  disattivare

**Trovare**

- Filtri per colore, traccia, autore/nome, o parola chiave a testo libero
- Clic su una riga e la testina di riproduzione salta su quel marcatore

**Tornare indietro**

- `Cmd+Z` / `Ctrl+Z`, e un pannello History: doppio clic su un passaggio
  precedente e torni direttamente lì, come in un programma di fotoritocco
- Copre colore, traccia, modifiche in tabella, cancellazioni e import CSV fatti
  nella sessione. Non resta in memoria dopo che hai chiuso lo script

**Portare i marcatori dentro e fuori**

- Esportazione e importazione in CSV

**Nella tua lingua**

- L'interfaccia è tradotta in 12 lingue — inglese, italiano, francese, tedesco,
  spagnolo, portoghese, russo, giapponese, coreano, cinese, vietnamita,
  thailandese. Parte nella lingua del sistema se c'è corrispondenza, altrimenti
  in inglese, e c'è un menu per cambiarla in alto nella finestra (ha effetto al
  riavvio dello script)

---

## Installazione

Scarica l'installer per il tuo sistema dalla
[pagina Releases](../../releases), poi:

**macOS** — **clic destro** sul file `.command` e scegli **Apri**
(non doppio clic: l'installer non è firmato con un certificato Apple, e il
doppio clic viene bloccato con un messaggio su uno sviluppatore non identificato).

**Windows** — doppio clic sul file `.cmd`. Se SmartScreen avvisa, scegli
*Ulteriori informazioni* → *Esegui comunque*.

L'installer copia i file e poi prepara l'ambiente Python che serve allo script.
Se quella seconda parte non riesce — manca la connessione, manca Python — i file
restano installati correttamente, e ti dice come completare dopo.

Poi, in Resolve:

    Workspace > Scripts > Comp > MarkerClipManager > MarkerClipManager

Preferisci installare a mano? Tutto quello che sta in `scripts/` va in una
cartella sola: `Fusion/Scripts/Comp/MarkerClipManager/`, tenendoci dentro la
sottocartella `strings/`. Poi lancia `MarkerClipManager_Setup.command` (macOS) o
`MarkerClipManager_Setup_Windows.cmd` per installare PySide6.

---

## Requisiti

- **DaVinci Resolve 19 o 20**
- **Python 3**, e PySide6 — ci pensa l'installer, su macOS in un ambiente
  separato così non tocca il Python di sistema
- macOS o Windows

> **Studio o versione gratuita?** Usato tutti i giorni su Resolve Studio. Se
> funzioni sulla versione gratuita non è stato provato. L'interfaccia è fatta con
> PySide6, non con UIManager di Resolve — quindi *non* incontra il limite che
> dalla 19.1 rende gli script UIManager riservati a Studio — ma l'accesso alle
> funzioni di scripting che legge la timeline non è stato verificato sulla
> gratuita. Se la provi lì, [apri una Issue](../../issues) e racconta com'è
> andata.

---

## Limiti noti

- **Windows è pronto ma non provato.** L'installer e lo script di preparazione
  per Windows esistono e il codice c'è, ma nessuno l'ha ancora eseguito su una
  macchina Windows vera. Se lo fai, fammelo sapere
- **"Parola chiave" non è un campo nativo di Resolve.** I marcatori di Resolve
  non ce l'hanno, quindi viene salvata nel `customData` del marcatore. È
  invisibile al pannello Marcatori di Resolve — solo questo script la legge e la
  scrive
- **L'icona del marcatore è una ricostruzione**, disegnata dallo script: Resolve
  non espone la propria. I colori sono esatti, la forma è approssimata
- **L'annulla non resta in memoria** tra un avvio e l'altro, e non si accorge dei
  marcatori che modifichi direttamente in Resolve mentre lo script è aperto
- **Spostare un marcatore su una traccia video o audio** richiede che in quella
  posizione ci sia già un clip — Resolve non ammette marcatori sospesi nel vuoto.
  Verso il righello `TIMELINE` funziona sempre
- **Il timecode** legge frame rate e modalità drop-frame dalla timeline (29.97 e
  59.94 DF gestiti con l'algoritmo SMPTE standard). Su frame rate inusuali o
  variabili il risultato è approssimato
- **L'import/export EDL dei marcatori non c'è** — lo fa Resolve nativamente
  (Timeline > Markers > Export/Import). Questo script gestisce il CSV
- **Le 12 traduzioni sono generate automaticamente** e verificate nella
  struttura, non nella qualità di ogni lingua. Refusi e rese poco naturali sono
  probabili: le correzioni sono benvenute

---

## Documentazione

- [Guida utente](docs/) — la stessa guida in 12 lingue
- [CHANGELOG](CHANGELOG.md) — cosa è cambiato in ogni versione

---

## Segnalare un problema

Apri una [Issue](../../issues) — è il modo migliore, perché chi avrà lo stesso
problema trova la risposta già scritta.

Lo script ha anche un pulsante 🐛 che apre una mail precompilata con i dettagli
del sistema, e tiene un file di log che puoi allegare:

- macOS: `~/Library/Logs/RepertoireDB/repertoire_db.log`
- Windows: `%LOCALAPPDATA%\Blackmagic Design\DaVinci Resolve\Logs\RepertoireDB\`

Una nota su cosa hai davanti: questo lo scrive un montatore, non uno
sviluppatore di professione. Il codice funziona e viene usato su montaggi veri,
ma non aspettarti le convenzioni di un progetto software.

---

## Crediti

**Tommaso Feraboli** — Film Editor
Distribuito con licenza [MIT](LICENSE.md) · Copyright (c) 2024-2026

Se ti fa risparmiare tempo: [offrimi un caffè](https://paypal.me/acoffeefortom) ☕
