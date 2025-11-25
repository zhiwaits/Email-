#!/usr/bin/env python
"""Test the email analysis pipeline"""

from parser import EmailParser
from scoring import EmailScorer
from modules.spam_detector import SpamDetector
import json

# Read the sample phishing email
with open('../sample_phishing.eml', 'rb') as f:
    eml_content = f.read()

# Parse it
email_data = EmailParser.parse_from_bytes(eml_content)

# Run analysis
phishing_result = EmailScorer.calculate_phishing_score(email_data)
spam_result = SpamDetector.calculate_spam_score(email_data)

# Print results
print('=== PHISHING ANALYSIS ===')
print('Score:', phishing_result['score'])
print('Level:', phishing_result['level'])
print('Top Findings:')
for finding in phishing_result['findings'][:5]:
    print('  -', finding)

print('\n=== SPAM ANALYSIS ===')
print('Score:', spam_result['score'])
print('Level:', spam_result['level'])
print('Probability:', spam_result['probability'])
print('Top Findings:')
for finding in spam_result['findings'][:5]:
    print('  -', finding)

# Classification
if phishing_result['score'] >= 70:
    classification = 'MALICIOUS_PHISHING'
elif phishing_result['score'] >= 40:
    classification = 'SUSPICIOUS_PHISHING'
elif spam_result['score'] >= 80:
    classification = 'LIKELY_SPAM'
elif spam_result['score'] >= 50:
    classification = 'SUSPICIOUS_SPAM'
else:
    classification = 'LEGITIMATE'

print('\n=== FINAL CLASSIFICATION ===')
print('Result:', classification)

if classification == 'MALICIOUS_PHISHING':
    print('Recommendation: BLOCK')
    print('Reason: High confidence phishing attempt detected')
    print('Risk Level: CRITICAL')
elif classification == 'SUSPICIOUS_PHISHING':
    print('Recommendation: VERIFY')
    print('Reason: Phishing indicators detected - verify sender out-of-band')
    print('Risk Level: HIGH')
elif classification == 'LIKELY_SPAM':
    print('Recommendation: QUARANTINE')
    print('Reason: High probability of unsolicited marketing or spam')
    print('Risk Level: MEDIUM')
elif classification == 'LEGITIMATE':
    print('Recommendation: ACCEPT')
    print('Reason: No significant security concerns detected')
    print('Risk Level: LOW')

print('\n=== EMAIL METADATA ===')
print('Subject:', email_data['subject'])
print('From:', email_data['from'])
print('URLs found:', len(email_data['urls']))
print('Attachments:', email_data['attachment_count'])
