import xml.etree.ElementTree as ET
import re

tree = ET.parse('feed.xml')
items = tree.getroot().findall('.//item')[:5]

lines = []
for item in items:
    title = item.find('title').text.strip()
    link = item.find('link').text.strip().replace('https://reddi.ai', 'https://reddi.tech')
    pub = item.find('pubDate').text.strip()[:16]
    lines.append('- [{}]({}) -- {}'.format(title, link, pub))

separator = chr(10)
block = separator.join(lines)
start = '<!-- BLOG_POSTS_START -->'
end = '<!-- BLOG_POSTS_END -->'
note = '<!-- Auto-updated daily via GitHub Actions - source: reddi.tech/feed.xml -->'

with open('README.md', 'r') as f:
    content = f.read()

replacement = '{}{}{}{}{}{}{}{}'.format(start, chr(10), note, chr(10), block, chr(10), end, '')
content = re.sub(
    r'<!-- BLOG_POSTS_START -->.*?<!-- BLOG_POSTS_END -->',
    replacement,
    content,
    flags=re.DOTALL
)

with open('README.md', 'w') as f:
    f.write(content)

print('Injected {} posts'.format(len(lines)))
