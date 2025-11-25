# VAMS - Email Security Analysis System

**Vulnerability Analysis & Malice Scoring** - An automated tool for law firms to detect phishing, spam, and malicious emails.

---

## 🎯 Overview

VAMS is a comprehensive email security analysis tool designed specifically for law firms. It analyzes emails across multiple dimensions to identify potential threats including:

- **Phishing Attempts** - Social engineering and credential harvesting
- **Spam & Marketing** - Unsolicited bulk communications
- **CEO Fraud** - Executive impersonation scams
- **Time-Wasting Inquiries** - Low-priority messages

### Key Features

✅ **Memory-Only Processing** - No email content persisted to disk  
✅ **Multi-Layer Analysis** - 85+ detection indicators  
✅ **Real-Time Scoring** - Instant phishing and spam classification  
✅ **User-Friendly Interface** - Beautiful dark theme with responsive design  
✅ **Multiple Input Methods** - Upload .eml files, paste content, or test samples  
✅ **Detailed Findings** - Specific indicators for each detected threat  

---

## 📋 Email Security Guidance

### RED FLAGS: When to Block or Verify

#### **1. Sender Verification Issues** 🚨
- Email claims to be from CEO/Finance but comes from external domain
- Slight domain variations (`lawfirm-usa.com` vs `lawfirm.com`)
- Free email domains (Gmail, Yahoo) for business correspondence
- Suspicious/cheap TLDs (.tk, .ml, .ga, .cf)
- Generic sender names (noreply, support, contact)
- Display name spoofing ("CEO John Smith" from unrelated domain)

#### **2. Urgency Tactics** ⏰
- "URGENT: Immediate action required"
- "Deal will expire if not completed today"
- ALL CAPS with multiple exclamation marks
- Artificial scarcity ("only 1 slot remaining")
- Time pressure on sensitive actions (wire transfers, account changes)

#### **3. Financial Requests** 💰
- Wire transfer requests (especially unusual amounts)
- Banking details requested
- Payment to new/unknown vendors
- Invoice/receipt requests from unverified sources
- Requests for prepayment, advance fees, or "processing fees"
- Requests for gift cards or cryptocurrency

#### **4. Suspicious Links & Attachments** 🔗
- Link text differs from actual URL destination
- Shortened URLs (bit.ly, tinyurl) in unsolicited emails
- IP addresses instead of domain names (192.168.1.1)
- Suspicious file extensions:
  - Executables: `.exe`, `.scr`, `.vbs`, `.bat`, `.cmd`
  - Office with macros: `.docm`, `.xlsm`, `.pptm`
  - Archives: `.zip`, `.rar` with unknown contents

#### **5. Authentication Failures** ✓
- SPF/DKIM/DMARC failures (visible in email headers)
- Gmail/Outlook warnings: "Check this message" or authentication fail
- No `Reply-To` header (spam indicator)
- Inconsistent sender information

#### **6. Generic or Unusual Content** 📝
- "Dear Beneficiary" instead of your name
- Poor spelling/grammar from established organizations
- Unusual business requests unrelated to your firm's practice
- Copy-paste spam language patterns
- High density of financial/urgency keywords
- Repetitive text patterns

---

## ⚡ What to Do When You Suspect Malicious Email

### Immediate Actions

1. **DON'T** click links or download attachments
2. **DON'T** reply with sensitive information
3. **Verify** sender identity through out-of-band methods (call them directly)
4. **Upload** the email to VAMS for analysis
5. **Report** to IT/Security team immediately
6. **Move** email to Spam/Junk folder (don't delete)

### VAMS Score Interpretation

| Score | Level | Risk | Action |
|-------|-------|------|--------|
| 70-100 | 🚨 CRITICAL | High phishing confidence | **BLOCK** immediately |
| 50-69 | ⚠️ HIGH | Phishing indicators present | **VERIFY** sender |
| 30-49 | ⚡ MEDIUM | Suspicious characteristics | **REVIEW** carefully |
| 0-29 | ✅ LOW | Appears legitimate | **ACCEPT** - low risk |

### Spam Score Interpretation

| Score | Level | Action |
|-------|-------|--------|
| 80-100 | Likely Spam | Quarantine/Delete |
| 50-79 | Suspicious Spam | Review before engaging |
| 30-49 | Low Risk | May be legitimate marketing |
| 0-29 | Probably Legitimate | Low spam probability |

---

## 🔧 Using VAMS

### Getting Started

#### **Option 1: Upload .eml File**
1. Download the email as `.eml` from your email client
2. Click the upload zone or drag the file
3. Click "Analyze Email"
4. Review the detailed findings

#### **Option 2: Paste Email Content**
1. Copy the complete email (including headers)
2. Go to "Paste Email Content" tab
3. Paste into the text area
4. Click "Analyze"

#### **Option 3: Test with Sample**
1. Go to "Sample Phishing" tab
2. Review the sample malicious email
3. Click "Analyze Sample" to see how VAMS detects it
4. Study the findings to understand detection patterns

### Interpreting Results

**Phishing Analysis**
- Detects: Executive impersonation, urgency language, credential requests, suspicious URLs, authentication failures

**Spam Analysis**
- Detects: Marketing keywords, generic greetings, newsletter patterns, financial references, link density

**Recommendation**
- **BLOCK**: Don't interact, delete immediately, block sender
- **VERIFY**: Call sender to confirm legitimacy
- **QUARANTINE**: Move to spam, review later if needed
- **REVIEW**: Double-check before trusting
- **ACCEPT**: Low risk, safe to read

---

## 🏗️ Technical Architecture

### Backend (Python + FastAPI)
- **Memory-only processing** - No files written to disk
- **Multiple analysis modules**:
  - Authentication (SPF/DKIM/DMARC)
  - URL reputation (TLD checks, shortening detection)
  - Content analysis (keywords, urgency tactics)
  - Attachment scanning (dangerous extensions, macros)
  - Sender verification (domain validation, executive lists)
  - Spam detection (85+ indicators)

### Frontend (Vue 3 + Tailwind CSS)
- Responsive design (mobile, tablet, desktop)
- Dark theme with intuitive UI
- Real-time analysis with progress tracking
- Detailed findings visualization
- Multiple input methods

---

## 📊 Analysis Examples

### ✅ Legitimate Email
```
From: partner@lawfirm.com
To: attorney@lawfirm.com
Subject: Discovery Documents - Case #2025-001

Hi Sarah,

I've attached the discovery documents for the Anderson case. 
Please review at your convenience.

Best regards,
John Smith
Senior Partner
```
**Result**: ✅ LEGITIMATE (Score: 5/100)

### ⚠️ Suspicious Phishing
```
From: CEO <ceo@lawfirm-usa.com>
To: accounting@lawfirm.com
Subject: URGENT: Wire Transfer Required Today

IMMEDIATE ACTION NEEDED!

Wire $250,000 to: Bank xyz, Account 987654321

Respond within 1 hour.
```
**Result**: 🚨 MALICIOUS PHISHING (Score: 78/100)

### 📧 Marketing Spam
```
From: newsletter@promotions.tk
To: staff@lawfirm.com
Subject: EXCLUSIVE OFFER - Save 50% TODAY!!!

Dear Valued Customer,

Don't miss out on our LIMITED TIME offer!!!

Click here now: bit.ly/deals123

Unsubscribe
```
**Result**: 📬 LIKELY SPAM (Score: 85/100)

---

## 🚀 Installation & Setup

### Requirements
- Python 3.12+
- Node.js 20.19+
- FastAPI
- Vue 3

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Backend runs on `http://localhost:8000`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on `http://localhost:5173`

---

## 📖 Training for Law Firm Staff

### For Partners & Attorneys
- Review the "Red Flags" section above
- Run 2-3 analysis examples using "Sample Phishing" tab
- Practice verifying suspicious senders through out-of-band methods

### For Admin & Finance Staff
- Pay special attention to wire transfer requests
- Always verify unusual banking instructions
- Use VAMS before processing any financial requests from unknown sources

### For IT/Security Team
- Monitor VAMS usage and high-risk emails
- Implement feedback loop to improve detection
- Update executive/partner names quarterly in configuration

---

## 🔐 Privacy & Security

✅ **No Data Persistence** - Emails analyzed only in RAM, never stored  
✅ **Secure Processing** - No external API calls with sensitive content  
✅ **Attorney-Client Privilege** - Email content never leaves your system  
✅ **GDPR Compliant** - No personal data collection or retention  

---

## 📞 Support & Feedback

For questions or improvements, contact your IT/Security team.

---

**Last Updated**: November 25, 2025  
**Version**: 1.0  
**Status**: Production Ready 
