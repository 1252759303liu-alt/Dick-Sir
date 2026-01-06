# Development Guide

## Project Architecture

### Backend (FastAPI)

```
backend/
├── app.py                 # Main FastAPI application with endpoints
├── config.py             # Configuration management
├── services/             # Business logic layer
│   ├── pdf_service.py    # PDF text extraction
│   ├── ocr_service.py    # OCR image processing
│   ├── ai_service.py     # DeepSeek API integration
│   └── chapter_service.py # Chapter structure recognition
└── utils/
    └── text_processor.py # Text processing utilities
```

### Frontend

```
frontend/
├── index.html           # Main HTML page
├── css/
│   └── style.css       # Custom styles
└── js/
    ├── app.js          # Main application logic
    └── upload.js       # File upload handling
```

## API Endpoints

### File Upload
- **POST** `/api/upload`
  - Accepts PDF or image files
  - Returns extracted text and file information

### Chapter Analysis
- **POST** `/api/analyze-chapters`
  - Analyzes text and identifies chapter structure
  - Returns chapter tree and metadata

### AI Summarization
- **POST** `/api/summarize-chapter`
  - Generates detailed chapter summary using DeepSeek V3
  - Returns markdown-formatted summary

### Q&A
- **POST** `/api/ask-question`
  - Answers questions based on chapter content
  - Supports context-aware conversation

### Summaries Management
- **GET** `/api/summaries` - List all saved summaries
- **GET** `/api/summary/{filename}` - Download specific summary

### Health Check
- **GET** `/health` - Check service status

## Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/1252759303liu-alt/Dick-Sir.git
cd Dick-Sir
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your DeepSeek API key
```

5. **Run in development mode**
```bash
python -m backend.app
```

## Code Style

- Python: Follow PEP 8 guidelines
- JavaScript: Use consistent indentation (2 spaces)
- Comments: Write clear, concise comments for complex logic

## Security Considerations

### Implemented Security Features

1. **Path Traversal Protection**
   - Validates all file paths
   - Prevents directory traversal attacks

2. **Content Security Policy**
   - Strict CSP headers to prevent XSS
   - Configured in `SecurityHeadersMiddleware`

3. **Input Validation**
   - File type validation
   - File size limits
   - Filename sanitization

4. **API Key Protection**
   - Environment variables only
   - Never committed to repository
   - .gitignore configured

### Best Practices

- Always validate user input
- Use parameterized queries if adding database support
- Keep dependencies up to date
- Regular security audits with `pip-audit`

## Testing

### Manual Testing

1. **Upload Test**
   - Upload a PDF file
   - Upload an image file
   - Verify text extraction

2. **Chapter Recognition**
   - Test with various chapter formats
   - Verify tree structure

3. **AI Features** (requires API key)
   - Test chapter summarization
   - Test Q&A functionality

### Running Health Check
```bash
curl http://localhost:8000/health
```

## Performance Optimization

### Current Optimizations

1. **Pre-compiled Regex Patterns**
   - Chapter patterns compiled at class level
   - Avoid recompilation on each use

2. **Chunked File Upload**
   - Memory-efficient file handling
   - Supports large files up to 50MB

3. **Async I/O**
   - FastAPI async endpoints
   - Non-blocking file operations

### Future Improvements

- [ ] Add caching for chapter analysis
- [ ] Implement rate limiting
- [ ] Add database for persistent storage
- [ ] WebSocket support for real-time updates

## Troubleshooting

### Common Issues

**Port 8000 already in use**
```bash
# Find process using port 8000
lsof -i :8000  # On Linux/macOS
netstat -ano | findstr :8000  # On Windows

# Kill the process or use a different port
# Edit backend/.env: PORT=8001
```

**Tesseract not found**
```bash
# Install Tesseract OCR
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim

# macOS
brew install tesseract tesseract-lang

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

**API Key not configured**
- Ensure `.env` file exists in `backend/` directory
- Verify `DEEPSEEK_API_KEY` is set correctly
- Restart the application

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Commit Message Format
```
<type>: <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat: Add support for DOCX file upload

- Implement DOCX text extraction
- Add file type validation
- Update UI to show DOCX support
```

## License

MIT License - see LICENSE file for details

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [DeepSeek API](https://platform.deepseek.com/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
