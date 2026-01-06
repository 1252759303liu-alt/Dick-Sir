"""Chapter structure recognition service"""
import re
from typing import List, Dict, Optional
from backend.utils.text_processor import TextProcessor


class ChapterService:
    """Service for recognizing and structuring textbook chapters"""
    
    # Common chapter heading patterns - Pre-compiled for performance
    CHAPTER_PATTERNS = [
        # Chinese patterns
        re.compile(r'^第[一二三四五六七八九十百千万\d]+章\s*[：:]\s*(.+)'),  # 第一章：标题
        re.compile(r'^第[一二三四五六七八九十百千万\d]+章\s+(.+)'),  # 第一章 标题
        re.compile(r'^第[一二三四五六七八九十百千万\d]+节\s*[：:]\s*(.+)'),  # 第一节：标题
        # English patterns
        re.compile(r'^Chapter\s+(\d+)\s*[：:]\s*(.+)', re.IGNORECASE),  # Chapter 1: Title
        re.compile(r'^Chapter\s+(\d+)\s+(.+)', re.IGNORECASE),  # Chapter 1 Title
        # Numeric patterns
        re.compile(r'^(\d+)\.\s+(.+)'),  # 1. Title
        re.compile(r'^(\d+\.\d+)\s+(.+)'),  # 1.1 Title
        re.compile(r'^(\d+\.\d+\.\d+)\s+(.+)'),  # 1.1.1 Title
    ]
    
    SECTION_PATTERNS = [
        re.compile(r'^第[一二三四五六七八九十百千万\d]+节\s*[：:]\s*(.+)'),
        re.compile(r'^Section\s+(\d+)\s*[：:]\s*(.+)', re.IGNORECASE),
        re.compile(r'^(\d+\.\d+)\s+(.+)'),
    ]
    
    @staticmethod
    def identify_chapters(text: str) -> List[Dict]:
        """
        Identify chapters from text content
        
        Args:
            text: Full text content
            
        Returns:
            List of chapter dictionaries with title, level, and content
        """
        lines = text.split('\n')
        chapters = []
        current_chapter = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_content:
                    current_content.append('')
                continue
            
            # Check if line matches any chapter pattern
            is_chapter = False
            for pattern in ChapterService.CHAPTER_PATTERNS:
                match = pattern.match(line)
                if match:
                    # Save previous chapter
                    if current_chapter:
                        current_chapter['content'] = '\n'.join(current_content).strip()
                        chapters.append(current_chapter)
                    
                    # Start new chapter
                    current_chapter = {
                        'title': line,
                        'level': 1,
                        'content': '',
                        'start_line': len(chapters)
                    }
                    current_content = []
                    is_chapter = True
                    break
            
            if not is_chapter:
                # Check for section patterns (sub-chapters)
                for pattern in ChapterService.SECTION_PATTERNS:
                    match = pattern.match(line)
                    if match:
                        # This could be a subsection
                        if current_chapter:
                            current_content.append(line)
                        is_chapter = True
                        break
            
            if not is_chapter and current_chapter:
                current_content.append(line)
        
        # Save the last chapter
        if current_chapter:
            current_chapter['content'] = '\n'.join(current_content).strip()
            chapters.append(current_chapter)
        
        # If no chapters found, treat entire text as one chapter
        if not chapters:
            chapters.append({
                'title': '全文',
                'level': 1,
                'content': text,
                'start_line': 0
            })
        
        return chapters
    
    @staticmethod
    def build_chapter_tree(chapters: List[Dict]) -> Dict:
        """
        Build a hierarchical tree structure from flat chapter list
        
        Args:
            chapters: List of chapter dictionaries
            
        Returns:
            Tree structure with nested chapters
        """
        tree = {
            'title': 'Table of Contents',
            'children': []
        }
        
        for chapter in chapters:
            tree['children'].append({
                'title': chapter['title'],
                'level': chapter.get('level', 1),
                'has_content': bool(chapter.get('content', '').strip())
            })
        
        return tree
    
    @staticmethod
    def extract_keywords(text: str, top_n: int = 10) -> List[str]:
        """
        Extract keywords from chapter content
        
        Args:
            text: Chapter text
            top_n: Number of top keywords to extract
            
        Returns:
            List of keywords
        """
        # Simple keyword extraction based on frequency
        # Remove common words and count frequency
        words = TextProcessor.tokenize(text)
        word_freq = {}
        
        for word in words:
            if len(word) > 1:  # Filter out single characters
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:top_n]]
