import re
import requests
import time
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from typing import Dict, Any, List

load_dotenv()

class URLAnalyzer:
    def __init__(self):
        self.name = "URL Reputation Analyzer"
        self.max_score = 25
        self.vt_api_key = os.getenv("VIRUSTOTAL_API_KEY") 
        self.vt_url = "https://www.virustotal.com/api/v3/urls"
        self.suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.date']

    def extract_urls(self, text: str) -> List[str]:
        # Basic URL regex
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        return re.findall(url_pattern, text)

    def is_ip_url(self, url: str) -> bool:
        domain = urlparse(url).netloc
        # Simple IP check (could be improved)
        return bool(re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain))

    def check_virustotal(self, url: str) -> bool:
        if not self.vt_api_key or self.vt_api_key == "YOUR_VIRUSTOTAL_API_KEY":
            return False # Skip if no key
            
        try:
            # 1. Submit URL for scanning (or get ID) - Simplified for MVP to just check report if exists
            # In a real impl, we'd need to base64 encode the URL to get the ID
            import base64
            url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
            
            headers = {"x-apikey": self.vt_api_key}
            response = requests.get(f"{self.vt_url}/{url_id}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get('data', {}).get('attributes', {}).get('last_analysis_stats', {})
                if stats.get('malicious', 0) > 0:
                    return True
            return False
        except Exception as e:
            print(f"VT API Error: {e}")
            return False

    def analyze(self, body: str) -> Dict[str, Any]:
        score = 0
        findings = []
        urls = self.extract_urls(body)
        
        # Tier 1: Local Checks
        for url in urls:
            domain = urlparse(url).netloc
            
            # Check TLD
            for tld in self.suspicious_tlds:
                if domain.endswith(tld):
                    score += 12
                    findings.append(f"Suspicious TLD detected: {tld} in {url}")
            
            # Check IP
            if self.is_ip_url(url):
                score += 10
                findings.append(f"IP-based URL detected: {url}")
                
        # Tier 2: Cache (Placeholder)
        # TODO: Implement SQLite cache check
        
        # Tier 3: VirusTotal (Limit to first 2 URLs to save quota)
        # Only run if we haven't already maxed out score
        if score < self.max_score:
            for url in urls[:2]:
                is_malicious = self.check_virustotal(url)
                if is_malicious:
                    score += 25
                    findings.append(f"VirusTotal flagged URL: {url}")
                    break # Stop after one positive hit
                time.sleep(15) # Rate limit compliance (4/min = 15s delay)

        return {
            "module": self.name,
            "score": min(score, self.max_score),
            "findings": findings
        }
