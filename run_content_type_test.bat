@echo off

:: Content-Type修复测试启动脚本
:: 此脚本会启动Flask服务器并运行验证测试

color 0A
echo ========================================================
echo           Content-Type修复测试工具
echo ========================================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python。请先安装Python并添加到系统PATH。
    pause
    exit /b 1
)

echo 步骤1: 启动Flask服务器...
echo 请保持此窗口打开，不要关闭！
echo.

:: 启动Flask服务器在后台运行
start "Flask Server" cmd /k "python app.py"

echo 等待服务器启动...
:: 等待3秒让服务器启动
ping localhost -n 4 >nul

echo.
echo 步骤2: 运行Content-Type验证测试...
echo.

:: 运行验证测试脚本
python verify_content_type_fix.py

set test_result=%errorlevel%

echo.
echo ========================================================

if %test_result% equ 0 (
    echo ^(^✓^) 测试成功！Content-Type修复验证通过。
    echo.
    echo 建议使用fixed_ai_report.html页面进行正常的API调用。
) else (
    echo ^(^✗^) 测试失败！请检查问题。
    echo.
    echo 可能原因：
    echo 1. 服务器未正确启动
    echo 2. API端点路径有变化
    echo 3. 文件路径配置不正确
)

echo ========================================================
echo.
echo 按任意键关闭测试窗口...
pause >nul

:: 关闭Flask服务器窗口
taskkill /FI "WINDOWTITLE eq Flask Server" /F >nul 2>&1

exit /b %test_result%
