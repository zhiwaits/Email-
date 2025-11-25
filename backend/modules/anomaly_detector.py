from typing import Dict, List
import re

class AnomalyDetector:
    """Detect statistical and behavioral anomalies"""
    
    MAX_SCORE = 30
    
    def analyze(self, email_data: Dict) -> Dict:
        """Detect email anomalies"""
        score = 0
        findings = []
        
        # 1. Time-based anomalies
        time_score = self._check_timing_anomalies(email_data)
        score += time_score
        if time_score > 0:
            findings.append(f"Suspicious send time detected: {time_score} points")
        
        # 2. Content density anomalies
        density_score = self._check_content_density(email_data)
        score += density_score
        if density_score > 0:
            findings.append(f"Abnormal content distribution: {density_score} points")
        
        # 3. Encoding anomalies
        encoding_score = self._check_encoding_anomalies(email_data)
        score += encoding_score
        if encoding_score > 0:
            findings.append("Unusual character encoding detected")
        
        # 4. Header anomalies
        header_score = self._check_header_anomalies(email_data)
        score += header_score
        if header_score > 0:
            findings.append(f"Malformed headers: {header_score} points")
        
        return {
            "module": "Anomaly Detector",
            "score": min(score, self.MAX_SCORE),
            "findings": findings
        }
    
    @staticmethod
    def _check_timing_anomalies(email_data: Dict) -> int:
        """Check for suspicious send times"""
        score = 0
        
        # Emails sent at odd hours (2AM-5AM) are suspicious
        date_header = email_data.get('Date', '')
        if date_header:
            # Extract hour if possible
            try:
                hour = int(re.search(r'(\d{1,2}):', date_header).group(1))
                if hour >= 2 and hour <= 5:
                    score = 3
            except:
                pass
        
        return score
    
    @staticmethod
    def _check_content_density(email_data: Dict) -> int:
        """Detect unusual content distributions"""
        score = 0
        
        body = email_data.get('body', '')
        subject = email_data.get('subject', '')
        
        # Very short body with long subject = suspicious
        if subject and body:
            if len(subject) > len(body) * 0.8:
                score += 2
        
        # Mostly links/URLs with minimal text
        urls = len(re.findall(r'https?://', body))
        words = len(body.split())
        
        if words > 20 and urls > words * 0.2:
            score += 4
        
        return score
    
    @staticmethod
    def _check_encoding_anomalies(email_data: Dict) -> int:
        """Detect encoding tricks used for obfuscation"""
        score = 0
        
        body = email_data.get('body', '')
        
        # Base64 encoded content (often used to bypass filters)
        if re.search(r'[A-Za-z0-9+/]{20,}={0,2}', body):
            score += 2
        
        # HTML entity encoding
        if re.search(r'&#\d{3,};', body):
            score += 2
        
        # Hex encoding
        if re.search(r'%[0-9a-fA-F]{2}', body):
            score += 2
        
        return score
    
    @staticmethod
    def _check_header_anomalies(email_data: Dict) -> int:
        """Check email headers for anomalies"""
        score = 0
        
        headers = email_data.get('all_headers', {})
        
        # Missing critical headers
        critical_headers = ['From', 'To', 'Subject', 'Date']
        for header in critical_headers:
            if header not in headers:
                score += 2
        
        return min(score, 8)
