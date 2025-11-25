import sqlite3
from typing import Dict, Any
import os
from datetime import datetime

class SenderAnalyzer:
    def __init__(self):
        self.name = "Sender Behavior Analyzer"
        self.max_score = 10 # Lower weight for MVP as we build history
        self.db_path = "vams.db"
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS senders
                     (email TEXT PRIMARY KEY, first_seen TEXT, last_seen TEXT, count INTEGER)''')
        conn.commit()
        conn.close()

    def analyze(self, sender_email: str) -> Dict[str, Any]:
        score = 0
        findings = []
        
        if not sender_email:
            return {"module": self.name, "score": 0, "findings": []}

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT * FROM senders WHERE email=?", (sender_email,))
        row = c.fetchone()
        
        now = datetime.now().isoformat()
        
        if row is None:
            # First time sender
            score += 5
            findings.append(f"First-time sender detected: {sender_email}")
            
            # Add to DB
            c.execute("INSERT INTO senders VALUES (?, ?, ?, ?)", (sender_email, now, now, 1))
        else:
            # Update history
            count = row[3] + 1
            c.execute("UPDATE senders SET last_seen=?, count=? WHERE email=?", (now, count, sender_email))
            
            # If sender is very new (e.g. seen < 24 hours ago) and sending again? 
            # For MVP, we just track that we know them.
            # In future: Check if "External" sender is using "Executive" name (needs LDAP integration)
            pass
            
        conn.commit()
        conn.close()

        return {
            "module": self.name,
            "score": min(score, self.max_score),
            "findings": findings
        }
