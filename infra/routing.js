function handler(event) {
  var request = event.request;
  var uri = request.uri;
  if (uri === '/wix_archive') {
    return {statusCode: 301, statusDescription: 'Moved Permanently', headers: {location: {value: '/wix_archive/'}}};
  }
  if (uri.endsWith('/')) request.uri += 'index.html';
  else if (/^\/wix_archive\/site\/snhpinball\.wixsite\.com\/home(?:\/(?:about-us|events|grid|menu|merch|our-games))?$/.test(uri)) request.uri += '/index.html';
  return request;
}
