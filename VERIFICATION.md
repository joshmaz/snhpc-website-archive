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

## Live deployment completed — September 27, 2026 (America/New_York)

- Live URL: https://archive.snhpinballclub.com/
- CloudFormation stack `snhpc-website-archive`: `UPDATE_COMPLETE`; CloudFront `E2B9WQHNSCJAZD`: `Deployed`.
- Private S3 bucket: `snhpc-website-archive-bucket-uvqanalzyf9y`; all four public-access block settings remain enabled.
- CloudFront hostname: `d1riwi2wpmrl73.cloudfront.net`.
- ACM certificate `00b6875d-2962-4bcf-a073-3fbec3e5c5c7` in us-east-1: `ISSUED`, covering `archive.snhpinballclub.com`.
- Cloudflare DNS-only CNAME `archive` points to the archive CloudFront hostname. ACM validation CNAME is retained for renewal. Existing production DNS records were not changed.
- GitHub deployment [36360503905](https://github.com/joshmaz/snhpc-website-archive/actions/runs/36360503905) succeeded using OIDC; cache invalidation completed.
- The IAM trust matches GitHub's immutable subject `repo:joshmaz@80361142/snhpc-website-archive@1389793903:ref:refs/heads/main`. The initial name-only subject failed authentication and was corrected without broadening repository, branch or resource access.
- `python3 scripts/check-live.py` passed: entrance, home, About Us, Events, Gallery, Menu, Our Games, Merch and sample PNG/GIF assets return 200; both missing-page forms return 404 with the archive error page; archive entrance and HTTP-to-HTTPS redirects return 301. TLS certificate verification remained enabled.
- The live browser followed entrance → Home → Gallery → About Us, and gallery image elements loaded. Screenshot of the live homepage was captured.
- Production homepage and original `/wix_archive/index.html` return 200 with curl. Python urllib received a production Cloudflare 403; the availability check therefore uses curl for production. Archive checks use urllib normally.
- Source main remains `91f6995aedc33ec19ad04071f4175b439fe19f06`, matching the source that passed all 99 tests and the full build. No source-repository changes or production deployments were made.

The archive deployment and subdomain are confirmed working. The duplicate content remains in the source repository; removal and old-domain redirects are a separate follow-up.
