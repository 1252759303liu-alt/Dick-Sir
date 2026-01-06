"""OCR text recognition service"""
import pytesseract
from PIL import Image
from typing import Optional


class OCRService:
    """Service for extracting text from images using OCR"""
    
    @staticmethod
    def extract_text(image_path: str, language: str = "eng") -> str:
        """
        Extract text from image using Tesseract OCR
        
        Args:
            image_path: Path to the image file
            language: OCR language (default: 'eng', use 'chi_sim' for Chinese)
            
        Returns:
            Extracted text content
        """
        try:
            image = Image.open(image_path)
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Perform OCR
            text = pytesseract.image_to_string(image, lang=language)
            return text.strip()
        except Exception as e:
            raise Exception(f"Error performing OCR: {str(e)}")
    
    @staticmethod
    def extract_text_with_config(
        image_path: str,
        language: str = "eng",
        config: str = ""
    ) -> str:
        """
        Extract text from image with custom Tesseract configuration
        
        Args:
            image_path: Path to the image file
            language: OCR language
            config: Custom Tesseract configuration string
            
        Returns:
            Extracted text content
        """
        try:
            image = Image.open(image_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            text = pytesseract.image_to_string(image, lang=language, config=config)
            return text.strip()
        except Exception as e:
            raise Exception(f"Error performing OCR with config: {str(e)}")
    
    @staticmethod
    def is_tesseract_available() -> bool:
        """
        Check if Tesseract is installed and available
        
        Returns:
            True if Tesseract is available, False otherwise
        """
        try:
            pytesseract.get_tesseract_version()
            return True
        except:
            return False
