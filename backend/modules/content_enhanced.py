from typing import Dict, List, Tuple
import re
from collections import Counter

class EnhancedContentAnalyzer:
    """Advanced behavioral and psychological manipulation detection"""
    
    MAX_SCORE = 40  # Increased from 20
    
    def __init__(self):
        self.urgency_keywords = [
            "urgent", "immediately", "action required", "suspend", "terminate", 
            "expire", "critical", "warning", "emergency", "alert", "critical issue",
            "verify now", "confirm asap", "act immediately", "time sensitive",
            "only today", "limited availability", "respond now", "no delay"
        ]
        
        self.financial_keywords = [
            "wire transfer", "bank details", "invoice", "payment", "account number",
            "routing number", "swift code", "iban", "credit card", "debit card",
            "bank account", "transfer funds", "money transfer", "payment processing",
            "refund", "reimbursement", "wire this amount"
        ]
        
        self.credential_keywords = [
            "password", "verify your account", "click here to login", "confirm identity",
            "reset password", "update password", "authenticate", "verification needed",
            "security code", "confirm credentials", "sign in", "log in",
            "ssn", "social security", "id verification", "re-authenticate"
        ]
        
        # Authority/Legitimacy-mimicking
        self.authority_keywords = [
            "compliance", "audit", "investigation", "federal agent", "irs",
            "fraud department", "security team", "legal", "lawsuit",
            "court", "jail", "prison", "arrest", "subpoena", "attorney",
            "financial crimes", "money laundering", "sanctions"
        ]
        
        # Personal identifiers (fake legitimacy)
        self.personal_identifiers = [
            "your account", "your email", "your password", "your information",
            "your transaction", "your order", "your bank", "your credit",
            "account 1234", "case #", "reference #", "transaction id"
        ]
        
        # Quid pro quo patterns
        self.quid_pro_quo = [
            "help you", "assist you", "support you", "benefit you", "advantage you",
            "special offer", "gift", "bonus", "reward", "exclusive access",
            "free", "no cost", "refund", "compensation", "claim prize"
        ]
        
        # Scareware patterns
        self.scareware_keywords = [
            "malware detected", "virus found", "system compromised", "unauthorized access",
            "suspicious activity", "unusual login", "security breach", "security risk",
            "update required", "update windows", "update your browser", "critical update",
            "your pc is at risk", "your device is infected", "threat detected"
        ]
        
    def analyze(self, subject: str, body: str) -> Dict:
        """Comprehensive behavioral analysis"""
        score = 0
        findings = []
        text_lower = (subject + " " + body).lower()
        
        # 1. Urgency analysis
        urgency_count = sum(1 for kw in self.urgency_keywords if kw in text_lower)
        if urgency_count >= 3:
            score += 15
            findings.append(f"Extreme urgency language ({urgency_count} keywords)")
        elif urgency_count == 2:
            score += 8
            findings.append(f"Multiple urgency keywords detected")
        
        # 2. Financial requests
        financial_count = sum(1 for kw in self.financial_keywords if kw in text_lower)
        if financial_count >= 2:
            score += 12
            findings.append(f"Multiple financial transaction indicators ({financial_count} keywords)")
        elif financial_count >= 1:
            score += 8
            findings.append("Financial transaction request detected")
        
        # 3. Credential harvesting
        cred_count = sum(1 for kw in self.credential_keywords if kw in text_lower)
        if cred_count >= 2:
            score += 18
            findings.append(f"Credential harvesting attack detected ({cred_count} keywords)")
        elif cred_count >= 1:
            score += 12
            findings.append("Login/credential verification request")
        
        # 4. Authority impersonation
        authority_count = sum(1 for kw in self.authority_keywords if kw in text_lower)
        if authority_count >= 2:
            score += 16
            findings.append(f"Authority impersonation (feds, courts, IRS): {authority_count} keywords")
        elif authority_count >= 1:
            score += 8
            findings.append("Impersonates authority figure")
        
        # 5. Personal details (fake legitimacy)
        personal_count = sum(1 for kw in self.personal_identifiers if kw in text_lower)
        if personal_count >= 3:
            score += 10
            findings.append(f"Attempts to appear personalized with {personal_count} personal identifiers")
        
        # 6. Quid pro quo detection
        quid_pro_quo_count = sum(1 for kw in self.quid_pro_quo if kw in text_lower)
        if quid_pro_quo_count >= 3 and urgency_count >= 1:
            score += 12
            findings.append("Quid pro quo attack: Offers benefit in exchange for action")
        
        # 7. Scareware detection
        scareware_count = sum(1 for kw in self.scareware_keywords if kw in text_lower)
        if scareware_count >= 2:
            score += 14
            findings.append(f"Scareware/fear-based manipulation ({scareware_count} keywords)")
        elif scareware_count >= 1:
            score += 6
            findings.append("Uses fear/security threat language")
        
        # 8. Contradiction/Urgency + unusual request combination
        has_urgency = urgency_count > 0
        has_financial = financial_count > 0
        has_unusual_sender = cred_count > 0 or authority_count > 0
        
        if has_urgency and (has_financial or has_unusual_sender):
            score += 5
            findings.append("Combines urgency with suspicious request pattern")
        
        # 9. Grammar quality analysis
        grammar_score = self._analyze_grammar_quality(body)
        if grammar_score > 0:
            score += grammar_score
            findings.append("Poor grammar/spelling indicates non-native or template phishing")
        
        # 10. Emoji/Unicode abuse
        emoji_score = self._analyze_emoji_abuse(body)
        if emoji_score > 0:
            score += emoji_score
            findings.append("Excessive emojis/unicode characters (phishing obfuscation)")
        
        return {
            "module": "Enhanced Content Analyzer",
            "score": min(score, self.MAX_SCORE),
            "findings": findings,
            "urgency_indicators": urgency_count,
            "financial_indicators": financial_count,
            "credential_indicators": cred_count,
            "authority_indicators": authority_count
        }
    
    @staticmethod
    def _analyze_grammar_quality(text: str) -> int:
        """Check for poor grammar/spelling typical of phishing"""
        score = 0
        
        # Common phishing misspellings
        phishing_typos = [
            "clck", "clik", "chck", "veriffy", "verificaton",
            "confirmm", "confrim", "accout", "acount", "recieve", "occured",
            "shoudl", "neccessary", "accomodate", "desparate"
        ]
        
        text_lower = text.lower()
        typo_count = sum(1 for typo in phishing_typos if typo in text_lower)
        
        if typo_count >= 3:
            score += 8
        elif typo_count >= 1:
            score += 3
        
        return score
    
    @staticmethod
    def _analyze_emoji_abuse(text: str) -> int:
        """Detect emoji/unicode abuse for obfuscation"""
        score = 0
        
        # Count emojis and special unicode
        emoji_pattern = re.compile(r'[\U0001F300-\U0001F9FF]|[\u2600-\u27BF]|[\u1F600-\u1F64F]')
        emoji_count = len(emoji_pattern.findall(text))
        
        if emoji_count > 10:
            score += 6
        elif emoji_count > 5:
            score += 2
        
        return score
