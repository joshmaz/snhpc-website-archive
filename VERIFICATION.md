# Archive split verification

Verified locally September 26–27, 2026, from source main `91f6995aedc33ec19ad04071f4175b439fe19f06`.

## Passed

- Source checkout is unchanged. All 189 original archive files are preserved in the archive repository's initial commit and SHA-256 manifest.
- Archive builds without dependencies or application credentials.
- 1,253 local HTML/CSS URL references resolve to existing output files.
- Routing tests cover the root, archive entrance redirect, directory and extensionless archive pages, query preservation, asset paths, and missing-page behavior. CloudFront configuration maps origin 403/404 responses to an actual HTTP 404.
- Chromium rendered the entrance, Home, About Us, Events, Gallery, Menu, Our Games and Merch with all third-party networking blocked. No local requests returned errors after the fixes. All images loaded when lazy images were requested: Home 14/14, About 3/3, Events 6/6, Gallery 14/14, Menu 65/65, Our Games 65/65, Merch 17/17.
- Entrance-link navigation reaches the archived home. The home also loads at a 390px mobile viewport. Desktop screenshot inspected; preserved historical layout includes blank/unavailable embedded map content.
- Browser checks exposed Wix runtime requests for an uncaptured worker and replacement of local image URLs. The build now strips original executable scripts from published pages, retaining the archive slideshow/navigation scripts. Original source scripts remain preserved.
- Eight slideshow images and three PayPal image assets are local. External links and embeds remain historical references.
- Current website full build passed with bundled Node 24 and placeholder public Supabase settings: **99 tests passed**, duplicate-event check passed, public snapshot check passed. Initial system Node 22 attempts failed on TypeScript imports; Node 24 completed successfully. No source code changes were needed.

## Pending: requires AWS and DNS access

- CloudFormation service validation and actual stack creation.
- S3 upload, CloudFront deployment and cache invalidation.
- Live archive HTTP redirects, real edge 404 responses, image content types and HTTPS certificate checks.
- DNS/subdomain activation. Public DNS returned NXDOMAIN for `archive.snhpinball.club`; local resolution of the main hostname also failed. This does not establish the cause or domain registration status.
- Live current-site verification; its build is verified, but its public URL was not reachable through local DNS during this task.

No AWS profiles or credentials were available. No AWS or DNS changes were made. No archive content was removed from the source repository. Follow `DEPLOYMENT.md` and record live acceptance before any removal.
