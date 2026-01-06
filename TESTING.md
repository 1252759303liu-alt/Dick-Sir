# Testing Guide

This guide helps you test the Textbook Reading Assistant application.

## Prerequisites

- Python 3.9+ installed
- DeepSeek API key configured in `.env`
- (Optional) Tesseract OCR for image processing

## Quick Test

### 1. Start the Application

```bash
# Linux/macOS
./start.sh

# Windows
start.bat

# Or manually
cd backend
python -m backend.app
```

### 2. Access the Application

Open your browser and visit: http://localhost:8000

You should see:
- Navigation bar with "教科书阅读助手"
- Upload section with drag-and-drop area
- Navigation links: 上传, 章节, 问答

### 3. Test Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "ai_service": true,    # false if API key not configured
  "ocr_available": false  # true if Tesseract installed
}
```

## Feature Testing

### Test 1: PDF Upload (Without AI)

**Purpose:** Test PDF text extraction

1. Find a simple PDF file (or create one)
2. Click "选择文件" or drag PDF to upload area
3. Wait for upload to complete
4. Check that:
   - ✅ File info shows: filename, size, page count
   - ✅ Text is extracted and displayed
   - ✅ Chapter section appears
   - ✅ Chapter tree shows identified chapters

**Sample Test PDF:**
Create a simple PDF with this content:
```
第一章：测试章节

这是测试内容。

第二章：另一个章节

更多测试内容。
```

### Test 2: Image Upload (Requires Tesseract)

**Purpose:** Test OCR functionality

1. Create a simple image with text or screenshot a page
2. Upload the image
3. Check that:
   - ✅ OCR extracts text from image
   - ✅ Text appears in chapter analysis

**Note:** If Tesseract is not installed, you'll get an error message.

### Test 3: Chapter Recognition

**Purpose:** Test chapter structure analysis

Test with different chapter formats:

**Chinese Format:**
```
第一章：标题
第一节：小节
```

**English Format:**
```
Chapter 1: Introduction
Chapter 2: Main Content
```

**Numeric Format:**
```
1. First Section
1.1 Subsection
2. Second Section
```

### Test 4: AI Summarization (Requires API Key)

**Purpose:** Test DeepSeek V3 integration

1. Upload a PDF with clear chapter structure
2. Click on a chapter in the tree
3. Switch to "总结" view
4. Click "生成AI总结"
5. Check that:
   - ✅ Loading modal appears
   - ✅ Summary generates successfully
   - ✅ Summary includes:
     - Main content overview
     - Key concepts
     - Important points
     - Difficulty explanations
     - Learning suggestions
   - ✅ Summary is formatted in Markdown

**Expected Summary Format:**
```markdown
## 主要内容概述
...

## 关键概念
1. Concept 1
2. Concept 2

## 重点知识点
...

## 难点解析
...

## 学习建议
...
```

### Test 5: Q&A Feature (Requires API Key)

**Purpose:** Test intelligent question answering

1. Upload and analyze a document
2. Navigate to Q&A section
3. (Optional) Select a specific chapter
4. Ask a question like: "这个章节的主要内容是什么？"
5. Click "提问"
6. Check that:
   - ✅ Answer generates successfully
   - ✅ Answer is relevant to the content
   - ✅ Conversation history shows question and answer
   - ✅ Can ask follow-up questions

### Test 6: File Size Limits

**Purpose:** Test file validation

1. Try uploading a file > 50MB
2. Expected: Error message "文件太大！最大支持 50MB"

### Test 7: File Type Validation

**Purpose:** Test file type restrictions

1. Try uploading a .txt, .docx, or other unsupported file
2. Expected: Error message about unsupported file type

### Test 8: Summary Export

**Purpose:** Test summary saving and retrieval

1. Generate a summary
2. Check `outputs/` folder for .md file
3. Download the summary via API:
   ```bash
   curl http://localhost:8000/api/summaries
   ```

## API Testing

### Using curl

**1. Upload File**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/path/to/test.pdf"
```

**2. Analyze Chapters**
```bash
curl -X POST http://localhost:8000/api/analyze-chapters \
  -d "text=第一章：测试\n内容内容内容"
```

**3. Generate Summary** (Requires API key)
```bash
curl -X POST http://localhost:8000/api/summarize-chapter \
  -d "chapter_title=第一章：测试" \
  -d "chapter_text=这是测试内容"
```

**4. Ask Question** (Requires API key)
```bash
curl -X POST http://localhost:8000/api/ask-question \
  -d "question=这是什么？" \
  -d "context=这是一本关于Python的教科书" \
  -d "chapter_title=第一章"
```

## Browser Testing

### Supported Browsers
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Test Responsive Design
1. Open browser dev tools (F12)
2. Toggle device toolbar
3. Test on different screen sizes:
   - Mobile (375px)
   - Tablet (768px)
   - Desktop (1920px)

## Performance Testing

### File Upload Speed
- Small file (1MB): < 2 seconds
- Medium file (10MB): < 10 seconds
- Large file (50MB): < 30 seconds

### Chapter Analysis Speed
- 10 chapters: < 5 seconds
- 50 chapters: < 15 seconds

### AI Response Time
- Summary generation: 30-60 seconds
- Q&A response: 10-30 seconds

## Troubleshooting Tests

### Test Error Handling

1. **No API Key**
   - Try using AI features without API key
   - Expected: Error message about missing configuration

2. **Invalid API Key**
   - Set invalid API key in `.env`
   - Expected: API call error message

3. **Network Error**
   - Disconnect internet
   - Try AI features
   - Expected: Timeout error message

4. **Large File**
   - Upload 51MB file
   - Expected: File size error

## Security Testing

### Test Path Traversal Protection
```bash
# This should fail with "Invalid filename" error
curl http://localhost:8000/api/summary/../../../etc/passwd
```

### Test XSS Protection
1. Upload file with malicious content: `<script>alert('XSS')</script>`
2. Check that content is properly escaped in UI
3. Verify CSP headers prevent script execution

### Test File Upload Security
1. Try uploading .exe, .sh files
2. Expected: File type rejection

## Acceptance Criteria

✅ All core features work as expected
✅ No security vulnerabilities
✅ Error messages are clear and helpful
✅ UI is responsive and user-friendly
✅ API responses are fast (< 60s for AI features)
✅ Files are properly validated
✅ No crashes or unhandled exceptions

## Reporting Issues

If you find any bugs:
1. Check the browser console for errors (F12)
2. Check the server logs
3. Note the steps to reproduce
4. Create a GitHub issue with details

## Test Results Template

```
Environment:
- OS: 
- Python Version: 
- Browser: 

Test Results:
[ ] PDF Upload
[ ] Image Upload (OCR)
[ ] Chapter Recognition
[ ] AI Summarization
[ ] Q&A Feature
[ ] File Validation
[ ] Security Tests

Issues Found:
- 

Notes:
- 
```
