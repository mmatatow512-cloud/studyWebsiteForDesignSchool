# PowerShell script: Run Python and capture errors
Write-Host "=== Python Test Started ==="

# Show current directory
Write-Host "Current directory: $(Get-Location)"

# Run Python script and capture all output
try {
    $output = & python test_hello.py 2>&1
    Write-Host "Python output: $output"
    Write-Host "Python execution completed successfully"
} catch {
    Write-Host "Python execution failed: $_"
    Write-Host "Error details: $($_.Exception.Message)"
}

Write-Host "=== Python Test Completed ==="