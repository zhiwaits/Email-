import email
from email import policy
from typing import Dict, Any, List
import re
from bs4 import BeautifulSoup

class EmailParser:
    """Parse .eml format from bytes without disk access"""
    
    @staticmethod
    def parse_from_bytes(file_content: bytes) -> Dict[str, Any]:
        """Parse .eml format from bytes without touching disk"""
        
        try:
            msg = email.message_from_bytes(
                file_content,
                policy=policy.default
            )
        except Exception as e:
            raise ValueError(f"Invalid email format: {str(e)}")
        
        # Extract basic headers
        headers = dict(msg.items())
        
        # Extract body parts
        body_text = ""
        body_html = ""
        attachment_metadata = []
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = part.get("Content-Disposition", "")
                
                if content_type == "text/plain":
                    try:
                        body_text += part.get_payload(decode=True).decode(errors='ignore')
                    except:
                        pass
                        
                elif content_type == "text/html":
                    try:
                        body_html += part.get_payload(decode=True).decode(errors='ignore')
                    except:
                        pass
                        
                elif "attachment" in content_disposition:
                    # Metadata only, don't extract
                    filename = part.get_filename() or "unknown"
                    attachment_metadata.append({
                        "filename": filename,
                        "content_type": content_type,
                        "size": len(part.get_payload(decode=True)) if part.get_payload() else 0
                    })
        else:
            try:
                body_text = msg.get_payload(decode=True).decode(errors='ignore')
            except:
                body_text = msg.get_payload()
        
        # Clean HTML to plain text if needed
        if body_html and not body_text:
            soup = BeautifulSoup(body_html, 'html.parser')
            body_text = soup.get_text(separator='\n')
        
        # Extract all URLs from body and headers
        urls = EmailParser._extract_urls(body_text + body_html + headers.get("From", ""))
        
        # Combine body text
        combined_body = body_text if body_text else body_html
        
        return {
            "from": headers.get("From", ""),
            "to": headers.get("To", ""),
            "subject": headers.get("Subject", ""),
            "cc": headers.get("Cc", ""),
            "bcc": headers.get("Bcc", ""),
            "date": headers.get("Date", ""),
            "all_headers": headers,
            "body_text": body_text,
            "body_html": body_html,
            "body": combined_body,  # For backward compatibility
            "urls": urls,
            "attachments": attachment_metadata,
            "has_attachments": len(attachment_metadata) > 0,
            "attachment_count": len(attachment_metadata),
            "headers": headers  # For backward compatibility
        }
    
    @staticmethod
    def _extract_urls(text: str) -> List[str]:
        """Extract all URLs from text"""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        return list(set(re.findall(url_pattern, text)))
