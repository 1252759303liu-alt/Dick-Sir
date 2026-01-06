"""
Textbook Reading Assistant - Main FastAPI Application
教科书阅读助手
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
import shutil
from pathlib import Path
import json
from datetime import datetime

from backend.config import Config
from backend.services.pdf_service import PDFService
from backend.services.ocr_service import OCRService
from backend.services.ai_service import AIService
from backend.services.chapter_service import ChapterService

# Initialize FastAPI app
app = FastAPI(
    title="Textbook Reading Assistant",
    description="智能教科书阅读助手 - 使用DeepSeek V3提供AI分析和总结",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Ensure directories exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)

# Initialize services
pdf_service = PDFService()
ocr_service = OCRService()
ai_service = None

# Initialize AI service only if API key is set
try:
    if Config.DEEPSEEK_API_KEY and Config.DEEPSEEK_API_KEY != "your_api_key_here":
        ai_service = AIService(Config.DEEPSEEK_API_KEY, Config.DEEPSEEK_API_BASE)
except Exception as e:
    print(f"Warning: AI service not initialized - {str(e)}")


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    return FileResponse("frontend/index.html")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "ai_service": ai_service is not None,
        "ocr_available": OCRService.is_tesseract_available()
    }


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload PDF or image file
    
    Args:
        file: The uploaded file
        
    Returns:
        JSON with file info and extracted text
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(Config.ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size
    file_content = await file.read()
    if len(file_content) > Config.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {Config.MAX_FILE_SIZE_MB}MB"
        )
    
    # Save file
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    # Extract text based on file type
    file_ext = filename.rsplit('.', 1)[1].lower()
    try:
        if file_ext == 'pdf':
            text = pdf_service.extract_text(file_path)
            page_count = pdf_service.get_page_count(file_path)
            file_info = {"type": "pdf", "pages": page_count}
        else:
            # Image file - use OCR
            if not OCRService.is_tesseract_available():
                raise HTTPException(
                    status_code=500,
                    detail="OCR service not available. Please install Tesseract."
                )
            text = ocr_service.extract_text(file_path)
            file_info = {"type": "image"}
        
        return {
            "success": True,
            "filename": filename,
            "file_path": file_path,
            "text": text,
            "text_length": len(text),
            "file_info": file_info
        }
    except Exception as e:
        # Clean up file on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.post("/api/analyze-chapters")
async def analyze_chapters(text: str = Form(...)):
    """
    Analyze text and identify chapter structure
    
    Args:
        text: The text content to analyze
        
    Returns:
        JSON with chapter structure
    """
    try:
        chapters = ChapterService.identify_chapters(text)
        chapter_tree = ChapterService.build_chapter_tree(chapters)
        
        return {
            "success": True,
            "chapters": chapters,
            "chapter_tree": chapter_tree,
            "total_chapters": len(chapters)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing chapters: {str(e)}")


@app.post("/api/summarize-chapter")
async def summarize_chapter(
    chapter_text: str = Form(...),
    chapter_title: str = Form(...)
):
    """
    Generate detailed summary for a chapter using DeepSeek API
    
    Args:
        chapter_text: The chapter content
        chapter_title: The chapter title
        
    Returns:
        JSON with chapter summary
    """
    if not ai_service:
        raise HTTPException(
            status_code=503,
            detail="AI service not available. Please configure DEEPSEEK_API_KEY in .env file."
        )
    
    try:
        summary = ai_service.summarize_chapter(chapter_text, chapter_title)
        
        # Save summary to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_title = "".join(c for c in chapter_title if c.isalnum() or c in (' ', '-', '_'))[:50]
        summary_filename = f"{timestamp}_{safe_title}.md"
        summary_path = os.path.join(Config.OUTPUT_FOLDER, summary_filename)
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"# {chapter_title}\n\n{summary}")
        
        return {
            "success": True,
            "summary": summary,
            "summary_file": summary_filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")


@app.post("/api/ask-question")
async def ask_question(
    question: str = Form(...),
    context: str = Form(...),
    chapter_title: str = Form(default="")
):
    """
    Answer questions based on chapter content
    
    Args:
        question: User's question
        context: Chapter content or relevant context
        chapter_title: Optional chapter title
        
    Returns:
        JSON with answer
    """
    if not ai_service:
        raise HTTPException(
            status_code=503,
            detail="AI service not available. Please configure DEEPSEEK_API_KEY in .env file."
        )
    
    try:
        answer = ai_service.answer_question(question, context, chapter_title)
        
        return {
            "success": True,
            "question": question,
            "answer": answer,
            "chapter_title": chapter_title
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")


@app.get("/api/summaries")
async def list_summaries():
    """
    List all saved summaries
    
    Returns:
        JSON with list of summary files
    """
    try:
        summaries = []
        output_path = Path(Config.OUTPUT_FOLDER)
        
        for file_path in output_path.glob("*.md"):
            stat = file_path.stat()
            summaries.append({
                "filename": file_path.name,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "size": stat.st_size
            })
        
        summaries.sort(key=lambda x: x['created'], reverse=True)
        
        return {
            "success": True,
            "summaries": summaries
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing summaries: {str(e)}")


@app.get("/api/summary/{filename}")
async def get_summary(filename: str):
    """
    Get content of a saved summary
    
    Args:
        filename: Name of the summary file
        
    Returns:
        File download response
    """
    file_path = os.path.join(Config.OUTPUT_FOLDER, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Summary not found")
    
    return FileResponse(
        file_path,
        media_type="text/markdown",
        filename=filename
    )


if __name__ == "__main__":
    import uvicorn
    
    # Validate configuration
    try:
        if Config.DEEPSEEK_API_KEY == "your_api_key_here":
            print("\n" + "="*60)
            print("WARNING: DeepSeek API Key not configured!")
            print("="*60)
            print("Please copy .env.example to .env and add your API key.")
            print("AI features will be disabled until configured.")
            print("="*60 + "\n")
    except ValueError as e:
        print(f"\nConfiguration Error: {e}\n")
    
    uvicorn.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        log_level="info"
    )
