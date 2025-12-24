import os
import uuid
from werkzeug.utils import secure_filename

# 支持的文件类型
ALLOWED_EXTENSIONS = {'doc', 'docx', 'pdf', 'md', 'txt'}

# 文件上传目录
UPLOAD_FOLDER = 'AI_analysis/uploads'

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """检查文件类型是否被允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_file_upload(file):
    """处理文件上传并返回文件路径"""
    if file and allowed_file(file.filename):
        # 生成唯一文件名
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # 保存文件
        file.save(file_path)
        
        return {
            'success': True,
            'file_path': file_path,
            'original_filename': filename
        }
    else:
        return {
            'success': False,
            'error': '不支持的文件类型，请上传Word/PDF/Markdown/TXT格式的文件'
        }

def read_file_content(file_path):
    """读取文件内容（根据文件类型进行不同处理）"""
    try:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext in ['.txt', '.md']:
            # 读取文本文件，尝试不同编码
            encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    # 验证内容是否合理（至少包含一些中文字符或英文字符）
                    if any(char.isalpha() or char.isdigit() for char in content):
                        return content
                except UnicodeDecodeError:
                    continue
            return '无法读取文件内容，可能是编码问题'
        elif ext in ['.doc', '.docx']:
            # 使用python-docx读取Word文件
            try:
                from docx import Document
                doc = Document(file_path)
                content = []
                for para in doc.paragraphs:
                    content.append(para.text)
                return '\n'.join(content)
            except ImportError:
                return '需要安装python-docx库来读取Word文件'
        elif ext == '.pdf':
            # 使用PyPDF2读取PDF文件
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    content = []
                    for page in reader.pages:
                        content.append(page.extract_text())
                    return '\n'.join(content)
            except ImportError:
                return '需要安装PyPDF2库来读取PDF文件'
        else:
            return '不支持的文件格式'
    except Exception as e:
        return f'读取文件失败：{str(e)}'
