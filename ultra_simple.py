# 这是一个超级简单的脚本，只做文件写入

# 直接写入文件，不使用任何函数
open('ultra_output.txt', 'w').write('Hello World!\n')
open('ultra_output.txt', 'a').write('This is a test.\n')
open('ultra_output.txt', 'a').write('Python version: ' + str(__import__('sys').version) + '\n')
open('ultra_output.txt', 'a').write('Current directory: ' + str(__import__('os').getcwd()) + '\n')

# 强制刷新
__import__('os').sync()