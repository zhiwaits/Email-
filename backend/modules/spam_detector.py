import re
from typing import Dict, List, Tuple
from collections import Counter

class SpamDetector:
    """Detect spam, newsletters, marketing, and time-wasting inquiries"""
    
    MAX_SPAM_SCORE = 100
    
    # Spam indicators
    SPAM_KEYWORDS = {
        "marketing": [
            "unsubscribe", "marketing", "promotional", "deal", "offer",
            "discount", "save now", "limited time", "act now", "click here",
            "call now", "buy now", "order now", "exclusive offer", "special promotion"
        ],
        "newsletter": [
            "newsletter", "mailing list", "subscribe", "weekly digest",
            "monthly report", "news update", "announcement", "bulletin",
            "publication", "journal"
        ],
        "time_wasting": [
            "nigerian", "lottery", "inheritance", "claim your prize",
            "congratulations", "you won", "selected", "beneficiary",
            "advance fee", "processing fee", "update your account",
            "verify your identity", "confirm password"
        ],
        "bulk_marketing": [
            "dear customer", "dear user", "dear member", "dear subscriber",
            "dear valued", "to whom it may concern", "dear friend"
        ]
    }
    
    # Spam patterns
    SPAM_PATTERNS = {
        "url_spam": r"(?:http|https)?(?::\/\/)?(?:www\.)?[a-zA-Z0-9\-\.]+\.(tk|ml|ga|cf|click|download|top|win)",
        "excessive_caps": r"[A-Z]{10,}",
        "money_references": r"\$\d+[\d,]*(?:\.\d+)?|usd|gbp|eur",
        "html_heavy": r"<[^>]+>",
    }
    
    @classmethod
    def calculate_spam_score(cls, email_data: Dict) -> Dict:
        """
        Calculate spam probability score (0-100)
        Returns: {score, level, findings, probability}
        """
        score = 0
        findings = []
        
        # Check 1: Subject line analysis
        subject_score, subject_findings = cls._analyze_subject(email_data.get("subject", ""))
        score += subject_score
        findings.extend(subject_findings)
        
        # Check 2: Body content analysis
        body_score, body_findings = cls._analyze_body(email_data.get("body", ""))
        score += body_score
        findings.extend(body_findings)
        
        # Check 3: Sender analysis
        sender_score, sender_findings = cls._analyze_sender(email_data.get("from", ""))
        score += sender_score
        findings.extend(sender_findings)
        
        # Check 4: Structure analysis
        structure_score, structure_findings = cls._analyze_structure(email_data)
        score += structure_score
        findings.extend(structure_findings)
        
        # Check 5: Link analysis
        link_score, link_findings = cls._analyze_links(email_data.get("urls", []))
        score += link_score
        findings.extend(link_findings)
        
        # Normalize to 0-100
        score = min(int(score), cls.MAX_SPAM_SCORE)
        
        # Determine level
        level = cls._get_spam_level(score)
        
        # Calculate probability (0.0 - 1.0)
        probability = round(score / 100.0, 2)
        
        return {
            "module": "Spam Detector",
            "score": score,
            "level": level,
            "findings": findings[:10],  # Top 10 findings
            "probability": probability
        }
    
    @classmethod
    def _analyze_subject(cls, subject: str) -> Tuple[int, List[str]]:
        """Analyze subject line for spam indicators"""
        score = 0
        findings = []
        
        if not subject:
            return 0, ["No subject line (suspicious)"]
        
        subject_lower = subject.lower()
        
        # Check for spam keywords
        for category, keywords in cls.SPAM_KEYWORDS.items():
            matches = [kw for kw in keywords if kw in subject_lower]
            if matches:
                score += len(matches) * 3
                findings.append(f"Subject contains {category} keywords: {', '.join(matches[:3])}")
                break  # Count once per category
        
        # Excessive caps
        if re.search(cls.SPAM_PATTERNS["excessive_caps"], subject):
            score += 5
            findings.append("Subject line uses excessive capitals")
        
        # Urgency spam
        urgency_words = ["!!!", "URGENT", "ACT NOW", "IMMEDIATELY", "ASAP"]
        if any(word in subject.upper() for word in urgency_words):
            score += 8
            findings.append("Subject uses urgency manipulation tactics")
        
        # Question mark spam
        if subject.count("?") > 2:
            score += 3
            findings.append("Subject contains excessive question marks")
        
        return score, findings
    
    @classmethod
    def _analyze_body(cls, body: str) -> Tuple[int, List[str]]:
        """Analyze email body for spam indicators"""
        score = 0
        findings = []
        
        if not body or len(body) < 10:
            return 0, []
        
        body_lower = body.lower()
        word_count = len(body.split())
        
        # 1. Keyword density analysis
        keyword_matches = Counter()
        for category, keywords in cls.SPAM_KEYWORDS.items():
            for keyword in keywords:
                if keyword in body_lower:
                    keyword_matches[category] += body_lower.count(keyword)
        
        if keyword_matches:
            dominant_category = keyword_matches.most_common(1)[0][0]
            match_count = keyword_matches.most_common(1)[0][1]
            score += min(match_count * 2, 25)
            findings.append(
                f"High density of {dominant_category} keywords ({match_count} occurrences)"
            )
        
        # 2. Generic greeting analysis
        generic_greetings = [
            "dear customer", "dear user", "dear friend", "to whom it may concern",
            "dear valued", "dear sir/madam", "hello there"
        ]
        if any(greeting in body_lower for greeting in generic_greetings):
            score += 5
            findings.append("Uses generic greeting instead of personalization")
        
        # 3. Money/financial references
        money_matches = re.findall(cls.SPAM_PATTERNS["money_references"], body_lower)
        if money_matches:
            score += len(money_matches) * 4
            findings.append(f"Contains {len(money_matches)} financial references")
        
        # 4. Link-to-text ratio
        links = re.findall(r'https?://[^\s]+', body)
        if word_count > 20 and links:
            link_ratio = len(links) / (word_count / 100)
            if link_ratio > 0.5:
                score += 8
                findings.append(f"High link density ({len(links)} links for {word_count} words)")
        
        # 5. HTML heavy
        html_tags = len(re.findall(cls.SPAM_PATTERNS["html_heavy"], body))
        if html_tags > 30:
            score += 5
            findings.append(f"Heavy HTML formatting ({html_tags} tags) - typical of marketing")
        
        # 6. Repetitive language
        words = body_lower.split()
        if len(words) > 20:
            word_freq = Counter(words)
            most_common = word_freq.most_common(1)[0]
            if most_common[1] > len(words) * 0.15:
                score += 4
                findings.append(f"Repetitive language ('{most_common[0]}' used {most_common[1]} times)")
        
        # 7. No unsubscribe link
        if any(keyword in body_lower for keywords in cls.SPAM_KEYWORDS.values() for keyword in keywords):
            if "unsubscribe" not in body_lower and "opt-out" not in body_lower:
                score += 3
                findings.append("Marketing content without unsubscribe link (CAN-SPAM violation)")
        
        return score, findings
    
    @classmethod
    def _analyze_sender(cls, sender: str) -> Tuple[int, List[str]]:
        """Analyze sender for spam indicators"""
        score = 0
        findings = []
        
        if not sender:
            return 0, []
        
        sender_lower = sender.lower()
        
        # Extract email domain
        if "@" in sender:
            domain = sender.split("@")[1].strip(">").lower()
            
            # Free email for business
            free_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com"]
            if domain in free_domains:
                score += 3
                findings.append(f"Sender uses free email domain: {domain}")
            
            # Suspicious TLDs
            if re.search(r'\.(tk|ml|ga|cf|click|download|top|win)$', domain):
                score += 5
                findings.append(f"Sender uses suspicious TLD: {domain}")
            
            # Generic sender names
            generic_names = ["noreply", "support", "info", "contact", "admin", "notification"]
            if any(name in sender_lower for name in generic_names):
                score += 2
                findings.append(f"Generic sender identity")
        
        return score, findings
    
    @classmethod
    def _analyze_structure(cls, email_data: Dict) -> Tuple[int, List[str]]:
        """Analyze email structure for spam indicators"""
        score = 0
        findings = []
        
        # 1. Missing headers
        from_header = email_data.get("from", "")
        to_header = email_data.get("to", "")
        subject = email_data.get("subject", "")
        
        if not from_header:
            score += 5
            findings.append("Missing From header")
        if not to_header:
            score += 3
            findings.append("BCC'd or missing recipient header")
        
        # 2. Too many recipients
        if to_header and (to_header.count(",") > 10 or to_header.count(";") > 10):
            score += 8
            findings.append("Sent to many recipients (mass mailing)")
        
        # 3. Attachment analysis
        attachments = email_data.get("attachments", [])
        if attachments:
            for attachment in attachments:
                filename = attachment.get("filename", "").lower()
                # Suspicious extensions
                suspicious_exts = [".exe", ".scr", ".vbs", ".bat", ".cmd", ".com"]
                if any(filename.endswith(ext) for ext in suspicious_exts):
                    score += 10
                    findings.append(f"Suspicious executable attachment")
                
                # Financial document pattern
                if any(word in filename for word in ["invoice", "payment", "receipt", "bill"]):
                    score += 3
                    findings.append(f"Financial document attachment: {filename}")
        
        # 4. No reply-to
        if "Reply-To" not in email_data.get("all_headers", {}) and "reply-to" not in str(email_data.get("all_headers", {})).lower():
            score += 2
            findings.append("No Reply-To header")
        
        return score, findings
    
    @classmethod
    def _analyze_links(cls, urls: List[str]) -> Tuple[int, List[str]]:
        """Analyze links for spam indicators"""
        score = 0
        findings = []
        
        if not urls:
            return 0, []
        
        for url in urls[:10]:  # Analyze first 10 URLs
            url_lower = url.lower()
            
            # Suspicious TLDs
            if re.search(cls.SPAM_PATTERNS["url_spam"], url_lower):
                score += 4
                findings.append(f"URL uses suspicious TLD")
            
            # Shortened URLs
            if any(shortener in url_lower for shortener in ["bit.ly", "tinyurl", "short.link", "goo.gl"]):
                score += 3
                findings.append(f"Shortened URL detected")
        
        return score, findings
    
    @classmethod
    def _get_spam_level(cls, score: int) -> str:
        """Convert score to spam level"""
        if score >= 80:
            return "LIKELY_SPAM"
        elif score >= 50:
            return "SUSPICIOUS"
        elif score >= 30:
            return "LOW_RISK"
        else:
            return "NOT_SPAM"
