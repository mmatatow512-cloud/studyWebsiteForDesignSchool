# PowerShell脚本：运行Python环境检查
Write-Host "=== Python环境检查开始 ==="

# 使用python运行环境检查脚本
$output = & python check_python.py 2>&1

# 显示输出结果
Write-Host "Python环境检查输出:"
Write-Host $output

# 检查返回码
if ($LASTEXITCODE -eq 0) {
    Write-Host "=== Python环境检查成功完成 ==="
} else {
    Write-Host "=== Python环境检查失败，退出码: $LASTEXITCODE ==="
}
