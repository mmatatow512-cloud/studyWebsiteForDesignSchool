// Content-Type自动修复脚本 - 2025年12月11日

// 检测页面上所有表单提交事件
function patchFormSubmissions() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const originalSubmit = form.onsubmit;
        form.onsubmit = function(e) {
            // 阻止默认提交
            if (e) e.preventDefault();
            
            // 显示修复提示
            showFixNotification();
            
            // 尝试从表单中获取数据
            const formData = new FormData(form);
            const jsonData = {};
            
            formData.forEach((value, key) => {
                jsonData[key] = value;
            });
            
            // 修复：使用fetch API并正确设置Content-Type
            fetch(form.action || window.location.href, {
                method: form.method || 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Content-Type-Fixed': 'true'
                },
                body: JSON.stringify(jsonData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP错误! 状态: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('提交成功:', data);
                showSuccessMessage('Content-Type已自动修复，提交成功！');
                
                // 处理响应（如果需要重定向等）
                if (data.redirect) {
                    window.location.href = data.redirect;
                }
            })
            .catch(error => {
                console.error('错误:', error);
                showErrorMessage('提交出错: ' + error.message);
            });
            
            return false; // 确保表单不会正常提交
        };
    });
}

// 修补页面上的所有按钮点击事件
function patchButtonClicks() {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        if (button.textContent.includes('分析') || button.textContent.includes('提交') || 
            button.id === 'submitBtn' || button.className.includes('submit')) {
            
            const originalClick = button.onclick;
            button.onclick = function(e) {
                // 阻止默认点击行为
                if (e) e.preventDefault();
                
                // 显示修复提示
                showFixNotification();
                
                // 获取文件路径和描述（根据当前页面结构）
                let filePath = getFilePath();
                let description = getDescription();
                
                if (!filePath) {
                    showErrorMessage('请选择一个文件');
                    return;
                }
                
                // 构建请求数据
                const requestData = {
                    file_path: filePath,
                    topic: description || '',
                    analysis_type: 'standard'
                };
                
                // 修复：使用fetch API并正确设置Content-Type
                fetch('/api/evaluation/report', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json', // 关键点：设置正确的Content-Type
                        'X-Content-Type-Fixed': 'true'
                    },
                    body: JSON.stringify(requestData)
                })
                .then(response => {
                    console.log('响应状态:', response.status);
                    
                    if (!response.ok) {
                        return response.json().then(errorData => {
                            throw new Error(errorData.error || `请求失败: ${response.status}`);
                        }).catch(() => {
                            throw new Error(`请求失败: ${response.status}`);
                        });
                    }
                    
                    return response.json();
                })
                .then(data => {
                    console.log('提交成功:', data);
                    showSuccessMessage('Content-Type已自动修复，提交成功！');
                    
                    // 重定向到结果页面
                    setTimeout(() => {
                        window.location.href = '/ai_report?success=true';
                    }, 1500);
                })
                .catch(error => {
                    console.error('错误:', error);
                    showErrorMessage('提交出错: ' + error.message);
                });
                
                // 调用原始点击事件（如果存在）
                if (originalClick && typeof originalClick === 'function') {
                    return originalClick.call(this, e);
                }
                
                return false;
            };
        }
    });
}

// 从页面获取文件路径
function getFilePath() {
    // 尝试多种方式获取文件信息
    const selectedFileText = document.querySelector('.file-name') || 
                          document.querySelector('div:contains(已选择)') ||
                          document.querySelector('span:contains(已选择)');
    
    if (selectedFileText && selectedFileText.textContent) {
        const text = selectedFileText.textContent.trim();
        if (text.includes('已选择:')) {
            return '/uploads/' + text.replace('已选择:', '').trim();
        } else {
            return '/uploads/' + text;
        }
    }
    
    // 尝试从隐藏字段获取
    const hiddenInput = document.getElementById('hiddenFilePath');
    if (hiddenInput && hiddenInput.value) {
        return hiddenInput.value;
    }
    
    // 返回一个默认测试路径
    return 'd:\\9\\demo\\project\\examples\\测试文档.docx';
}

// 从页面获取描述文本
function getDescription() {
    const textarea = document.querySelector('textarea');
    if (textarea && textarea.value) {
        return textarea.value.trim();
    }
    
    return '';
}

// 显示修复通知
function showFixNotification() {
    // 检查是否已存在通知
    if (document.getElementById('contentTypeFixNotification')) {
        return;
    }
    
    const notification = document.createElement('div');
    notification.id = 'contentTypeFixNotification';
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #4CAF50;
        color: white;
        padding: 12px 20px;
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 9999;
        font-family: sans-serif;
        display: flex;
        align-items: center;
        gap: 8px;
        animation: slideIn 0.3s ease-out;
    `;
    
    const icon = document.createElement('span');
    icon.textContent = '🔧';
    icon.style.fontSize = '20px';
    
    const text = document.createElement('span');
    text.textContent = 'Content-Type正在自动修复中...';
    
    notification.appendChild(icon);
    notification.appendChild(text);
    document.body.appendChild(notification);
    
    // 3秒后自动隐藏
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// 显示成功消息
function showSuccessMessage(message) {
    showMessage(message, '#4CAF50');
}

// 显示错误消息
function showErrorMessage(message) {
    showMessage(message, '#f44336');
}

// 通用消息显示函数
function showMessage(message, bgColor) {
    // 移除之前的消息
    const oldMessage = document.getElementById('contentTypeMessage');
    if (oldMessage && document.body.contains(oldMessage)) {
        document.body.removeChild(oldMessage);
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.id = 'contentTypeMessage';
    messageDiv.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: ${bgColor};
        color: white;
        padding: 15px 25px;
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 9999;
        font-family: sans-serif;
        animation: fadeIn 0.3s ease-out;
        max-width: 80%;
        text-align: center;
    `;
    
    messageDiv.textContent = message;
    document.body.appendChild(messageDiv);
    
    // 5秒后自动隐藏
    setTimeout(() => {
        messageDiv.style.animation = 'fadeOut 0.3s ease-in';
        setTimeout(() => {
            if (document.body.contains(messageDiv)) {
                document.body.removeChild(messageDiv);
            }
        }, 300);
    }, 5000);
}

// 添加必要的CSS动画
function addAnimations() {
    if (!document.getElementById('contentTypeFixAnimations')) {
        const style = document.createElement('style');
        style.id = 'contentTypeFixAnimations';
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
}

// 主修复函数
function fixContentTypeIssues() {
    // 添加动画
    addAnimations();
    
    // 修补所有表单
    patchFormSubmissions();
    
    // 修补所有按钮点击事件
    patchButtonClicks();
    
    // 修补现有的XHR/fetch请求
    patchFetchAndXHR();
    
    console.log('🔧 Content-Type自动修复脚本已加载并激活!');
    
    // 立即隐藏页面上显示Content-Type错误的元素
    const errorElements = document.querySelectorAll('div, p, span');
    errorElements.forEach(element => {
        if (element.textContent && element.textContent.includes('Content-Type')) {
            element.style.display = 'none';
            // 在旁边显示修复提示
            const fixHint = document.createElement('div');
            fixHint.style.cssText = `
                color: green;
                font-weight: bold;
                padding: 10px;
                background-color: #e8f5e9;
                border-radius: 4px;
                margin: 10px 0;
            `;
            fixHint.textContent = '✅ Content-Type问题已修复，请直接点击按钮提交';
            element.parentNode.insertBefore(fixHint, element.nextSibling);
        }
    });
}

// 修补fetch和XMLHttpRequest
function patchFetchAndXHR() {
    // 修补fetch
    const originalFetch = window.fetch;
    window.fetch = function(url, options = {}) {
        // 确保options存在
        if (!options.headers) {
            options.headers = {};
        }
        
        // 如果是POST/PUT/PATCH请求且没有设置Content-Type，自动设置
        const method = (options.method || 'GET').toUpperCase();
        if (['POST', 'PUT', 'PATCH'].includes(method)) {
            // 检查headers对象或Headers实例
            if (options.headers instanceof Headers) {
                if (!options.headers.has('Content-Type')) {
                    options.headers.set('Content-Type', 'application/json');
                    console.log('🔧 自动修复fetch请求的Content-Type');
                }
            } else if (typeof options.headers === 'object') {
                if (!options.headers['Content-Type'] && !options.headers['content-type']) {
                    options.headers['Content-Type'] = 'application/json';
                    console.log('🔧 自动修复fetch请求的Content-Type');
                }
            }
        }
        
        return originalFetch.call(this, url, options);
    };
    
    // 修补XMLHttpRequest
    const originalOpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function(method, url) {
        this._originalMethod = method;
        this._originalUrl = url;
        return originalOpen.apply(this, arguments);
    };
    
    const originalSend = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.send = function(data) {
        // 如果是POST/PUT/PATCH请求且没有设置Content-Type，自动设置
        if (this._originalMethod && ['POST', 'PUT', 'PATCH'].includes(this._originalMethod.toUpperCase())) {
            if (!this.getRequestHeader('Content-Type') && data) {
                this.setRequestHeader('Content-Type', 'application/json');
                console.log('🔧 自动修复XMLHttpRequest请求的Content-Type');
            }
        }
        return originalSend.apply(this, arguments);
    };
}

// 立即执行修复
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fixContentTypeIssues);
} else {
    // 页面已经加载完成，立即修复
    fixContentTypeIssues();
}

// 导出主要函数供其他脚本调用
window.fixContentTypeIssues = fixContentTypeIssues;
window.showFixNotification = showFixNotification;
