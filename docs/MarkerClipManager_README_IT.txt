MarkerClipManager — Gestione Marcatori Timeline e Clip per DaVinci Resolve
==========================================================================
Author: Tommaso Feraboli — Film Editor
Version: 1.4.6
MIT License — see the script header

COSA FA
-------
Una singola finestra per visualizzare e gestire tutti i marcatori in una timeline Resolve:
sia i marcatori righello (a livello di timeline) che i marcatori posizionati su clip individuali,
su ogni traccia video e audio.

Per ogni marcatore mostra: grafica marcatore (stessa forma nativa di Resolve),
traccia, TC inizio, TC fine, durata, colore, nome, parola chiave, nota.

FUNZIONI
--------
- Seleziona uno o più marcatori e cambia colore, cambia traccia (incluso
  verso/da il righello "TIMELINE"), elimina
- Modifica Nome, Parola chiave e Nota direttamente in tabella (doppio clic),
  anche su più marcatori selezionati insieme
- Il tasto Canc fa lo stesso del pulsante Elimina, con una conferma che puoi
  disattivare
- Annulla e ripeti con Cmd+Z / Ctrl+Z, più un pannello History: doppio clic su
  un passaggio precedente per tornarci direttamente. Copre solo la sessione in
  corso e si azzera quando chiudi lo script
- Filtra per colore, traccia, autore/nome, parola chiave
- Esporta/importa marcatori come CSV
- Fai clic su una riga: la testina di riproduzione salta su quel marcatore
- Interfaccia disponibile in 12 lingue: parte nella lingua del sistema se c'è
  corrispondenza, altrimenti in inglese, e la cambi dal menu in alto nella
  finestra (ha effetto al riavvio dello script)

REQUISITI
---------
- DaVinci Resolve 19/20 (macOS)
- Python 3 installato nel sistema
- PySide6 (installato automaticamente dallo script di setup sottostante — nessun
  passaggio manuale necessario)

INSTALLAZIONE (una sola volta)
------------------------------
1. Scarica l'installer per il tuo sistema
2. macOS: CLIC DESTRO sul file .command e scegli "Apri" — non doppio clic, che
   macOS blocca perché il file non è firmato con un certificato Apple
   Windows: doppio clic sul file .cmd; se SmartScreen avvisa, scegli
   "Ulteriori informazioni" e poi "Esegui comunque"
3. L'installer copia i file e poi prepara l'ambiente Python che serve allo
   script (questa parte richiede una connessione a internet e impiega circa un
   minuto)
4. Se quella seconda parte non riesce — manca la connessione, o manca Python —
   i file restano installati correttamente: apri la cartella installata e
   lancia "MarkerClipManager_Setup.command" (macOS) o
   "MarkerClipManager_Setup_Windows.cmd" (Windows) quando puoi
5. Fatto. Gli aggiornamenti si installano allo stesso modo, sopra la versione
   precedente, e le tue impostazioni restano intatte

UTILIZZO
--------
In DaVinci Resolve: Workspace > Scripts > Comp > MarkerClipManager > MarkerClipManager
(lo script si trova nella sottocartella "MarkerClipManager" dentro Comp, quindi appare
nel menu come un sottomenu con lo stesso nome)

LIMITAZIONI NOTE
----------------
- Il marcatore nella tabella è un'icona ricreata disegnata dallo script, non
  l'icona ufficiale di Resolve (non esposta dall'API). I colori sono i
  valori esadecimali esatti forniti dall'utente — solo la forma dell'icona
  rimane un'approssimazione
- "Parola chiave" non è un campo marcatore nativo di Resolve: viene archiviato
  in un campo marcatore interno (customData), invisibile al pannello Marcatori
  nativo di Resolve — leggibile/scrivibile solo da questo script
- Il timecode legge fps e la modalità Drop Frame/Non-Drop Frame direttamente
  dalla timeline attiva del progetto (29.97 e 59.94 DF gestiti correttamente
  con l'algoritmo SMPTE standard); su fps non standard la matematica rimane approssimativa
- L'importazione/esportazione EDL non è gestita da questo script: utilizza la
  funzione nativa di Resolve (Timeline > Markers > Export/Import)
- Lo spostamento di un marcatore su una traccia video/audio richiede che un clip
  esista già in quella posizione

SUPPORTO
--------
Segnalazioni di bug: utilizza il pulsante 🐛 nell'app (apre un'email precompilata a
tomfilmeditor.tools@gmail.com)
Se vuoi supportare lo sviluppo: pulsante ☕ nell'app, o
https://paypal.me/acoffeefortom

⚠️  Note on translations: This documentation is available in multiple languages.
These translations were generated automatically. If you find any errors or typos,
please report them to the contact listed in the SUPPORT section above.
