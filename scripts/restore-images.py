"""Save clear Wix renditions locally and replace captured blurred img sources."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor
import urllib.request,re,json
root=Path(__file__).resolve().parent.parent
pages=list((root/'wix_archive/site/snhpinball.wixsite.com').rglob('*.html'))
refs={}
class Images(HTMLParser):
 def handle_starttag(self,tag,attrs):
  if tag!='img':return
  src=dict(attrs).get('src','')
  if 'blur_' not in src:return
  match=re.search(r'static\.wixstatic\.com/media/([^/]+)/',unquote(src))
  if match: refs[src]=match.group(1)
for page in pages: Images().feed(page.read_text())
folder=root/'wix_archive/assets/clear-images';folder.mkdir(parents=True,exist_ok=True)
def save(media):
 url=f'https://static.wixstatic.com/media/{media}/v1/fit/w_800,h_800,q_85/{media}'
 target=folder/media
 if not target.exists():
  with urllib.request.urlopen(url,timeout=60) as response:
   data=response.read();kind=response.headers.get('Content-Type','')
  if not kind.startswith('image/') or len(data)<500:raise ValueError((url,kind,len(data)))
  target.write_bytes(data)
 return media,{'url':url,'bytes':target.stat().st_size}
with ThreadPoolExecutor(max_workers=6) as pool: saved=dict(pool.map(save,sorted(set(refs.values()))))
count=0
for page in pages:
 s=page.read_text()
 def replace(match):
  global count
  tag=match.group(0)
  for src,media in refs.items():
   old='src="'+src+'"'
   if old in tag:
    count+=1
    return tag.replace(old,'src="/wix_archive/assets/clear-images/'+media+'"')
  return tag
 out=re.sub(r'<img\b[^>]*>',replace,s,flags=re.I)
 if out!=s:page.write_text(out)
if saved:(root/'IMAGE-RESTORATION.json').write_text(json.dumps(saved,indent=2)+'\n')
print(f'Saved {len(saved)} clear images; replaced {count} blurred image references across {len(pages)} pages')
