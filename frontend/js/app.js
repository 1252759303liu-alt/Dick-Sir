/**
 * Main Application Module
 * Handles chapter viewing, summarization, and Q&A functionality
 */

// Global state
const AppState = {
    chapters: [],
    currentChapter: null,
    currentChapterIndex: -1,
    fullText: ''
};

// Chapter Viewer Module
const ChapterViewer = {
    chapterTree: null,
    originalContent: null,
    summaryContent: null,
    summaryText: null,
    showOriginalBtn: null,
    showSummaryBtn: null,
    generateSummaryBtn: null,
    
    init() {
        this.chapterTree = document.getElementById('chapterTree');
        this.originalContent = document.getElementById('originalContent');
        this.summaryContent = document.getElementById('summaryContent');
        this.summaryText = document.getElementById('summaryText');
        this.showOriginalBtn = document.getElementById('showOriginalBtn');
        this.showSummaryBtn = document.getElementById('showSummaryBtn');
        this.generateSummaryBtn = document.getElementById('generateSummaryBtn');
        
        this.attachEventListeners();
    },
    
    attachEventListeners() {
        this.showOriginalBtn.addEventListener('click', () => {
            this.showOriginal();
        });
        
        this.showSummaryBtn.addEventListener('click', () => {
            this.showSummary();
        });
        
        this.generateSummaryBtn.addEventListener('click', () => {
            this.generateSummary();
        });
    },
    
    async analyzeChapters(text) {
        AppState.fullText = text;
        showLoading('分析章节结构...');
        
        try {
            const formData = new FormData();
            formData.append('text', text);
            
            const response = await fetch('/api/analyze-chapters', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('章节分析失败');
            }
            
            const result = await response.json();
            AppState.chapters = result.chapters;
            
            this.renderChapterTree(result.chapters);
            
            // Show chapters section
            document.getElementById('chapters-section').style.display = 'block';
            document.getElementById('qa-section').style.display = 'block';
            
            // Populate Q&A chapter selector
            if (window.QAModule) {
                window.QAModule.populateChapterSelector(result.chapters);
            }
            
            hideLoading();
            showNotification(`成功识别 ${result.total_chapters} 个章节`, 'success');
            
        } catch (error) {
            hideLoading();
            showNotification('章节分析失败: ' + error.message, 'danger');
        }
    },
    
    renderChapterTree(chapters) {
        this.chapterTree.innerHTML = '';
        
        chapters.forEach((chapter, index) => {
            const chapterItem = document.createElement('div');
            chapterItem.className = 'chapter-item';
            chapterItem.dataset.index = index;
            
            const title = document.createElement('div');
            title.className = 'chapter-title';
            title.textContent = chapter.title;
            
            chapterItem.appendChild(title);
            
            chapterItem.addEventListener('click', () => {
                this.selectChapter(index);
            });
            
            this.chapterTree.appendChild(chapterItem);
        });
    },
    
    selectChapter(index) {
        AppState.currentChapterIndex = index;
        AppState.currentChapter = AppState.chapters[index];
        
        // Update active state
        const items = this.chapterTree.querySelectorAll('.chapter-item');
        items.forEach(item => item.classList.remove('active'));
        items[index].classList.add('active');
        
        // Show original content
        this.showOriginal();
        this.originalContent.textContent = AppState.currentChapter.content;
        
        // Clear previous summary
        this.summaryText.innerHTML = '';
    },
    
    showOriginal() {
        this.originalContent.style.display = 'block';
        this.summaryContent.style.display = 'none';
        this.showOriginalBtn.classList.add('active');
        this.showSummaryBtn.classList.remove('active');
    },
    
    showSummary() {
        this.originalContent.style.display = 'none';
        this.summaryContent.style.display = 'block';
        this.showOriginalBtn.classList.remove('active');
        this.showSummaryBtn.classList.add('active');
    },
    
    async generateSummary() {
        if (!AppState.currentChapter) {
            showNotification('请先选择一个章节', 'warning');
            return;
        }
        
        showLoading('生成AI总结中，请稍候...');
        
        try {
            const formData = new FormData();
            formData.append('chapter_text', AppState.currentChapter.content);
            formData.append('chapter_title', AppState.currentChapter.title);
            
            const response = await fetch('/api/summarize-chapter', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || '生成总结失败');
            }
            
            const result = await response.json();
            
            // Render markdown summary
            this.summaryText.innerHTML = marked.parse(result.summary);
            
            hideLoading();
            showNotification('总结生成成功！', 'success');
            
        } catch (error) {
            hideLoading();
            showNotification('生成总结失败: ' + error.message, 'danger');
        }
    }
};

// Q&A Module
const QAModule = {
    qaChapterSelect: null,
    questionInput: null,
    askQuestionBtn: null,
    historyContent: null,
    conversationHistory: [],
    
    init() {
        this.qaChapterSelect = document.getElementById('qaChapterSelect');
        this.questionInput = document.getElementById('questionInput');
        this.askQuestionBtn = document.getElementById('askQuestionBtn');
        this.historyContent = document.getElementById('historyContent');
        
        this.attachEventListeners();
    },
    
    attachEventListeners() {
        this.askQuestionBtn.addEventListener('click', () => {
            this.askQuestion();
        });
        
        this.questionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.askQuestion();
            }
        });
    },
    
    populateChapterSelector(chapters) {
        this.qaChapterSelect.innerHTML = '<option value="">全部内容</option>';
        
        chapters.forEach((chapter, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = chapter.title;
            this.qaChapterSelect.appendChild(option);
        });
    },
    
    async askQuestion() {
        const question = this.questionInput.value.trim();
        
        if (!question) {
            showNotification('请输入问题', 'warning');
            return;
        }
        
        const selectedChapterIndex = this.qaChapterSelect.value;
        let context = AppState.fullText;
        let chapterTitle = '';
        
        if (selectedChapterIndex !== '') {
            const chapter = AppState.chapters[parseInt(selectedChapterIndex)];
            context = chapter.content;
            chapterTitle = chapter.title;
        }
        
        showLoading('AI思考中...');
        
        try {
            const formData = new FormData();
            formData.append('question', question);
            formData.append('context', context);
            formData.append('chapter_title', chapterTitle);
            
            const response = await fetch('/api/ask-question', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || '回答问题失败');
            }
            
            const result = await response.json();
            
            // Add to conversation history
            this.conversationHistory.push({
                question: question,
                answer: result.answer,
                chapter: chapterTitle || '全部内容'
            });
            
            this.renderConversation();
            
            // Clear question input
            this.questionInput.value = '';
            
            hideLoading();
            showNotification('回答已生成', 'success');
            
        } catch (error) {
            hideLoading();
            showNotification('回答失败: ' + error.message, 'danger');
        }
    },
    
    renderConversation() {
        this.historyContent.innerHTML = '';
        
        this.conversationHistory.forEach((item, index) => {
            // Question
            const questionDiv = document.createElement('div');
            questionDiv.className = 'qa-message qa-question fade-in';
            questionDiv.innerHTML = `
                <span class="qa-label">问题 ${index + 1}:</span>
                <div>${escapeHtml(item.question)}</div>
                ${item.chapter ? `<small class="text-muted">章节: ${escapeHtml(item.chapter)}</small>` : ''}
            `;
            this.historyContent.appendChild(questionDiv);
            
            // Answer
            const answerDiv = document.createElement('div');
            answerDiv.className = 'qa-message qa-answer fade-in';
            answerDiv.innerHTML = `
                <span class="qa-label">回答:</span>
                <div>${marked.parse(item.answer)}</div>
            `;
            this.historyContent.appendChild(answerDiv);
        });
        
        // Scroll to bottom
        this.historyContent.scrollTop = this.historyContent.scrollHeight;
    }
};

// Utility Functions
function showLoading(message = '处理中...') {
    document.getElementById('loadingText').textContent = message;
    const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
    modal.show();
}

function hideLoading() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
    if (modal) {
        modal.hide();
    }
}

function showNotification(message, type = 'info') {
    const toast = document.getElementById('notificationToast');
    const toastMessage = document.getElementById('toastMessage');
    
    toastMessage.textContent = message;
    
    // Set toast color based on type
    toast.className = 'toast';
    if (type === 'success') {
        toast.classList.add('bg-success', 'text-white');
    } else if (type === 'danger') {
        toast.classList.add('bg-danger', 'text-white');
    } else if (type === 'warning') {
        toast.classList.add('bg-warning');
    } else {
        toast.classList.add('bg-info', 'text-white');
    }
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize modules
document.addEventListener('DOMContentLoaded', () => {
    ChapterViewer.init();
    QAModule.init();
    
    // Make modules globally accessible
    window.ChapterViewer = ChapterViewer;
    window.QAModule = QAModule;
});
