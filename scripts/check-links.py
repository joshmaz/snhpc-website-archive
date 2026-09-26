"""Validate local HTML and CSS resources without requiring Wix network access."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import re
root=Path('dist').resolve()
errors=set(); checked=0; external=set()
def check(value, source):
 global checked
 if value and '${' in value: return  # Wix runtime template, not a literal CSS URL
 if not value or value.startswith(('data:', 'mailto:', 'tel:', '#', 'javascript:')): return
 u=urlsplit(urljoin('https://archive.test/'+source.relative_to(root).as_posix(), value))
 if u.netloc!='archive.test':
  external.add(u.netloc); return
 target=root/unquote(u.path).lstrip('/')
 if u.path.endswith('/'): target=target/'index.html'
 checked+=1
 if not target.is_file(): errors.add((str(source.relative_to(root)),value))
class Parser(HTMLParser):
 def handle_starttag(self, tag, attrs):
  for key,value in attrs:
   if key in ('href','src','poster'): check(value, source)
for source in root.rglob('*'):
 if source.suffix=='.html': Parser().feed(source.read_text())
 if source.suffix in ('.html','.css'):
  for value in re.findall(r'url\([\s\"\']*([^\)\"\']+)',source.read_text()): check(value.strip(),source)
print(f'Checked {checked} local references; {len(errors)} missing')
print('External hosts:', ', '.join(sorted(external)))
for error in sorted(errors): print(error)
assert not errors
