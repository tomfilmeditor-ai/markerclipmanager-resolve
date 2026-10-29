MarkerClipManager — Timeline & Clip Marker Manager for DaVinci Resolve
======================================================================
Author: Tommaso Feraboli — Film Editor
Version: 1.4.8
MIT License — see the script header

WHAT IT DOES
------------
A single window to view and manage all markers in a Resolve timeline: both
ruler (timeline-level) markers and markers placed on individual clips, on
every video and audio track.

For each marker it shows: marker graphic (same native shape as Resolve),
track, TC in, TC out, duration, color, name, keyword, note.

FEATURES
--------
- Select one or more markers and change color, change track (including
  to/from the "TIMELINE" ruler), delete
- Edit Name, Keyword and Note directly in the table (double-click), even
  across multiple selected markers at once
- The Delete key does the same as the Delete button, with a confirmation
  you can switch off
- Undo and redo with Cmd+Z / Ctrl+Z, plus a History panel: double-click an
  earlier step to go straight back to it. It covers the current session
  only and is cleared when you close the script
- Filter by color, track, author/name, keyword
- Export/import markers as CSV
- Click a row: the timeline playhead jumps to that marker's position
- Interface available in 12 languages: it starts in your system language
  when there is a match, otherwise in English, and you can change it from
  the menu at the top of the window (it takes effect when you restart the
  script)

REQUIREMENTS
------------
- DaVinci Resolve 19/20 (macOS)
- Python 3 installed on the system
- PySide6 (installed automatically by the setup script below — no manual
  steps needed)

INSTALLATION (one-time)
-----------------------
1. Download the installer for your system
2. macOS: RIGHT-CLICK the .command file and choose "Open" — not a
   double-click, which macOS blocks because the file is not signed with an
   Apple developer certificate
   Windows: double-click the .cmd file; if SmartScreen warns you, choose
   "More info" and then "Run anyway"
3. The installer copies the files and then prepares the Python environment
   the script needs (this part needs an internet connection and takes about
   a minute)
4. If that second part fails — no connection, or Python missing — the files
   are installed correctly anyway: open the installed folder and run
   "MarkerClipManager_Setup.command" (macOS) or
   "MarkerClipManager_Setup_Windows.cmd" (Windows) when you are ready
5. Done. Updates are installed the same way, on top of the previous version,
   and your settings are left untouched

USAGE
-----
In DaVinci Resolve: Workspace > Scripts > Comp > MarkerClipManager > MarkerClipManager
(the script lives in the "MarkerClipManager" subfolder inside Comp, so it shows up in
the menu as a submenu with the same name)

KNOWN LIMITATIONS
-----------------
- The marker in the table is a recreated icon drawn by the script, not
  Resolve's official icon (not exposed by the API). Colors are the exact
  hex values provided by the user — only the icon shape remains an
  approximation
- "Keyword" is not a native Resolve marker field: it is stored in an
  internal marker field (customData), invisible to Resolve's native
  Marker panel — readable/writable only by this script
- Timecode reads fps and Drop Frame/Non-Drop Frame mode directly from the
  project's active timeline (29.97 and 59.94 DF handled correctly with the
  standard SMPTE algorithm); on non-standard fps the math stays approximate
- EDL import/export is not handled by this script: use Resolve's native
  feature (Timeline > Markers > Export/Import)
- Moving a marker to a video/audio track requires a clip to already exist
  at that position

SUPPORT
-------
Bug reports: use the 🐛 button in the app (opens a pre-filled email to
tomfilmeditor.tools@gmail.com)
If you'd like to support development: ☕ button in the app, or
https://paypal.me/acoffeefortom

⚠️  Note on translations: This documentation is available in multiple languages.
These translations were generated automatically. If you find any errors or typos,
please report them to the contact listed in the SUPPORT section above.
