import re
from typing import Dict, List

class EnhancedAuthValidator:
    """Advanced authentication and impersonation detection"""
    
    MAX_SCORE = 50  # Increased from 30
    
    def __init__(self):
        self.executive_keywords = [
            "ceo", "cfo", "cto", "coo", "cfo", "vp", "president", "director", 
            "founder", "chairman", "managing director", "general counsel",
            "finance director", "chief", "executive", "owner", "partner",
            "general manager", "board member"
        ]
        
        # Common vendor/service impersonations
        self.service_impersonations = [
            ('microsoft', ['outlook', 'office365', 'sharepoint', 'teams', 'azure']),
            ('google', ['gmail', 'drive', 'workspace', 'analytics']),
            ('amazon', ['aws', 'amazon.com', 'prime']),
            ('apple', ['icloud', 'itunes', 'appstore']),
            ('paypal', ['ebay', 'checkout']),
            ('bank', ['security', 'verify', 'update', 'confirm']),
        ]
        
        # Known spoofed company patterns
        self.spoofed_companies = [
            'support-', 'noreply-', 'secure-', 'verify-', 'notify-',
            'billing-', 'alert-', 'admin-', 'no-reply'
        ]
    
    def analyze(self, headers: Dict, body: str, sender_email: str) -> Dict:
        """Enhanced authentication and impersonation detection"""
        score = 0
        findings = []
        
        # 1. SPF/DKIM/DMARC validation (existing, score 0-15)
        auth_score = self._check_authentication_headers(headers)
        score += auth_score
        if auth_score > 0:
            findings.append(f"Authentication failed: {auth_score} points")
        
        # 2. Executive impersonation (existing, enhanced)
        exec_score, exec_finding = self._check_executive_impersonation(headers, sender_email)
        score += exec_score
        if exec_finding:
            findings.append(exec_finding)
        
        # 3. Service/Vendor impersonation
        vendor_score, vendor_finding = self._check_vendor_impersonation(headers, body, sender_email)
        score += vendor_score
        if vendor_finding:
            findings.append(vendor_finding)
        
        # 4. Domain continuity check
        continuity_score = self._check_domain_consistency(headers, sender_email)
        score += continuity_score
        if continuity_score > 0:
            findings.append(f"Domain inconsistency detected: {continuity_score} points")
        
        # 5. Reply-To spoofing
        reply_to_score = self._check_reply_to_spoofing(headers, sender_email)
        score += reply_to_score
        if reply_to_score > 0:
            findings.append("Reply-To address differs from sender (redirection risk)")
        
        # 6. Sender reputation anomalies
        rep_score = self._check_sender_reputation_anomalies(headers, sender_email)
        score += rep_score
        if rep_score > 0:
            findings.append(f"Sender reputation issues: {rep_score} points")
        
        return {
            "module": "Enhanced Auth Validator",
            "score": min(score, self.MAX_SCORE),
            "findings": findings
        }
    
    def _check_authentication_headers(self, headers: Dict) -> int:
        """Check SPF/DKIM/DMARC (existing logic)"""
        score = 0
        auth_results = headers.get('Authentication-Results', '')
        
        if 'spf=fail' in auth_results.lower() or 'spf=softfail' in auth_results.lower():
            score += 8
        if 'dkim=fail' in auth_results.lower():
            score += 8
        if 'dmarc=fail' in auth_results.lower():
            score += 10
        
        return min(score, 15)
    
    def _check_executive_impersonation(self, headers: Dict, sender_email: str) -> tuple:
        """Enhanced executive impersonation detection"""
        score = 0
        finding = None
        
        from_header = headers.get('From', '')
        match = re.search(r'<(.*?)>', str(from_header))
        
        if match:
            actual_email = match.group(1).lower()
            display_name = str(from_header).split('<')[0].strip().strip('"')
            display_name_lower = display_name.lower()
            
            # Check for executive keywords
            for exec_kw in self.executive_keywords:
                if exec_kw in display_name_lower:
                    # Check if sender domain is suspicious
                    domain = actual_email.split('@')[1] if '@' in actual_email else ''
                    
                    if self._is_suspicious_domain(domain):
                        score = 16
                        finding = f"Executive Impersonation: '{display_name}' with suspicious domain '{domain}'"
                    elif '@' not in actual_email:
                        score = 12
                        finding = "Invalid sender format masquerading as executive"
                    else:
                        score = 8
                        finding = f"Potential executive impersonation: {exec_kw} from external domain"
                    
                    break
        
        return score, finding
    
    def _check_vendor_impersonation(self, headers: Dict, body: str, sender_email: str) -> tuple:
        """Detect impersonation of known vendors"""
        score = 0
        finding = None
        
        from_header = str(headers.get('From', '')).lower()
        body_lower = body.lower()
        sender_lower = sender_email.lower()
        
        # Check each vendor
        for vendor, keywords in self.service_impersonations:
            vendor_present = any(kw in body_lower for kw in keywords)
            
            if vendor_present:
                # Check if sender actually represents vendor
                if vendor in sender_lower:
                    continue  # Likely legitimate
                
                # Check for spoofed patterns
                if any(pattern in from_header for pattern in self.spoofed_companies):
                    score = 14
                    finding = f"Impersonates {vendor}: Using spoofed sender pattern"
                    break
                
                # Check for external domain claiming to be vendor
                if '@' in sender_email:
                    domain = sender_email.split('@')[1]
                    if not domain.startswith(vendor.replace(' ', '')):
                        score = 10
                        finding = f"Mentions {vendor} but sent from '{domain}'"
                        break
        
        return score, finding
    
    @staticmethod
    def _is_suspicious_domain(domain: str) -> bool:
        """Check if domain looks suspicious"""
        suspicious_patterns = [
            domain.endswith('.tk'), domain.endswith('.ml'),
            '-' in domain and len(domain.split('-')) > 3,
            domain.count('-') > 2,
            len(domain) > 30,
            domain.startswith('mail-'), domain.startswith('secure-'),
            domain.startswith('verify-'), domain.startswith('support-')
        ]
        return any(suspicious_patterns)
    
    @staticmethod
    def _check_domain_consistency(headers: Dict, sender_email: str) -> int:
        """Check if From/Return-Path/Reply-To are consistent"""
        score = 0
        
        from_addr = headers.get('From', '').split('@')[-1].strip('>').strip() if '@' in headers.get('From', '') else ''
        return_path = headers.get('Return-Path', '').split('@')[-1].strip('>').strip() if '@' in headers.get('Return-Path', '') else ''
        reply_to = headers.get('Reply-To', '').split('@')[-1].strip('>').strip() if '@' in headers.get('Reply-To', '') else ''
        
        mismatches = 0
        if from_addr and return_path and from_addr != return_path:
            mismatches += 1
        if from_addr and reply_to and from_addr != reply_to:
            mismatches += 1
        
        score = mismatches * 4
        return score
    
    @staticmethod
    def _check_reply_to_spoofing(headers: Dict, sender_email: str) -> int:
        """Reply-To redirects to different domain"""
        score = 0
        
        from_addr = headers.get('From', '')
        reply_to = headers.get('Reply-To', '')
        
        if from_addr and reply_to and from_addr.lower() != reply_to.lower():
            # Extract domains
            from_domain = from_addr.split('@')[-1].strip('>').strip() if '@' in from_addr else ''
            reply_domain = reply_to.split('@')[-1].strip('>').strip() if '@' in reply_to else ''
            
            if from_domain and reply_domain and from_domain != reply_domain:
                score = 6
        
        return score
    
    @staticmethod
    def _check_sender_reputation_anomalies(headers: Dict, sender_email: str) -> int:
        """Check for reputation red flags"""
        score = 0
        
        # Missing common headers
        if 'Message-ID' not in headers:
            score += 2
        if 'Date' not in headers:
            score += 2
        if 'Subject' not in headers:
            score += 2
        
        # Anomalous sender format
        if not re.match(r'^[^@]+@[^@]+\.[a-z]{2,}$', sender_email):
            score += 3
        
        return min(score, 8)
