// 前端JavaScript代码示例：修复Content-Type设置问题

// 示例1：使用fetch API发送请求时设置正确的Content-Type
function submitAnalysisWithFetch() {
    // 获取表单数据
    const fileInput = document.querySelector('input[type="file"]'); // 假设文件输入框
    const file = fileInput.files[0];
    const description = document.querySelector('textarea').value;
    
    // 准备API请求数据
    const payload = {
        file_path: file.name, // 或者其他文件标识信息
        description: description
    };
    
    // 使用fetch API发送请求，明确设置Content-Type
    fetch('/api/evaluation_report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // 关键：设置正确的Content-Type
            // 如果需要认证，可以添加Authorization头
            // 'Authorization': 'Bearer your-token-here'
        },
        body: JSON.stringify(payload) // 将JavaScript对象转换为JSON字符串
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP错误! 状态: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('成功:', data);
        // 处理成功响应，例如显示结果
        alert('智能分析成功完成!');
    })
    .catch(error => {
        console.error('错误:', error);
        alert(`请求失败: ${error.message}`);
    });
}

// 示例2：使用XMLHttpRequest设置Content-Type
function submitAnalysisWithXHR() {
    const fileInput = document.querySelector('input[type="file"]');
    const file = fileInput.files[0];
    const description = document.querySelector('textarea').value;
    
    const payload = {
        file_path: file.name,
        description: description
    };
    
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/evaluation_report', true);
    
    // 设置Content-Type
    xhr.setRequestHeader('Content-Type', 'application/json');
    
    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 300) {
            const data = JSON.parse(xhr.responseText);
            console.log('成功:', data);
            alert('智能分析成功完成!');
        } else {
            console.error('请求失败:', xhr.status, xhr.statusText);
            alert(`请求失败: ${xhr.status} ${xhr.statusText}`);
        }
    };
    
    xhr.onerror = function() {
        console.error('网络错误');
        alert('网络错误，请检查连接');
    };
    
    // 发送JSON数据
    xhr.send(JSON.stringify(payload));
}

// 示例3：修改现有的表单提交处理函数
function modifyFormSubmission() {
    // 假设您有一个表单提交按钮
    const submitButton = document.querySelector('.紫色按钮'); // 根据实际HTML结构修改选择器
    
    submitButton.addEventListener('click', function(event) {
        // 阻止默认表单提交行为
        event.preventDefault();
        
        // 使用示例1或示例2中的方法发送请求
        submitAnalysisWithFetch();
        // 或者 submitAnalysisWithXHR();
    });
}

// 页面加载完成后初始化
if (typeof window !== 'undefined') {
    window.addEventListener('DOMContentLoaded', function() {
        // 初始化修复
        modifyFormSubmission();
    });
}

/*
使用说明：
1. 将此JavaScript文件引入到您的HTML页面中
2. 根据您的实际页面结构调整选择器
3. 确保API端点路径('/api/evaluation_report')与后端匹配
4. 根据需要调整payload数据结构

关键要点：
- 必须在请求头中设置 'Content-Type': 'application/json'
- 发送的body数据必须是JSON字符串，使用JSON.stringify()转换
- 处理响应时需要检查HTTP状态码
*/