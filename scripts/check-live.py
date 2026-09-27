"""Live acceptance checks. Run after deployment: python3 scripts/check-live.py"""
import urllib.request, urllib.error
base='https://archive.snhpinballclub.com'
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl): return None
opener=urllib.request.build_opener(NoRedirect)
def fetch(url):
 try: return opener.open(url,timeout=30)
 except urllib.error.HTTPError as error: return error
checks={
 '/':(200,'text/html'),
 '/wix_archive/':(200,'text/html'),
 '/wix_archive/site/snhpinball.wixsite.com/home/':(200,'text/html'),
 '/wix_archive/site/snhpinball.wixsite.com/home/about-us':(200,'text/html'),
 '/wix_archive/site/snhpinball.wixsite.com/home/events/index.html':(200,'text/html'),
 '/wix_archive/site/snhpinball.wixsite.com/home/grid/index.html':(200,'text/html'),
 '/wix_archive/site/snhpinball.wixsite.com/home/menu/index.html?menu=pinball':(200,'text/html'),
 '/wix_archive/site/snhpinball.wixsite.com/home/our-games/index.html':(200,'text/html'),
 '/wix_archive/site/snhpinball.wixsite.com/home/merch/index.html':(200,'text/html'),
 '/wix_archive/assets/slideshow/fb7b05_1e20a8131fa048708bd65678bb565f1a~mv2.png':(200,'image/png'),
 '/wix_archive/assets/paypal/btn_buynow_LG.gif':(200,'image/gif'),
 '/missing-archive-check-20260927':(404,'text/html'),
 '/missing-archive-check-20260927/':(404,'text/html'),
}
for path,(status,kind) in checks.items():
 with fetch(base+path) as r:
  assert r.status==status,(path,r.status)
  assert kind in r.headers.get('Content-Type',''),(path,r.headers)
  body=r.read()
  if status==404: assert b'Page not found' in body
  print(r.status,path)
for url,target in [(base+'/wix_archive','/wix_archive/'),('http://archive.snhpinballclub.com/',base+'/')]:
 with fetch(url) as r:
  assert r.status in (301,302,307,308),(url,r.status)
  assert r.headers['Location']==target,(url,r.headers['Location'])
  print(r.status,url,'->',target)
for url in ['https://snhpinballclub.com/','https://snhpinballclub.com/wix_archive/index.html']:
 with fetch(url) as r:
  assert r.status==200,(url,r.status)
  print(r.status,url)
print('Live acceptance passed; HTTPS certificate validation was enabled.')
