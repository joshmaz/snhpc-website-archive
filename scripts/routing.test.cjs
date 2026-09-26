const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const code = fs.readFileSync('infra/routing.js','utf8');
const context = vm.createContext({}); vm.runInContext(code,context);
function route(uri) { return context.handler({request:{uri,querystring:{menu:{value:'pinball'}}}}); }
test('directory and historical page URLs resolve to actual objects',()=>{
 for (const [uri,expected] of [['/','/index.html'],['/wix_archive/','/wix_archive/index.html'],['/wix_archive/site/snhpinball.wixsite.com/home/about-us','/wix_archive/site/snhpinball.wixsite.com/home/about-us/index.html']]) {
  const result=route(uri); assert.equal(result.uri,expected); assert.ok(fs.existsSync('dist'+expected)); assert.equal(result.querystring.menu.value,'pinball');
 }
});
test('archive redirect, asset paths and missing paths remain distinct',()=>{
 assert.equal(route('/wix_archive').statusCode,301);
 assert.equal(route('/wix_archive').headers.location.value,'/wix_archive/');
 assert.equal(route('/missing-page').uri,'/missing-page');
 assert.equal(route('/image.png').uri,'/image.png');
 const config=JSON.parse(fs.readFileSync('infra/archive.json'));
 assert.equal(config.Resources.Routing.Properties.FunctionCode,code);
 for (const response of config.Resources.Distribution.Properties.DistributionConfig.CustomErrorResponses) assert.equal(response.ResponseCode,404);
});
