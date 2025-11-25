from typing import Dict, Any
import re

class ContentAnalyzer:
    def __init__(self):
        self.name = "Content & Behavioral Analyzer"
        self.max_score = 20
        
        self.urgency_keywords = [
            "urgent", "immediately", "action required", "suspend", "terminate", 
            "expire", "critical", "warning"
        ]
        self.financial_keywords = [
            "wire transfer", "bank details", "invoice", "payment", "account number",
            "routing number", "swift code"
        ]
        self.credential_keywords = [
            "password", "verify your account", "click here to login", "confirm identity",
            "reset password"
        ]

    def analyze(self, subject: str, body: str) -> Dict[str, Any]:
        score = 0
        findings = []
        text = (subject + " " + body).lower()
        
        # Check Urgency
        urgency_count = sum(1 for kw in self.urgency_keywords if kw in text)
        if urgency_count >= 2:
            score += 10
            findings.append(f"High urgency language detected ({urgency_count} keywords)")
            
        # Check Financial
        financial_count = sum(1 for kw in self.financial_keywords if kw in text)
        if financial_count >= 1:
            score += 10
            findings.append("Financial transaction request detected")
            
        # Check Credentials
        cred_count = sum(1 for kw in self.credential_keywords if kw in text)
        if cred_count >= 1:
            score += 15
            findings.append("Credential/Login request detected")

        return {
            "module": self.name,
            "score": min(score, self.max_score),
            "findings": findings
        }
