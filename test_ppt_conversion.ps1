# Test PPT to Video Conversion

# Step 1: Login to get session
Write-Host "Step 1: Logging in..."
try {
    $loginResponse = Invoke-WebRequest -Uri http://127.0.0.1:5001/login -Method POST -Body @{username='admin';password='admin'} -SessionVariable session -UseBasicParsing
    Write-Host "Login successful! Status: $($loginResponse.StatusCode)"
} catch {
    Write-Host "Login failed: $($_.Exception.Message)"
    exit 1
}

# Step 2: Test PPT to Video conversion
Write-Host "\nStep 2: Testing PPT to Video conversion..."
$filePath = "./test_ppt.pptx"

if (-not (Test-Path $filePath)) {
    Write-Host "Error: Test file $filePath not found!"
    exit 1
}

Write-Host "Using test file: $filePath"
Write-Host "File size: $((Get-Item $filePath).Length / 1KB) KB"

# Set long timeout to handle conversion
$ProgressPreference = 'SilentlyContinue' # Disable progress bar for faster upload
$timeoutSeconds = 600 # 10 minutes timeout

$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

try {
    # For PowerShell 5, using .NET WebClient is more reliable for file uploads
    Write-Host "Using WebClient for file upload..."
    $webClient = New-Object System.Net.WebClient
    
    # Add cookies from session
    $cookies = $session.Cookies.GetCookies("http://127.0.0.1:5001")
    $cookieArray = @()
    foreach ($cookie in $cookies) {
        $cookieArray += "$($cookie.Name)=$($cookie.Value)"
    }
    $cookieHeader = $cookieArray -join "; "
    $webClient.Headers.Add("Cookie", $cookieHeader)
    
    # Note: Timeout property in WebClient behaves differently in different PowerShell versions
    # Removing explicit timeout setting
    
    # Create file upload form
    $uri = "http://127.0.0.1:5001/convert_ppt_to_video"
    $fileFieldName = "file"
    $method = "POST"
    
    Write-Host "Uploading file and starting conversion..."
    
    # Use WebClient to upload the file - it returns response bytes directly
    $responseBytes = $webClient.UploadFile($uri, $method, $filePath)
    
    # Check response headers
    $contentType = $webClient.ResponseHeaders["Content-Type"]
    $contentLength = $webClient.ResponseHeaders["Content-Length"]
    
    $stopwatch.Stop()
    $elapsedMinutes = $stopwatch.Elapsed.TotalMinutes.ToString("F2")
    
    Write-Host "Conversion completed! Time taken: $elapsedMinutes minutes"
    Write-Host "Content Type: $contentType"
    Write-Host "Content Length: $contentLength bytes"
    
    # Check if response is a video
    if ($contentType -like "video/*") {
        Write-Host "✓ Received video file! Size: $($responseBytes.Length / 1MB) MB"
        
        # Save the video
        $outputPath = "./output_test.mp4"
        [System.IO.File]::WriteAllBytes($outputPath, $responseBytes)
        Write-Host "Video saved to: $outputPath"
        Write-Host "Video file created successfully!"
    } else {
        # Try to convert response to string for text responses
        try {
            $responseText = [System.Text.Encoding]::UTF8.GetString($responseBytes)
            Write-Host "⚠️  Received non-video response. Content preview (first 200 chars):"
            Write-Host $responseText.Substring(0, [Math]::Min(200, $responseText.Length))
        } catch {
            Write-Host "⚠️  Received binary response that is not a video. Size: $($responseBytes.Length / 1KB) KB"
        }
    }
    
    # Clean up WebClient
    $webClient.Dispose()
    
} catch {
    $stopwatch.Stop()
    $elapsedMinutes = $stopwatch.Elapsed.TotalMinutes.ToString("F2")
    
    Write-Host "Error during conversion: $($_.Exception.Message)"
    Write-Host "Time taken before error: $elapsedMinutes minutes"
    
    # Clean up WebClient if it was created
    if (Get-Variable -Name webClient -ErrorAction SilentlyContinue) {
        $webClient.Dispose()
    }
}

Write-Host "\nTest completed!"