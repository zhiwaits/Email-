from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import re

# Import Modules
from parser import EmailParser
from scoring import EmailScorer
from modules.spam_detector import SpamDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VAMS API",
    description="Vulnerability Analysis & Malice Scoring API - Email Security",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "VAMS API is running", "version": "1.0.0"}

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "Email Analysis API"}

@app.post("/api/analyze")
async def analyze_email(file: UploadFile = File(...)):
    """
    Analyze email entirely in memory.
    No files written to disk, no persistent storage of email content.
    Returns: Classification, phishing score, spam score, and recommendations.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.eml'):
            return JSONResponse(
                {
                    "error": "Only .eml files supported",
                    "status": "error"
                },
                status_code=400
            )
        
        # 1. Read file into RAM only
        logger.info(f"Analyzing: {file.filename}")
        file_bytes = await file.read()
        
        if len(file_bytes) > 50 * 1024 * 1024:  # 50MB limit
            return JSONResponse(
                {
                    "error": "File too large (max 50MB)",
                    "status": "error"
                },
                status_code=413
            )
        
        # 2. Parse email in memory
        email_data = EmailParser.parse_from_bytes(file_bytes)
        
        # 3. Run analysis modules
        phishing_result = EmailScorer.calculate_phishing_score(email_data)
        spam_result = SpamDetector.calculate_spam_score(email_data)
        
        # 4. Determine overall classification
        classification = _classify_email(phishing_result, spam_result)
        
        # 5. Generate response (no email content stored)
        response = {
            "status": "success",
            "classification": classification,
            "phishing": {
                "score": phishing_result["score"],
                "level": phishing_result["level"],
                "findings": phishing_result["findings"]
            },
            "spam": {
                "score": spam_result["score"],
                "level": spam_result["level"],
                "findings": spam_result["findings"],
                "probability": spam_result["probability"]
            },
            "recommendation": _get_recommendation(classification, phishing_result, spam_result),
            "metadata": {
                "sender": email_data["from"],
                "subject": email_data["subject"],
                "has_attachments": email_data["has_attachments"],
                "attachment_count": email_data["attachment_count"],
                "url_count": len(email_data["urls"])
            }
        }
        
        logger.info(f"Analysis complete: {classification} (Phishing: {phishing_result['score']}, Spam: {spam_result['score']})")
        return response
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return JSONResponse(
            {
                "error": str(e),
                "status": "error"
            },
            status_code=400
        )
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return JSONResponse(
            {
                "error": "Internal analysis error",
                "status": "error"
            },
            status_code=500
        )

def _classify_email(phishing_result, spam_result):
    """Determine overall email classification"""
    phishing_score = phishing_result["score"]
    spam_score = spam_result["score"]
    
    # Phishing takes priority
    if phishing_score >= 70:
        return "MALICIOUS_PHISHING"
    elif phishing_score >= 40:
        return "SUSPICIOUS_PHISHING"
    elif spam_score >= 80:
        return "LIKELY_SPAM"
    elif spam_score >= 50:
        return "SUSPICIOUS_SPAM"
    else:
        return "LEGITIMATE"

def _get_recommendation(classification, phishing_result, spam_result):
    """Generate action recommendation"""
    recommendations = {
        "MALICIOUS_PHISHING": {
            "action": "BLOCK",
            "reason": "High confidence phishing attempt detected",
            "level": "CRITICAL"
        },
        "SUSPICIOUS_PHISHING": {
            "action": "VERIFY",
            "reason": "Phishing indicators detected - verify sender out-of-band",
            "level": "HIGH"
        },
        "LIKELY_SPAM": {
            "action": "QUARANTINE",
            "reason": "High probability of unsolicited marketing or spam",
            "level": "MEDIUM"
        },
        "SUSPICIOUS_SPAM": {
            "action": "REVIEW",
            "reason": "Possible spam - review before trusting",
            "level": "MEDIUM"
        },
        "LEGITIMATE": {
            "action": "ACCEPT",
            "reason": "No significant security concerns detected",
            "level": "LOW"
        }
    }
    return recommendations.get(classification, {})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
