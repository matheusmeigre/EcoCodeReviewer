"""
Detector Refinado v2 - FASE 1
Sistema aprimorado de detecção automática de linguagens
"""
import re
from typing import Optional, Dict, List
from review_engine.core.dto import DetectionResult


class LanguageDetector:
    """Detector com heurísticas avançadas baseadas no roadmap"""
    
    # Extensões de arquivo por linguagem
    EXTENSIONS = {
        "python": [".py", ".pyw", ".pyi"],
        "javascript": [".js", ".mjs", ".cjs"],
        "typescript": [".ts", ".tsx"],
        "java": [".java"],
        "csharp": [".cs"],
        "sql": [".sql"],
        "nosql": [".mongodb", ".json"],
        "react": [".jsx", ".tsx"],
        "delphi": [".pas", ".dpr", ".dfm"],
        "go": [".go"],
        "rust": [".rs"],
        "php": [".php"],
        "ruby": [".rb"],
        "kotlin": [".kt", ".kts"],
        "swift": [".swift"],
        "html": [".html", ".htm"],
        "css": [".css", ".scss", ".sass"],
        "vue": [".vue"],
        "angular": [".ts", ".component.ts"],
        "svelte": [".svelte"],
        "bash": [".sh", ".bash"],
        "yaml": [".yml", ".yaml"],
        "dockerfile": ["Dockerfile", ".dockerfile"],
        "terraform": [".tf", ".tfvars"]
    }
    
    # Palavras-chave reservadas por linguagem
    KEYWORDS = {
        "python": ["def ", "class ", "import ", "from ", "elif ", "with ", "__init__"],
        "javascript": ["function ", "const ", "let ", "var ", "=> ", "console.log", "require("],
        "typescript": ["interface ", "type ", ": string", ": number", ": boolean"],
        "java": ["public class", "private ", "protected ", "System.out", "import java"],
        "csharp": ["using System", "namespace ", "public class", "Console.WriteLine"],
        "sql": ["SELECT ", "INSERT INTO", "UPDATE ", "DELETE FROM", "CREATE TABLE", "JOIN"],
        "go": ["func ", "package ", "import ", "type ", "struct ", "go ", "defer "],
        "rust": ["fn ", "let mut", "impl ", "pub ", "use ", "match "],
        "php": ["<?php", "function ", "$", "->", "namespace ", "use "],
        "ruby": ["def ", "end", "require ", "class ", "module ", "@"],
        "kotlin": ["fun ", "val ", "var ", "data class", "object "],
        "swift": ["func ", "var ", "let ", "import ", "class "],
        "bash": ["#!/bin/bash", "if [ ", "fi", "do", "done", "$"],
        "yaml": ["---", "apiVersion:", "kind:", "spec:", "metadata:"],
        "terraform": ["resource ", "variable ", "output ", "provider "]
    }
    
    # Padrões sintáticos regex
    SYNTAX_PATTERNS = {
        "python": [
            r'^\s*def\s+\w+\s*\(',
            r'^\s*class\s+\w+.*:',
            r'^\s*@\w+',
            r':\s*$'
        ],
        "javascript": [
            r'^\s*function\s+\w+\s*\(',
            r'=>\s*{',
            r'console\.(log|error|warn)',
            r'export\s+(default|const)'
        ],
        "java": [
            r'public\s+class\s+\w+',
            r'public\s+static\s+void\s+main',
            r'System\.out\.println'
        ],
        "sql": [
            r'^\s*SELECT\s+',
            r'^\s*INSERT\s+INTO',
            r'\bJOIN\b',
            r'\bWHERE\b'
        ],
        "go": [
            r'func\s+\w+\(',
            r'package\s+\w+',
            r':=\s*'
        ],
        "rust": [
            r'fn\s+\w+\(',
            r'let\s+mut\s+',
            r'impl\s+\w+'
        ],
        "kotlin": [
            r'fun\s+\w+\(',
            r'data\s+class\s+',
            r'val\s+\w+\s*='
        ],
        "swift": [
            r'func\s+\w+\(',
            r'import\s+Foundation',
            r'var\s+\w+:\s*\w+'
        ],
        "bash": [
            r'#!/bin/(ba)?sh',
            r'if\s+\[\s+',
            r'\$\w+'
        ],
        "yaml": [
            r'^---',
            r'^\w+:\s*$',
            r'^\s+-\s+'
        ],
        "dockerfile": [
            r'^FROM\s+',
            r'^RUN\s+',
            r'^COPY\s+'
        ],
        "terraform": [
            r'resource\s+"[^"]+"\s+"[^"]+"',
            r'variable\s+"[^"]+"',
            r'provider\s+"[^"]+"'
        ]
    }
    
    def __init__(self):
        self.confidence_threshold = 50  # Mínimo para não exigir fallback manual
    
    def detect(self, code: str, filename: Optional[str] = None) -> DetectionResult:
        """
        Detecção multi-camadas com nível de confiança
        1. Por extensão (95% confiança)
        2. Por palavras-chave (70% confiança)
        3. Por padrões sintáticos (80% confiança)
        """
        # Camada 1: Extensão de arquivo
        if filename:
            ext_result = self._detect_by_extension(filename)
            if ext_result:
                return ext_result
        
        # Camada 2: Palavras-chave
        keyword_result = self._detect_by_keywords(code)
        if keyword_result and keyword_result.confidence >= 70:
            return keyword_result
        
        # Camada 3: Padrões sintáticos
        syntax_result = self._detect_by_syntax(code)
        if syntax_result:
            return syntax_result
        
        # Fallback: Baixa confiança
        return DetectionResult(
            language="auto",
            confidence=0,
            detected_by="none",
            fallback_required=True
        )
    
    def _detect_by_extension(self, filename: str) -> Optional[DetectionResult]:
        """Detecção por extensão de arquivo"""
        filename_lower = filename.lower()
        
        for language, extensions in self.EXTENSIONS.items():
            for ext in extensions:
                if filename_lower.endswith(ext.lower()) or filename_lower == ext.lower():
                    return DetectionResult(
                        language=language,
                        confidence=95,
                        detected_by="extension"
                    )
        return None
    
    def _detect_by_keywords(self, code: str) -> Optional[DetectionResult]:
        """Detecção por palavras-chave"""
        scores = {}
        
        for language, keywords in self.KEYWORDS.items():
            matches = 0
            for keyword in keywords:
                if keyword in code:
                    matches += 1
            
            if matches > 0:
                # Confiança proporcional ao número de matches
                confidence = min(70 + (matches * 5), 90)
                scores[language] = confidence
        
        if not scores:
            return None
        
        # Retorna linguagem com maior score
        best_lang = max(scores, key=scores.get)
        return DetectionResult(
            language=best_lang,
            confidence=scores[best_lang],
            detected_by="keywords"
        )
    
    def _detect_by_syntax(self, code: str) -> Optional[DetectionResult]:
        """Detecção por padrões regex"""
        scores = {}
        
        for language, patterns in self.SYNTAX_PATTERNS.items():
            matches = 0
            for pattern in patterns:
                if re.search(pattern, code, re.MULTILINE | re.IGNORECASE):
                    matches += 1
            
            if matches > 0:
                confidence = min(70 + (matches * 10), 90)
                scores[language] = confidence
        
        if not scores:
            return None
        
        best_lang = max(scores, key=scores.get)
        return DetectionResult(
            language=best_lang,
            confidence=scores[best_lang],
            detected_by="syntax"
        )
    
    def get_supported_languages(self) -> List[str]:
        """Retorna todas as linguagens suportadas"""
        return list(set(self.EXTENSIONS.keys()))
