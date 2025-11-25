from typing import List, Dict, Any
from modules.auth_enhanced import EnhancedAuthValidator
from modules.url_enhanced import EnhancedURLAnalyzer
from modules.content_enhanced import EnhancedContentAnalyzer
from modules.attachments import AttachmentAnalyzer
from modules.sender import SenderAnalyzer
from modules.spam_detector import SpamDetector
from modules.anomaly_detector import AnomalyDetector

class ScoringEngine:
    def __init__(self):
        self.whitelist = ["example.com", "myfirm.com"]

    def calculate(self, module_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Legacy method for backward compatibility"""
        total_score = 0
        all_findings = []
        
        for res in module_results:
            total_score += res.get('score', 0)
            all_findings.extend(res.get('findings', []))
            
        # Cap score at 100
        total_score = min(total_score, 100)
        
        # Determine Risk Level & Action
        if total_score <= 10:
            risk = "LOW"
            action = "DELIVER"
            color = "green"
        elif total_score <= 20:
            risk = "MEDIUM"
            action = "TAG [EXTERNAL]"
            color = "yellow"
        elif total_score <= 35:
            risk = "HIGH"
            action = "WARN USER"
            color = "orange"
        elif total_score <= 50:
            risk = "CRITICAL"
            action = "QUARANTINE"
            color = "red"
        else:
            risk = "MALICIOUS"
            action = "BLOCK"
            color = "darkred"

        return {
            "total_score": total_score,
            "risk_level": risk,
            "recommended_action": action,
            "ui_color": color,
            "findings": all_findings,
            "module_breakdown": module_results
        }


class EmailScorer:
    """Run all phishing detection modules and aggregate scores"""
    
    MAX_PHISHING_SCORE = 100
    
    @classmethod
    def calculate_phishing_score(cls, email_data: Dict) -> Dict:
        """Run all phishing modules (enhanced version) and return aggregate score"""
        
        # Use enhanced modules for better detection
        auth_validator = EnhancedAuthValidator()
        url_analyzer = EnhancedURLAnalyzer()
        content_analyzer = EnhancedContentAnalyzer()
        attachment_analyzer = AttachmentAnalyzer()
        sender_analyzer = SenderAnalyzer()
        anomaly_detector = AnomalyDetector()
        
        # Run all modules
        results = {
            "auth": auth_validator.analyze(
                email_data.get("all_headers", {}),
                email_data.get("body", ""),
                email_data.get("from", "")
            ),
            "url": url_analyzer.analyze(email_data.get("body", "")),
            "content": content_analyzer.analyze(
                email_data.get("subject", ""),
                email_data.get("body", "")
            ),
            "attachments": attachment_analyzer.analyze(email_data.get("attachments", [])),
            "sender": sender_analyzer.analyze(email_data.get("from", "")),
            "anomalies": anomaly_detector.analyze(email_data)
        }
        
        # Aggregate score
        total_score = 0
        all_findings = []
        
        for module_name, result in results.items():
            module_score = result.get("score", 0)
            total_score += module_score
            findings = result.get("findings", [])
            all_findings.extend(findings)
        
        # Normalize to 0-100 (increased max possible from enhanced modules)
        total_score = min(int(total_score), cls.MAX_PHISHING_SCORE)
        
        # Determine level with improved thresholds
        level = cls._get_phishing_level(total_score)
        
        return {
            "score": total_score,
            "level": level,
            "findings": all_findings[:20],  # Increased from 15 to show more findings
            "modules": results
        }
    
    @classmethod
    def _get_phishing_level(cls, score: int) -> str:
        """Convert score to phishing risk level"""
        if score >= 70:
            return "CRITICAL"
        elif score >= 50:
            return "HIGH"
        elif score >= 30:
            return "MEDIUM"
        elif score >= 10:
            return "LOW"
        else:
            return "MINIMAL"

