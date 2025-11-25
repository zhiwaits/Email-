import spf
import dkim
import dns.resolver
import re
from typing import Dict, Any

class AuthValidator:
    def __init__(self):
        self.name = "Authentication Validator"
        self.max_score = 30  # Increased to allow for higher scores
        
        # Common executive titles/roles that are often spoofed
        self.executive_keywords = [
            "ceo", "cfo", "cto", "coo", "president", "director", 
            "finance director", "general counsel", "managing director",
            "executive", "founder", "chairman"
        ]

    def analyze(self, headers: Dict[str, Any], body: str, sender_email: str) -> Dict[str, Any]:
        score = 0
        findings = []
        
        # 1. Check Authentication-Results header
        auth_results = headers.get('Authentication-Results', '')
        
        spf_fail = False
        dkim_fail = False
        dmarc_fail = False

        if auth_results:
            if 'spf=fail' in auth_results.lower() or 'spf=softfail' in auth_results.lower():
                spf_fail = True
                score += 10
                findings.append("SPF Validation Failed")
            
            if 'dkim=fail' in auth_results.lower():
                dkim_fail = True
                score += 10
                findings.append("DKIM Validation Failed")
                
            if 'dmarc=fail' in auth_results.lower():
                dmarc_fail = True
                score += 15
                findings.append("DMARC Validation Failed")
        
        # 2. Enhanced Display Name Spoofing & Executive Impersonation
        from_header = headers.get('From', '')
        if isinstance(from_header, list):
            from_header = from_header[0] if from_header else ''
            
        # Regex to extract email from "Name <email>" format
        match = re.search(r'<(.*?)>', from_header)
        if match:
            actual_email = match.group(1).lower()
            display_name = from_header.split('<')[0].strip().strip('"')
            display_name_lower = display_name.lower()
            
            # Check 1: Email in display name that doesn't match sender
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            spoofed_emails = re.findall(email_pattern, display_name_lower)
            
            for spoofed in spoofed_emails:
                if spoofed != actual_email:
                    score += 8
                    findings.append(f"Display Name Spoofing: '{spoofed}' in display name but actual sender is '{actual_email}'")
            
            # Check 2: Executive/Title Impersonation
            for exec_kw in self.executive_keywords:
                if exec_kw in display_name_lower:
                    # Check if sender domain looks legitimate (not external/suspicious)
                    domain = actual_email.split('@')[1] if '@' in actual_email else ''
                    
                    # Red flags for executive impersonation
                    suspicious_indicators = [
                        domain.endswith('.tk'),
                        domain.endswith('.ml'),
                        domain.endswith('.ga'),
                        '-' in domain and not domain.startswith('mail'),  # hyphenated domains
                        len(domain) > 25,  # unusually long domain
                        domain.count('-') > 2,  # multiple hyphens
                    ]
                    
                    if any(suspicious_indicators):
                        score += 12
                        findings.append(f"Executive Impersonation: Display name '{display_name}' claims to be {exec_kw} but sent from suspicious domain '{domain}'")
                        break
            
            # Check 3: Domain mismatch (sender claiming to be from company but different domain)
            # Common pattern: display name has legit company name but sender is external domain
            if '@' in actual_email:
                sender_domain = actual_email.split('@')[1]
                suspicious_domains = ['.tk', '.ml', '.ga', '.cf', '.gq', '-usa', '-security', '-verify']
                
                for sus_suffix in suspicious_domains:
                    if sus_suffix in sender_domain:
                        # Check if display name looks like internal employee
                        if any(word in display_name_lower for word in ['john', 'smith', 'support', 'admin', 'finance']):
                            score += 8
                            findings.append(f"Domain Spoofing: Internal-looking name '{display_name}' from external suspicious domain '{sender_domain}'")
                        break
        
        return {
            "module": self.name,
            "score": min(score, self.max_score),
            "findings": findings
        }
