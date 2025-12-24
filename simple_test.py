print("Hello, Python!")
print("Current directory:", __import__('os').getcwd())
print("Script path:", __import__('os').path.abspath(__file__))