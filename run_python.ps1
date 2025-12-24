# PowerShell脚本：运行Python并捕获错误信息
Write-Host "=== 运行Python测试开始 ==="

# 显示当前目录
Write-Host "当前目录: $(Get-Location)"

# 显示Python版本
Write-Host ""
Write-Host "=== 检查Python版本 ==="
try {
    python --version 2>&1
    Write-Host "Python版本检查完成"
} catch {
    Write-Host "Python版本检查失败: $_"
}

# 直接运行Python脚本
Write-Host ""
Write-Host "=== 直接运行test_hello.py ==="
try {
    $result = & python test_hello.py 2>&1
    Write-Host "运行结果: $result"
    Write-Host "Python脚本运行完成"
} catch {
    Write-Host "Python脚本运行失败: $_"
    Write-Host "错误详情: $($_.Exception.Message)"
}

# 尝试使用python3
Write-Host ""
Write-Host "=== 尝试使用python3运行 ==="
try {
    $result = & python3 test_hello.py 2>&1
    Write-Host "运行结果: $result"
    Write-Host "Python3脚本运行完成"
} catch {
    Write-Host "Python3脚本运行失败: $_"
    Write-Host "错误详情: $($_.Exception.Message)"
}

Write-Host ""
Write-Host "=== 运行Python测试结束 ==="