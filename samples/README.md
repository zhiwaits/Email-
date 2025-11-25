# VAMS Sample Emails - Testing Guide

This folder contains 9 different email samples for testing VAMS with various threat scenarios. Each sample demonstrates different attack vectors and detection patterns.

---

## 📋 Sample Files

### 1. **legitimate_email.eml** ✅
**Type:** Legitimate Business Email  
**Expected VAMS Score:** 5-15 (GREEN - ACCEPT)

**Characteristics:**
- Professional greeting using name ("Hi Attorney Johnson")
- Clear business context (contract review follow-up)
- Specific details (page 7, liability clause)
- Normal formatting and language
- Legitimate sender domain (@actuallaw.com)
- No urgency tactics, no financial requests
- Verifiable phone number

**Why VAMS Accepts It:**
- ✓ No red flags detected
- ✓ Personalized, not generic
- ✓ Reasonable request timeframe
- ✓ Professional tone
- ✓ No suspicious links/attachments

---

### 2. **ceo_fraud.eml** 🚨 
**Type:** CEO Fraud / Impersonation  
**Expected VAMS Score:** 75-85 (RED - BLOCK)

**Red Flags:**
- Impersonation of executive authority
- Domain variation (lawfirm-secure.com vs lawfirm.com)
- URGENT, CONFIDENTIAL, IMMEDIATE pressure
- Unusual amount ($250,000)
- Financial request (wire transfer)
- Specific banking details
- Pressure to avoid discussion
- Multiple urgency markers (URGENT, IMMEDIATELY, TODAY)

**Detection Modules Triggered:**
- ✓ Auth Validator: Display name mismatched with domain
- ✓ Content Analyzer: Urgency language, financial request
- ✓ URL Analyzer: Suspicious domain variation
- ✓ Sender Analyzer: External domain impersonating executive

**Why VAMS Blocks It:**
- Classic CEO fraud pattern
- Multiple simultaneous red flags
- Time pressure on financial transaction
- Instruction to keep secret

---

### 3. **nigerian_prince_scam.eml** 🚨
**Type:** Nigerian Prince / Time-Wasting Inquiry  
**Expected VAMS Score:** 85-95 (RED - BLOCK)

**Red Flags:**
- Nigerian reference (classic scam indicator)
- Inheritance claim
- Unbelievable amount ($8.5M)
- Requests for personal information (passport, SSN, bank details)
- Processing fee requirement ($5,000)
- Time pressure (48 hours)
- Too-good-to-be-true bonus ($250k finder's fee)
- Multiple urgency markers (!!!,URGENT,ACT NOW)
- Shortened URL (bit.ly)
- Suspicious TLD (.tk)

**Detection Modules Triggered:**
- ✓ Spam Detector: Nigerian, lottery, inheritance, beneficiary, advance fee, processing fee keywords
- ✓ Content Analyzer: Multiple urgency tactics, financial amounts
- ✓ URL Analyzer: Shortened URL, suspicious TLD
- ✓ Sender Analyzer: Suspicious TLD (.tk), generic identity

**Why VAMS Blocks It:**
- 5+ time-wasting keywords detected
- Extremely high keyword density
- Classic advance-fee scam pattern
- Financial reference pattern

---

### 4. **phishing_credential_harvest.eml** 🚨
**Type:** Phishing - Credential Harvesting  
**Expected VAMS Score:** 70-80 (RED - BLOCK)

**Red Flags:**
- Spoofed legitimate service (Office 365)
- Suspicious link domain (office365-secure-verify.ml)
- Authentication scare tactic
- Unusual location claim (Beijing)
- Account suspension threat
- Requests credential verification
- Suspicious TLD (.ml)
- HTML-based (obfuscation technique)

**Detection Modules Triggered:**
- ✓ URL Analyzer: Spoofed domain, suspicious TLD
- ✓ Content Analyzer: Urgency language, credential request, authentication failure claim
- ✓ Sender Analyzer: Suspicious TLD, free domain (no-reply@)
- ✓ Auth Validator: Domain variation from legitimate

**Why VAMS Blocks It:**
- Impersonation of trusted service
- Credential harvesting request
- Scare tactics (account suspension)
- Suspicious verification URL

---

### 5. **malicious_attachment.eml** 🚨
**Type:** Malware - Malicious Attachment  
**Expected VAMS Score:** 60-70 (HIGH - VERIFY/BLOCK)

**Red Flags:**
- Executable file (.exe) masquerading as form
- Generic greeting ("Dear Employee")
- Instructions to "enable macros" (code execution)
- Time pressure (Friday deadline)
- Suspicious sender domain (.ga TLD)
- Attachment is binary (not legitimate)
- Tax-themed social engineering

**Detection Modules Triggered:**
- ✓ Attachment Analyzer: Dangerous .exe file detected (+15 points)
- ✓ Content Analyzer: Generic greeting, time pressure
- ✓ Sender Analyzer: Suspicious TLD (.ga)
- ✓ URL Analyzer: No legitimate URLs

**Why VAMS Flags It:**
- Executable file attachment is maximum danger signal
- Never open .exe files from unknown sources
- Even if named like document, still executable

---

### 6. **spam_marketing.eml** 📧
**Type:** Spam - Marketing/Promotional  
**Expected VAMS Score:** 55-70 (ORANGE - QUARANTINE)

**Red Flags:**
- Excessive marketing language
- Multiple ALL CAPS warnings
- Limited-time pressure ("expires in 24 HOURS")
- Artificial scarcity ("only 3 SLOTS REMAINING")
- Multiple action buttons (high link density)
- Promotional domains (.top TLD)
- Generic greeting
- Shortened URLs (bit.ly multiple times)
- No genuine unsubscribe link
- Multiple money-related language

**Detection Modules Triggered:**
- ✓ Spam Detector: Marketing keywords density, urgency tactics
- ✓ Content Analyzer: Multiple urgency markers, financial language
- ✓ URL Analyzer: Shortened URLs, suspicious TLD
- ✓ Sender Analyzer: Promotional domain pattern

**Why VAMS Quarantines It:**
- Clear marketing/spam pattern
- No legitimate business value
- Typical unsolicited commercial email

---

### 7. **time_wasting_lottery.eml** 🚨
**Type:** Advance-Fee Scam / Lottery Fraud  
**Expected VAMS Score:** 80-90 (RED - QUARANTINE)

**Red Flags:**
- Lottery winning claim (unsolicited)
- Extreme amount (€2,500,000)
- Generic greeting ("To claim your prize")
- Processing fee demand (€850)
- Identity verification request
- Banking details request
- Time pressure (48 hours)
- Multiple urgency indicators (!!!, URGENT, EXPIRES)
- Suspicious TLD (.cf)
- Confidentiality warning (secrecy tactic)
- Too-good-to-be-true premise

**Detection Modules Triggered:**
- ✓ Spam Detector: Lottery, congratulations, you won, selected, beneficiary, processing fee, advance fee
- ✓ Content Analyzer: Extreme financial amounts, urgency language
- ✓ Sender Analyzer: Suspicious TLD, generic identity
- ✓ URL Analyzer: TinyURL shortened link

**Why VAMS Blocks It:**
- Classic time-wasting inquiry
- 6+ time-wasting keywords
- Advance-fee pattern (characteristic of scams)
- Unrealistic winning amount

---

### 8. **double_extension_attack.eml** 🚨
**Type:** Double Extension Evasion / Malware  
**Expected VAMS Score:** 65-75 (HIGH - VERIFY/BLOCK)

**Red Flags:**
- Double extension filename: "Invoice_5847.pdf.exe"
- File appears to be PDF, actually executable
- Generic greeting
- Pressure to open attachment ("please confirm receipt")
- Suspicious sender domain (.click TLD)
- Generic sender identity (noreply@)
- Binary executable disguised as document

**Detection Modules Triggered:**
- ✓ Attachment Analyzer: Double extension evasion detected (+10 points)
- ✓ Attachment Analyzer: Dangerous .exe extension (+15 points)
- ✓ Sender Analyzer: Suspicious TLD, generic identity
- ✓ Content Analyzer: Pressure to open attachment

**Why VAMS Flags It:**
- Double extension is classic evasion technique
- Real file is .exe (executable/dangerous)
- Disguised as harmless PDF
- Sender pressure to open suggests malicious intent

---

### 9. **suspicious_link_spoofing.eml** 🚨
**Type:** Phishing - Link Spoofing  
**Expected VAMS Score:** 55-70 (HIGH - VERIFY)

**Red Flags:**
- Spoofed bank domain
- IP address as URL (192.168.1.100)
- Suspicious query parameters
- Generic greeting ("Dear Valued Customer")
- Account restriction threat
- Requests account details verification
- Link appears legitimate but goes to IP address
- One-time use threat (creates urgency)

**Detection Modules Triggered:**
- ✓ URL Analyzer: IP address instead of domain (suspicious)
- ✓ Content Analyzer: Account threat, verification demand
- ✓ Sender Analyzer: Spoofed bank domain variation
- ✓ Auth Validator: Domain inconsistency

**Why VAMS Flags It:**
- IP addresses in URLs are suspicious
- Bank impersonation
- Credential harvesting intent
- Threat-based pressure tactic

---

## 🧪 How to Test

### Option 1: Upload .eml File
```
1. Open VAMS frontend
2. Click "📁 Upload .eml File"
3. Select one of these files
4. View results
5. Check predicted score vs actual score
```

### Option 2: Paste Content
```
1. Open .eml file in text editor
2. Select all (Ctrl+A)
3. Copy (Ctrl+C)
4. Open VAMS
5. Click "📋 Paste Email Content"
6. Paste (Ctrl+V)
7. Analyze
```

---

## 📊 Expected Results Summary

| File | Type | Expected Score | Expected Classification |
|------|------|-----------------|------------------------|
| legitimate_email.eml | ✅ Legitimate | 5-15 | LEGITIMATE (GREEN) |
| ceo_fraud.eml | 🚨 Phishing | 75-85 | MALICIOUS_PHISHING (RED) |
| nigerian_prince_scam.eml | 🚨 Scam | 85-95 | LIKELY_SPAM (RED) |
| phishing_credential_harvest.eml | 🚨 Phishing | 70-80 | MALICIOUS_PHISHING (RED) |
| malicious_attachment.eml | 🚨 Malware | 60-70 | SUSPICIOUS_PHISHING (ORANGE) |
| spam_marketing.eml | 📧 Spam | 55-70 | SUSPICIOUS_SPAM (ORANGE) |
| time_wasting_lottery.eml | 🚨 Scam | 80-90 | LIKELY_SPAM (RED) |
| double_extension_attack.eml | 🚨 Malware | 65-75 | SUSPICIOUS_PHISHING (ORANGE) |
| suspicious_link_spoofing.eml | 🚨 Phishing | 55-70 | SUSPICIOUS_PHISHING (ORANGE) |

---

## 🎓 Learning Outcomes

By testing these samples, you'll learn:

1. **Legitimate emails** have personal touches, context, reasonable requests
2. **CEO fraud** uses domain variations, urgency, financial pressure
3. **Time-wasting inquiries** use unbelievable amounts, processing fees
4. **Phishing** asks for credentials, uses service impersonation
5. **Malware attachments** use double extensions, executable masquerades
6. **Spam** has marketing keywords, artificial scarcity, link density
7. **Link spoofing** uses IP addresses, suspicious domains
8. **Evasion techniques** include extensions tricks, encoded content

---

## ⚠️ Important Notes

- These are **educational samples** - real malware is removed/sanitized
- Actual .exe content is base64-encoded dummy data (not dangerous)
- Never run actual malicious code
- Use VAMS in safe, isolated testing environment
- These patterns help train security awareness in your firm

---

## 📝 Custom Testing

To create your own test email:
1. Use any of these templates
2. Modify content while keeping red flags
3. Add your own domains/details
4. Export as .eml from email client
5. Test with VAMS

This builds institutional knowledge about threat patterns in your organization.
