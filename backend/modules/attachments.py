from typing import Dict, Any, List
import os

class AttachmentAnalyzer:
    def __init__(self):
        self.name = "Attachment Risk Analyzer"
        self.max_score = 15
        
        self.dangerous_extensions = [
            '.exe', '.scr', '.bat', '.vbs', '.js', '.ps1', '.cmd', '.com', '.msi'
        ]
        self.macro_extensions = ['.docm', '.xlsm', '.pptm']
        self.archive_extensions = ['.zip', '.rar', '.7z', '.tar', '.gz']

    def analyze(self, attachments: List[Dict[str, Any]]) -> Dict[str, Any]:
        score = 0
        findings = []
        
        for att in attachments:
            filename = att.get('filename', '').lower()
            if not filename:
                continue
                
            # Check Dangerous Extensions
            _, ext = os.path.splitext(filename)
            if ext in self.dangerous_extensions:
                score += 15
                findings.append(f"Dangerous file extension detected: {filename}")
                
            # Check Macros
            if ext in self.macro_extensions:
                score += 12
                findings.append(f"Macro-enabled Office file detected: {filename}")
                
            # Check Double Extensions (e.g., invoice.pdf.exe)
            # Remove the last extension and check if there's still a known extension
            name_without_ext, _ = os.path.splitext(filename)
            _, second_ext = os.path.splitext(name_without_ext)
            if second_ext and (second_ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.txt']):
                score += 10
                findings.append(f"Double extension evasion detected: {filename}")

        return {
            "module": self.name,
            "score": min(score, self.max_score),
            "findings": findings
        }
