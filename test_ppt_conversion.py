import requests
import os
import time

# Configuration
BASE_URL = "http://127.0.0.1:5001"
TEST_FILE = "test_ppt.pptx"
OUTPUT_FILE = "output_test.mp4"
TIMEOUT = 600  # 10 minutes

print("Step 1: Logging in...")
# Login
login_data = {"username": "admin", "password": "admin"}
session = requests.Session()
# Allow redirects and print detailed information
login_response = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=True)

print(f"Login status code: {login_response.status_code}")
print(f"Login URL: {login_response.url}")
print(f"Login headers: {login_response.headers}")
print(f"Login cookies: {session.cookies}")

# Check if we were redirected to dashboard
if 'dashboard' in login_response.url:
    print("Login successful and redirected to dashboard!")
else:
    print("Login response content preview (first 500 chars):")
    print(login_response.text[:500])
    exit(1)

print(f"\nStep 2: Testing PPT to Video conversion...")
# Check if test file exists
if not os.path.exists(TEST_FILE):
    print(f"Test file {TEST_FILE} not found!")
    exit(1)

# Get file size
file_size = os.path.getsize(TEST_FILE) / (1024 * 1024)  # Convert to MB
print(f"Using test file: {TEST_FILE}")
print(f"File size: {file_size:.2f} MB")

# Start timer
start_time = time.time()

# Test conversion
try:
    print("Uploading file and converting...")
    with open(TEST_FILE, 'rb') as f:
        files = {'ppt_file': f}
        # Set a long timeout for the conversion
        response = session.post(f"{BASE_URL}/convert_ppt_to_video", files=files, timeout=TIMEOUT)
    
    # Check response
    if response.status_code == 200:
        # Check if response is a video
        content_type = response.headers.get('Content-Type')
        if 'video' in content_type:
            # Save video
            with open(OUTPUT_FILE, 'wb') as f:
                f.write(response.content)
            
            elapsed_time = (time.time() - start_time) / 60  # Convert to minutes
            print(f"\nConversion successful!")
            print(f"Time taken: {elapsed_time:.2f} minutes")
            print(f"Video saved as: {OUTPUT_FILE}")
            print(f"Video size: {len(response.content) / (1024 * 1024):.2f} MB")
        else:
            print(f"\nConversion failed: Server returned non-video content")
            print(f"Content-Type: {content_type}")
            print(f"Response preview (first 500 chars): {response.text[:500]}...")
    else:
        print(f"\nConversion failed with status: {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.Timeout:
    elapsed_time = (time.time() - start_time) / 60
    print(f"\nConversion timed out after {elapsed_time:.2f} minutes")
except Exception as e:
    elapsed_time = (time.time() - start_time) / 60
    print(f"\nError during conversion: {str(e)}")
    print(f"Time taken before error: {elapsed_time:.2f} minutes")

print("\nTest completed!")