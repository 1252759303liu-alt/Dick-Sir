/**
 * File Upload Module
 * Handles file upload functionality with drag-and-drop support
 */

const FileUploader = {
    uploadArea: null,
    fileInput: null,
    selectFileBtn: null,
    progressContainer: null,
    uploadProgress: null,
    progressText: null,
    fileInfo: null,
    fileDetails: null,
    
    currentFile: null,
    uploadedText: null,
    
    init() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.selectFileBtn = document.getElementById('selectFileBtn');
        this.progressContainer = document.getElementById('progressContainer');
        this.uploadProgress = document.getElementById('uploadProgress');
        this.progressText = document.getElementById('progressText');
        this.fileInfo = document.getElementById('fileInfo');
        this.fileDetails = document.getElementById('fileDetails');
        
        this.attachEventListeners();
    },
    
    attachEventListeners() {
        // Click to select file
        this.selectFileBtn.addEventListener('click', () => {
            this.fileInput.click();
        });
        
        this.uploadArea.addEventListener('click', (e) => {
            if (e.target === this.uploadArea || e.target.closest('.upload-icon, .upload-text, .upload-info')) {
                this.fileInput.click();
            }
        });
        
        // File input change
        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFile(e.target.files[0]);
            }
        });
        
        // Drag and drop
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });
        
        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.classList.remove('dragover');
        });
        
        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            
            if (e.dataTransfer.files.length > 0) {
                this.handleFile(e.dataTransfer.files[0]);
            }
        });
    },
    
    handleFile(file) {
        // Validate file type
        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
        if (!allowedTypes.includes(file.type)) {
            showNotification('文件类型不支持！请上传 PDF、JPG 或 PNG 文件。', 'danger');
            return;
        }
        
        // Validate file size (50MB)
        const maxSize = 50 * 1024 * 1024;
        if (file.size > maxSize) {
            showNotification('文件太大！最大支持 50MB。', 'danger');
            return;
        }
        
        this.currentFile = file;
        this.uploadFile(file);
    },
    
    async uploadFile(file) {
        // Show progress
        this.progressContainer.style.display = 'block';
        this.fileInfo.style.display = 'none';
        this.uploadProgress.style.width = '0%';
        this.progressText.textContent = '上传中...';
        
        // Create form data
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            // Simulate progress
            let progress = 0;
            const progressInterval = setInterval(() => {
                if (progress < 90) {
                    progress += 10;
                    this.uploadProgress.style.width = progress + '%';
                }
            }, 100);
            
            // Upload file
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            clearInterval(progressInterval);
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || '上传失败');
            }
            
            const result = await response.json();
            
            // Complete progress
            this.uploadProgress.style.width = '100%';
            this.progressText.textContent = '上传完成！';
            
            // Store uploaded data
            this.uploadedText = result.text;
            
            // Show file info
            setTimeout(() => {
                this.progressContainer.style.display = 'none';
                this.fileInfo.style.display = 'block';
                
                let details = `文件名: ${file.name}<br>`;
                details += `大小: ${(file.size / 1024).toFixed(2)} KB<br>`;
                details += `文本长度: ${result.text_length} 字符`;
                
                if (result.file_info.pages) {
                    details += `<br>页数: ${result.file_info.pages}`;
                }
                
                this.fileDetails.innerHTML = details;
                
                showNotification('文件上传成功！', 'success');
                
                // Trigger chapter analysis
                if (window.ChapterViewer) {
                    window.ChapterViewer.analyzeChapters(result.text);
                }
            }, 500);
            
        } catch (error) {
            this.progressContainer.style.display = 'none';
            showNotification('上传失败: ' + error.message, 'danger');
        }
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    FileUploader.init();
});
