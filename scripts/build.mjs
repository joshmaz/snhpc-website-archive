import { cp, mkdir, rm } from 'node:fs/promises';
await rm('dist', {recursive:true, force:true});
await mkdir('dist');
for (const file of ['index.html','404.html','robots.txt','wix_archive']) await cp(file, 'dist/'+file, {recursive:true});
console.log('Built dist/');
// Frozen museum pages use their captured HTML/CSS. Rehydrating Wix replaces
// saved image URLs and starts workers/APIs that were never captured.
const {readdir, readFile, writeFile} = await import('node:fs/promises');
async function freeze(dir) {
 for (const entry of await readdir(dir,{withFileTypes:true})) {
  const file=dir+'/'+entry.name;
  if(entry.isDirectory()) await freeze(file);
  else if(file.endsWith('.html')) {
   let html=await readFile(file,'utf8');
   html=html.replace(/<script\b[^>]*>[\s\S]*?<\/script\s*>/gi,tag=> /\bsrc=["'][^"']*\/archive-(?:nav-fix|marquee)\.js["']/.test(tag) || /\bsrc=["']archive-(?:nav-fix|marquee)\.js["']/.test(tag) ? tag : '');
   await writeFile(file,html);
  }
 }
}
await freeze('dist/wix_archive/site/snhpinball.wixsite.com');
