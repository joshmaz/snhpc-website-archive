import { cp, mkdir, rm } from 'node:fs/promises';
await rm('dist', {recursive:true, force:true});
await mkdir('dist');
for (const file of ['index.html','404.html','robots.txt','wix_archive']) await cp(file, 'dist/'+file, {recursive:true});
console.log('Built dist/');
