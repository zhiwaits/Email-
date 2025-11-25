import re
from typing import Dict, List
from urllib.parse import urlparse

class EnhancedURLAnalyzer:
    """Advanced URL reputation and manipulation detection"""
    
    MAX_SCORE = 45  # Increased from 25
    
    def __init__(self):
        self.suspicious_tlds = [
            '.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.date',
            '.racing', '.webcam', '.download', '.science', '.click', '.space',
            '.review', '.win', '.party', '.bid', '.faith', '.accountant'
        ]
        
        self.url_shorteners = [
            'bit.ly', 'tinyurl.com', 'short.link', 'goo.gl', 'ow.ly',
            'is.gd', 'buff.ly', 'adf.ly', 't.co', 'ur1.ca'
        ]
    
    def analyze(self, body: str) -> Dict:
        """Analyze all URLs in email body"""
        score = 0
        findings = []
        
        # Extract URLs
        urls = self._extract_urls(body)
        
        if not urls:
            return {"module": "Enhanced URL Analyzer", "score": 0, "findings": ["No URLs detected"], "url_count": 0}
        
        suspicious_urls = []
        
        for url in urls[:15]:  # Analyze first 15 URLs
            url_score = 0
            url_issues = []
            
            # 1. Suspicious TLD check
            if self._has_suspicious_tld(url):
                url_score += 8
                url_issues.append("Suspicious TLD")
            
            # 2. IP-based URL (highly suspicious)
            if self._is_ip_url(url):
                url_score += 12
                url_issues.append("IP-based URL")
            
            # 3. Shortened URL
            if self._is_shortened_url(url):
                url_score += 6
                url_issues.append("Shortened URL (hides real destination)")
            
            # 4. Typosquatting/look-alike domain
            typo_score, typo_issue = self._check_typosquatting(url)
            url_score += typo_score
            if typo_issue:
                url_issues.append(typo_issue)
            
            # 5. Port number anomalies
            if self._has_unusual_port(url):
                url_score += 5
                url_issues.append("Non-standard port number")
            
            # 6. Subdomain depth (multiple subdomains = suspicious)
            subdomain_score = self._check_subdomain_depth(url)
            url_score += subdomain_score
            if subdomain_score > 0:
                url_issues.append("Excessive subdomain nesting")
            
            # 7. URL path length anomaly
            if self._has_unusually_long_path(url):
                url_score += 4
                url_issues.append("Unusually long URL path (obfuscation)")
            
            # 8. Homograph/Unicode domain names
            if self._has_unicode_characters(url):
                url_score += 10
                url_issues.append("Unicode/homograph attack in domain")
            
            # 9. Authentication in URL (user:pass@domain)
            if self._has_embedded_credentials(url):
                url_score += 8
                url_issues.append("Username/password embedded in URL")
            
            if url_score > 0:
                suspicious_urls.append({
                    "url": self._truncate_url(url),
                    "score": url_score,
                    "issues": url_issues
                })
            
            score += url_score
        
        if suspicious_urls:
            findings.append(f"Detected {len(suspicious_urls)} suspicious URLs")
            for sus_url in suspicious_urls[:3]:
                findings.append(f"• {sus_url['url']}: {', '.join(sus_url['issues'])}")
        
        return {
            "module": "Enhanced URL Analyzer",
            "score": min(score, self.MAX_SCORE),
            "findings": findings,
            "url_count": len(urls),
            "suspicious_url_count": len(suspicious_urls)
        }
    
    @staticmethod
    def _extract_urls(text: str) -> List[str]:
        """Extract all URLs from text"""
        url_pattern = r'https?://[^\s<>"\)]+|ftp://[^\s<>"\)]+'
        return re.findall(url_pattern, text)
    
    def _has_suspicious_tld(self, url: str) -> bool:
        return any(url.lower().endswith(tld) for tld in self.suspicious_tlds)
    
    @staticmethod
    def _is_ip_url(url: str) -> bool:
        """Check if URL uses IP address instead of domain"""
        ip_pattern = r'http[s]?://(\d{1,3}\.){3}\d{1,3}'
        return bool(re.search(ip_pattern, url))
    
    def _is_shortened_url(self, url: str) -> bool:
        return any(shortener in url.lower() for shortener in self.url_shorteners)
    
    def _check_typosquatting(self, url: str) -> tuple:
        """Detect typosquatting (misspelled legitimate domains)"""
        score = 0
        issue = None
        
        url_lower = url.lower()
        
        # Common typos: amzaon, gogle, mircrosoft, etc.
        typos = {
            'amzaon': 'amazon',
            'gogle': 'google',
            'mircrosoft': 'microsoft',
            'facbook': 'facebook',
            'paypel': 'paypal'
        }
        
        for typo, real in typos.items():
            if typo in url_lower:
                score = 10
                issue = f"Typosquatting: '{typo}' mimics '{real}'"
                break
        
        return score, issue
    
    @staticmethod
    def _has_unusual_port(url: str) -> bool:
        """Check for non-standard ports"""
        try:
            parsed = urlparse(url)
            port = parsed.port
            
            # Standard ports: 80 (HTTP), 443 (HTTPS), 8080, 3000
            if port and port not in [80, 443, 8080, 3000, 8443]:
                return True
        except:
            pass
        
        return False
    
    @staticmethod
    def _check_subdomain_depth(url: str) -> int:
        """Excessive subdomains = suspicious"""
        try:
            parsed = urlparse(url)
            hostname = parsed.netloc
            subdomain_count = hostname.count('.')
            
            # More than 3 dots = suspicious (sub.sub.sub.domain.com)
            if subdomain_count > 3:
                return 4
        except:
            pass
        
        return 0
    
    @staticmethod
    def _has_unusually_long_path(url: str) -> bool:
        """URLs with very long paths often used for obfuscation"""
        try:
            parsed = urlparse(url)
            if len(parsed.path) > 200:
                return True
        except:
            pass
        
        return False
    
    @staticmethod
    def _has_unicode_characters(url: str) -> bool:
        """Detect unicode/homograph attacks"""
        try:
            url.encode('ascii')
            return False
        except UnicodeEncodeError:
            return True
    
    @staticmethod
    def _has_embedded_credentials(url: str) -> bool:
        """Check for user:pass@domain patterns"""
        return '@' in url and '://' not in url.split('@')[0]
    
    @staticmethod
    def _truncate_url(url: str, max_length: int = 60) -> str:
        if len(url) > max_length:
            return url[:max_length] + "..."
        return url
