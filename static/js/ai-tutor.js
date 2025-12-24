// 模块切换按钮事件绑定
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('btn-chat').onclick = () => switchModule('chat');
    document.getElementById('btn-history').onclick = () => switchModule('history');
    document.getElementById('btn-faq').onclick = () => switchModule('faq');
    document.getElementById('send-btn').onclick = sendQuestion;

    // 初始化显示智能对话模块
    switchModule('chat');
});

// 切换模块函数
function switchModule(type) {
    // 更新导航按钮状态
    document.querySelectorAll('.top-nav button').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`btn-${type}`).classList.add('active');

    // 显示/隐藏对应模块
    document.querySelector('.chat-area').style.display = type === 'chat' ? 'block' : 'none';
    document.querySelector('.input-area').style.display = type === 'chat' ? 'flex' : 'none';
    document.querySelector('.history-area').style.display = type === 'history' ? 'block' : 'none';
    document.querySelector('.faq-area').style.display = type === 'faq' ? 'block' : 'none';

    // 根据模块类型加载数据
    if (type === 'history') loadHistory();
    if (type === 'faq') loadFAQ();
}

// 发送问题函数
async function sendQuestion() {
    const question = document.getElementById('question').value.trim();
    if (!question) return;

    const studentId = 'default'; // 实际应用中应替换为当前登录学生的ID
    const chatArea = document.getElementById('chat-area');
    // 生成唯一的会话ID
    const sessionId = 'session-' + Date.now();

    // 显示问题
    chatArea.innerHTML += `
        <div class="message user">
            <div class="message-content">
                ${question}
            </div>
        </div>
    `;

    // 清空输入框
    document.getElementById('question').value = '';
    // 滚动到对话底部
    chatArea.scrollTop = chatArea.scrollHeight;

    // 移除思考过程展示，直接显示回答

    // 创建AI回答元素
    const answerId = 'answer-' + Date.now();
    const loadingId = 'loading-' + Date.now();
    let aiAnswerElement = document.createElement('div');
    aiAnswerElement.className = 'message ai';
    aiAnswerElement.innerHTML = `
        <div class="message-header">AI助教</div>
        <div class="message-content">
            <div class="typing-indicator" id="${loadingId}">
                <div class="loading-indicator"></div>
                <span>AI正在思考中...</span>
            </div>
            <span class="answer-content" id="${answerId}" style="display: none;"></span>
        </div>
    `;
    chatArea.appendChild(aiAnswerElement);
    chatArea.scrollTop = chatArea.scrollHeight;

    let fullAnswer = '';

    // 使用SSE调用后端API
    const eventSource = new EventSource(`/api/ai-tutor/chat?${new URLSearchParams({question: question})}`);

    // 处理流式响应
    eventSource.onmessage = function(event) {
        if (event.data === '[DONE]') {
            // 关闭连接
            eventSource.close();
            
            // 保存对话记录
            saveConversation(question, fullAnswer, sessionId);
            return;
        }

        try {
            const data = JSON.parse(event.data);
            const answerSpan = document.getElementById(answerId);
            const loadingIndicator = document.getElementById(loadingId);
            const messageContent = answerSpan.parentNode;

            if (data.type === 'thinking') {
                // 第一次收到思考内容时，隐藏加载指示器并显示思考内容
                if (loadingIndicator && answerSpan.style.display === 'none') {
                    loadingIndicator.style.display = 'none';
                    // 添加思考样式类
                    messageContent.classList.add('thinking');
                    answerSpan.style.display = 'block';
                }
                // 显示思考过程（灰色文本）
                answerSpan.textContent += data.content + ' ';
                chatArea.scrollTop = chatArea.scrollHeight;
            } else if (data.type === 'answer') {
                // 第一次收到回答内容时，隐藏加载指示器并显示回答内容
                if (loadingIndicator && answerSpan.style.display === 'none') {
                    loadingIndicator.style.display = 'none';
                    answerSpan.style.display = 'block';
                }
                // 追加回答内容
                answerSpan.textContent += data.content;
                fullAnswer += data.content;
                chatArea.scrollTop = chatArea.scrollHeight;
            } else if (data.type === 'error') {
                // 处理错误类型的事件
                if (loadingIndicator && answerSpan.style.display === 'none') {
                    loadingIndicator.style.display = 'none';
                    answerSpan.style.display = 'block';
                }
                // 添加错误样式类
                messageContent.classList.add('error');
                // 显示错误信息
                answerSpan.textContent = data.content;
                fullAnswer = data.content; // 设置一个非空的回答内容，避免保存对话失败
                chatArea.scrollTop = chatArea.scrollHeight;
            }
        } catch (error) {
            console.error('解析SSE数据失败:', error);
        }
    };

    // 处理错误
    eventSource.onerror = function(error) {
        console.error('SSE连接错误:', error);
        console.error('错误详情:', {type: error.type, target: error.target, readyState: eventSource.readyState});
        
        // 获取更详细的错误信息
            let errorMessage = 'AI回答出错，请稍后重试。';
            const answerContent = aiAnswerElement.querySelector('.message-content');
            
            // 检查是否是401未登录错误
            if (error.target.readyState === EventSource.CLOSED) {
                // 创建一个临时请求来检查实际错误状态
                fetch(`/api/ai-tutor/chat?${new URLSearchParams({question: '测试'})}`, {
                    method: 'GET',
                    credentials: 'same-origin'
                }).then(response => {
                    if (response.status === 401) {
                    errorMessage = '会话已过期，请重新登录后再试。';
                    // 可以选择自动跳转到登录页
                    // setTimeout(() => window.location.href = '/login', 3000);
                }
                answerContent.classList.add('error');
                answerContent.innerHTML = `<span id="ai-answer">${errorMessage}</span>`;
                
                // 设置fullAnswer为错误信息，确保保存对话时不为空
                fullAnswer = errorMessage;
                // 保存对话记录
                saveConversation(question, fullAnswer, sessionId);
            }).catch(() => {
                answerContent.classList.add('error');
                answerContent.innerHTML = `<span id="ai-answer">${errorMessage}</span>`;
                
                // 设置fullAnswer为错误信息，确保保存对话时不为空
                fullAnswer = errorMessage;
                // 保存对话记录
                saveConversation(question, fullAnswer, sessionId);
            });
        } else {
            answerContent.classList.add('error');
            answerContent.innerHTML = `<span id="ai-answer">${errorMessage}</span>`;
            
            // 设置fullAnswer为错误信息，确保保存对话时不为空
            fullAnswer = errorMessage;
            // 保存对话记录
            saveConversation(question, fullAnswer, sessionId);
        }
        
        // 关闭连接
        eventSource.close();
        chatArea.scrollTop = chatArea.scrollHeight;
    };
}

// 保存对话记录函数
async function saveConversation(question, answer, sessionId) {
    try {
        const response = await fetch('/api/ai-tutor/save-conversation', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                answer: answer,
                session_id: sessionId
            })
        });
        
        const result = await response.json();
        if (!result.success) {
            console.error('保存对话失败:', result.error);
        }
    } catch (error) {
        console.error('保存对话错误:', error);
    }
}

// 加载历史对话
async function loadHistory() {
    const historyArea = document.getElementById('history-area');
    historyArea.innerHTML = '<p>正在加载历史对话...</p>';

    try {
        const response = await fetch('/api/ai-tutor/history', { credentials: 'same-origin' });
        const result = await response.json();
        
        if (result.error) {
            console.error('加载历史对话失败:', result.error);
            historyArea.innerHTML = '<p class="text-danger">加载历史对话失败</p>';
            return;
        }

        const history = result.history;
        let historyHtml = '<h5>历史对话</h5>';
        
        if (history.length === 0) {
            historyHtml += '<p>暂无历史对话</p>';
        } else {
            // 按时间倒序显示（API已经返回倒序数据）
            history.forEach(item => {
                historyHtml += `
                    <div class="card mb-3" style="cursor: pointer;" onclick="loadHistoryConversation('${item.session_id}')">
                        <div class="card-body">
                            <p class="card-text"><strong>Q:</strong> ${item.question}</p>
                            <p class="card-text"><strong>A:</strong> ${item.answer}</p>
                            <p class="card-text text-muted text-sm">${item.time}</p>
                        </div>
                    </div>
                `;
            });
        }

        historyArea.innerHTML = historyHtml;
    } catch (error) {
        console.error('加载历史对话错误:', error);
        historyArea.innerHTML = '<p class="text-danger">加载历史对话失败</p>';
    }
}

// 加载FAQ库（调用真实API）
async function loadFAQ() {
    const faqResults = document.getElementById('faq-results');
    faqResults.innerHTML = '<p>正在加载FAQ...</p>';

    try {
        // 调用获取高频FAQ的API
        const response = await fetch('/api/ai-tutor/faq', { credentials: 'same-origin' });
        const result = await response.json();
        
        if (result.error) {
            console.error('加载FAQ失败:', result.error);
            faqResults.innerHTML = '<p class="text-danger">加载FAQ失败</p>';
            return;
        }

        const faqList = result.faq;
        let faqHtml = '<h5>高频FAQ</h5>';
        
        if (faqList.length === 0) {
            faqHtml += '<p>暂无FAQ数据</p>';
        } else {
            // 按频率从高到低显示
            faqList.forEach(item => {
                faqHtml += `
                    <div class="card mb-3">
                        <div class="card-body">
                            <p class="card-text"><strong>Q:</strong> ${item.question}</p>
                            <p class="card-text"><strong>A:</strong> ${item.answer}</p>
                            <p class="card-text text-muted text-sm">使用次数: ${item.frequency}</p>
                        </div>
                    </div>
                `;
            });
        }

        faqResults.innerHTML = faqHtml;
    } catch (error) {
        console.error('加载FAQ错误:', error);
        faqResults.innerHTML = '<p class="text-danger">加载FAQ失败</p>';
    }

    // 为FAQ搜索框添加事件监听
    const faqSearch = document.getElementById('faq-search');
    faqSearch.oninput = handleFAQSearch;
}

// FAQ搜索函数
async function handleFAQSearch() {
    const faqResults = document.getElementById('faq-results');
    const searchText = this.value.trim();
    
    if (!searchText) {
        // 如果搜索框为空，重新加载所有FAQ
        loadFAQ();
        return;
    }
    
    faqResults.innerHTML = '<p>正在搜索FAQ...</p>';
    
    try {
        // 调用FAQ关键词检索API
        const response = await fetch(`/api/ai-tutor/faq/search?keyword=${encodeURIComponent(searchText)}`, { credentials: 'same-origin' });
        const result = await response.json();
        
        if (result.error) {
            console.error('搜索FAQ失败:', result.error);
            faqResults.innerHTML = '<p class="text-danger">搜索FAQ失败</p>';
            return;
        }
        
        const searchResults = result.faq;
        let faqHtml = `<h5>搜索结果: "${searchText}"</h5>`;
        
        if (searchResults.length === 0) {
            faqHtml += '<p>未找到相关FAQ</p>';
        } else {
            searchResults.forEach(item => {
                faqHtml += `
                    <div class="card mb-3">
                        <div class="card-body">
                            <p class="card-text"><strong>Q:</strong> ${item.question}</p>
                            <p class="card-text"><strong>A:</strong> ${item.answer}</p>
                        </div>
                    </div>
                `;
            });
        }
        
        faqResults.innerHTML = faqHtml;
    } catch (error) {
        console.error('搜索FAQ错误:', error);
        faqResults.innerHTML = '<p class="text-danger">搜索FAQ失败</p>';
    }
}

// 加载历史对话详情
async function loadHistoryConversation(sessionId) {
    // 切换到对话模块
    switchModule('chat');
    
    // 清空对话区域
    const chatArea = document.getElementById('chat-area');
    chatArea.innerHTML = '<p>正在加载对话详情...</p>';
    
    try {
            const response = await fetch(`/api/ai-tutor/history/${sessionId}`, { credentials: 'same-origin' });
            const result = await response.json();
        
        if (result.error) {
            console.error('加载对话详情失败:', result.error);
            chatArea.innerHTML = '<p class="text-danger">加载对话详情失败</p>';
            return;
        }
        
        const conversation = result.conversation;
        chatArea.innerHTML = '';
        
        // 显示历史对话
        conversation.forEach(message => {
            const messageClass = message.role === 'user' ? 'message user' : 'message ai';
            const messageHeader = message.role === 'ai' ? '<div class="message-header">AI助教</div>' : '';
            
            chatArea.innerHTML += `
                <div class="${messageClass}">
                    ${messageHeader}
                    <div class="message-content">
                        ${message.content}
                    </div>
                </div>
            `;
        });
        
        // 滚动到底部
        chatArea.scrollTop = chatArea.scrollHeight;
    } catch (error) {
        console.error('加载对话详情错误:', error);
        chatArea.innerHTML = '<p class="text-danger">加载对话详情失败</p>';
    }
}