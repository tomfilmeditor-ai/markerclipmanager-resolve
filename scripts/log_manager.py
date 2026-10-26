"""
LogManager — Sistema centralizzato di logging per script Python
Compatibile con: MarkerClipManager.py
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path


class LogManager:
    """Gestore centralizzato di log per script Python in DaVinci Resolve"""
    
    # Configurazione
    LOG_DIR = os.path.expanduser("~/Library/Logs/RepertoireDB")
    LOG_FILE = os.path.join(LOG_DIR, "marker_clip_manager.log")
    MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
    
    # Livelli di log
    LEVELS = {
        'DEBUG': 0,
        'INFO': 1,
        'WARNING': 2,
        'ERROR': 3,
        'CRITICAL': 4
    }
    MIN_LEVEL = LEVELS['INFO']  # Cambiare a DEBUG per debug completo
    
    _instance = None
    _handler = None
    _logger = None
    
    def __new__(cls):
        """Singleton pattern — un'unica istanza per processo"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inizializza il logger (una sola volta)"""
        if self._initialized:
            return
        
        # Crea directory se non esiste
        Path(self.LOG_DIR).mkdir(parents=True, exist_ok=True)
        
        # Configura logger Python
        self._logger = logging.getLogger("MarkerClipManager")
        self._logger.setLevel(logging.DEBUG)
        
        # Handler per file (con rotazione)
        try:
            handler = logging.FileHandler(self.LOG_FILE, encoding='utf-8')
            formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
            self._handler = handler
        except Exception as e:
            print(f"[ERROR] Non posso creare log file: {e}")
        
        self._initialized = True
    
    @staticmethod
    def _serialize_data(data):
        """Serializza dati strutturati per il log"""
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            try:
                return json.dumps(data, ensure_ascii=False, default=str)
            except:
                return str(data)
        else:
            return str(data)
    
    def _log(self, level, script_name, message, data=None):
        """Funzione interna di logging"""
        if self.LEVELS.get(level, 0) < self.MIN_LEVEL:
            return
        
        # Aggiungi dati strutturati se presenti
        full_message = message
        if data:
            full_message = f"{message} | {self._serialize_data(data)}"
        
        # Log con livello appropriato
        level_lower = level.lower()
        if level_lower == 'debug':
            self._logger.debug(f"{script_name}: {full_message}")
        elif level_lower == 'info':
            self._logger.info(f"{script_name}: {full_message}")
        elif level_lower == 'warning':
            self._logger.warning(f"{script_name}: {full_message}")
        elif level_lower == 'error':
            self._logger.error(f"{script_name}: {full_message}")
        elif level_lower == 'critical':
            self._logger.critical(f"{script_name}: {full_message}")
    
    # Interfaccia pubblica
    def debug(self, script_name, message, data=None):
        """Log di debug (dettagli tecnici)"""
        self._log('DEBUG', script_name, message, data)
    
    def info(self, script_name, message, data=None):
        """Log informativo (operazioni normali)"""
        self._log('INFO', script_name, message, data)
    
    def warn(self, script_name, message, data=None):
        """Log di warning (situazione non ideale ma recuperabile)"""
        self._log('WARNING', script_name, message, data)
    
    def error(self, script_name, message, data=None):
        """Log di errore (operazione fallita)"""
        self._log('ERROR', script_name, message, data)
    
    def critical(self, script_name, message, data=None):
        """Log critico (errore gravissimo, sistema potrebbe non funzionare)"""
        self._log('CRITICAL', script_name, message, data)
    
    def read_tail(self, n=20):
        """Leggi ultime N righe del log"""
        try:
            with open(self.LOG_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return ''.join(lines[-n:])
        except:
            return ""
    
    def read_all(self):
        """Leggi tutto il log"""
        try:
            with open(self.LOG_FILE, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return ""


# Istanza globale (singleton)
log = LogManager()
