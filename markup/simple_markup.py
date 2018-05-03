# re.sub用法
from util import *
import sys, re

print('<html><head><title>...</title><body>')

title = True
for block in blocks(sys.stdin):
    re.sub(r'\*(.+?)\*', r'<em>\1</em>', block)
    if title:
        print('<h1>')
        print(block)
        print('</h1>')
        title = False
    else:
        print('<p>')
        print(block)
        print('</p>')
print('</body></html>')
