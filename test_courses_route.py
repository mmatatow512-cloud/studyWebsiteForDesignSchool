import http.client

print("Testing /courses route...")
conn = http.client.HTTPConnection("127.0.0.1", 5001)
conn.request("GET", "/courses")
response = conn.getresponse()
print(f"Status: {response.status} {response.reason}")
print(f"Content-Type: {response.getheader('Content-Type')}")
conn.close()

print("\nTesting /course_library route...")
conn = http.client.HTTPConnection("127.0.0.1", 5001)
conn.request("GET", "/course_library")
response = conn.getresponse()
print(f"Status: {response.status} {response.reason}")
print(f"Content-Type: {response.getheader('Content-Type')}")
conn.close()
