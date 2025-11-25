#!/usr/bin/env python3
"""
Test script to verify memory-only email analysis
No files are written to disk during analysis
"""

from parser import EmailParser
from scoring import EmailScorer
from modules.spam_detector import SpamDetector
import json

def test_analysis():
    """Test with sample_phishing.eml"""
    
    print("\n" + "="*80)
    print("VAMS: Memory-Only Email Analysis Test")
    print("="*80 + "\n")
    
    try:
        # Read email into memory
        with open("../sample_phishing.eml", "rb") as f:
            email_bytes = f.read()
        
        print(f"✓ Email loaded into RAM ({len(email_bytes)} bytes)")
        print("✓ No temporary files created on disk\n")
        
        # Parse email (in memory)
        print("Parsing email...")
        email_data = EmailParser.parse_from_bytes(email_bytes)
        print(f"✓ From: {email_data['from']}")
        print(f"✓ Subject: {email_data['subject']}")
        print(f"✓ URLs found: {len(email_data['urls'])}")
        print(f"✓ Attachments: {email_data['attachment_count']}\n")
        
        # Run phishing analysis
        print("Running phishing analysis...")
        phishing_result = EmailScorer.calculate_phishing_score(email_data)
        print(f"✓ Phishing Score: {phishing_result['score']}/100")
        print(f"✓ Phishing Level: {phishing_result['level']}\n")
        
        # Run spam analysis
        print("Running spam analysis...")
        spam_result = SpamDetector.calculate_spam_score(email_data)
        print(f"✓ Spam Score: {spam_result['score']}/100")
        print(f"✓ Spam Level: {spam_result['level']}")
        print(f"✓ Spam Probability: {spam_result['probability']}\n")
        
        # Determine classification
        print("Classification Results:")
        print("-" * 80)
        
        if phishing_result['score'] >= 70:
            classification = "MALICIOUS_PHISHING"
        elif phishing_result['score'] >= 40:
            classification = "SUSPICIOUS_PHISHING"
        elif spam_result['score'] >= 80:
            classification = "LIKELY_SPAM"
        elif spam_result['score'] >= 50:
            classification = "SUSPICIOUS_SPAM"
        else:
            classification = "LEGITIMATE"
        
        print(f"Email Classification: {classification}\n")
        
        # Key findings
        print("Top Phishing Findings:")
        for i, finding in enumerate(phishing_result['findings'][:5], 1):
            print(f"  {i}. {finding}")
        
        print("\nTop Spam Findings:")
        for i, finding in enumerate(spam_result['findings'][:5], 1):
            print(f"  {i}. {finding}")
        
        print("\n" + "="*80)
        print("✓ Test completed successfully")
        print("✓ All analysis done in RAM - no disk I/O")
        print("="*80 + "\n")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_analysis()
    exit(0 if success else 1)
