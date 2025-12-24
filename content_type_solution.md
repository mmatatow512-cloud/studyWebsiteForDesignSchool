# Content-Type: application/json 问题解决方案

## 问题分析

根据界面显示的错误信息 "请设置Content-Type为application/json"，这是因为API端点期望接收JSON格式的数据，但请求头中没有正确设置 `Content-Type: application/json`。

## 原因详解

1. 当API设计为接收JSON数据时，服务器会检查请求头中的Content-Type
2. 如果缺少正确的Content-Type头，服务器无法识别数据格式，会返回415 Unsupported Media Type错误
3. 这是REST API的标准行为，确保数据格式正确以进行处理

## 解决方案

### 前端解决方案

以下是在不同环境中设置Content-Type的方法：

#### 1. 使用JavaScript fetch API
```javascript
fetch('/api/evaluation_report', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'  // 关键设置
  },
  body: JSON.stringify({
    file_path: 'your_file_path',
    description: '可选描述'
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

#### 2. 使用jQuery
```javascript
$.ajax({
  url: '/api/evaluation_report',
  type: 'POST',
  contentType: 'application/json',  // 关键设置
  data: JSON.stringify({
    file_path: 'your_file_path',
    description: '可选描述'
  }),
  success: function(data) {
    console.log(data);
  },
  error: function(error) {
    console.error('Error:', error);
  }
});
```

#### 3. 使用Axios
```javascript
axios.post('/api/evaluation_report', {
  file_path: 'your_file_path',
  description: '可选描述'
}, {
  headers: {
    'Content-Type': 'application/json'  // 关键设置
  }
})
.then(function(response) {
  console.log(response.data);
})
.catch(function(error) {
  console.error('Error:', error);
});
```

### 后端解决方案

如果您是API开发者，可以考虑以下改进：

1. 在API代码中添加更好的错误处理和提示信息
2. 对于调试目的，可以临时允许不设置Content-Type，但生产环境应该严格要求
3. 在API文档中明确说明需要设置的Content-Type头

## 相关文件

本项目中包含以下文件来帮助您解决这个问题：

1. `frontend_content_type_fix.js` - 前端JavaScript修复代码示例
2. `content_type_fixed_template.html` - 修复后的完整HTML模板
3. `content_type_example.py` - Python请求示例
4. `test_with_content_type.py` - 测试工具

## 使用方法

1. 参考 `content_type_fixed_template.html` 中的表单提交方式
2. 确保在发送请求前设置正确的Content-Type头
3. 使用JSON.stringify()将JavaScript对象转换为JSON字符串

## 开发者提示

- 使用浏览器的开发者工具（F12）检查Network面板，可以确认请求头是否正确设置
- 如果仍然遇到问题，请检查服务器端API是否正确配置以接收JSON数据
- 对于复杂的数据处理，考虑使用表单数据（multipart/form-data）并相应地调整服务器代码