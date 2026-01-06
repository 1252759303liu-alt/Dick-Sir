"""PDF text extraction service"""
import pdfplumber
from PyPDF2 import PdfReader
from typing import Optional


class PDFService:
    """Service for extracting text from PDF files"""
    
    @staticmethod
    def extract_text_pdfplumber(pdf_path: str) -> str:
        """
        Extract text from PDF using pdfplumber
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            text_content = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
            return "\n\n".join(text_content)
        except Exception as e:
            raise Exception(f"Error extracting text with pdfplumber: {str(e)}")
    
    @staticmethod
    def extract_text_pypdf2(pdf_path: str) -> str:
        """
        Extract text from PDF using PyPDF2 (fallback method)
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            text_content = []
            with open(pdf_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
            return "\n\n".join(text_content)
        except Exception as e:
            raise Exception(f"Error extracting text with PyPDF2: {str(e)}")
    
    @staticmethod
    def extract_text(pdf_path: str, method: str = "pdfplumber") -> str:
        """
        Extract text from PDF using specified method
        
        Args:
            pdf_path: Path to the PDF file
            method: Extraction method ('pdfplumber' or 'pypdf2')
            
        Returns:
            Extracted text content
        """
        if method == "pdfplumber":
            try:
                return PDFService.extract_text_pdfplumber(pdf_path)
            except:
                # Fallback to PyPDF2 if pdfplumber fails
                return PDFService.extract_text_pypdf2(pdf_path)
        else:
            return PDFService.extract_text_pypdf2(pdf_path)
    
    @staticmethod
    def get_page_count(pdf_path: str) -> int:
        """
        Get the number of pages in a PDF
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Number of pages
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                return len(pdf_reader.pages)
        except Exception as e:
            raise Exception(f"Error getting page count: {str(e)}")
