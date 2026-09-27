# Southern New Hampshire Pinball Club website archive

Independent museum copy of the former Wix site, copied from `joshmaz/pinball-club-website` at `91f6995aedc33ec19ad04071f4175b439fe19f06`. The original 189 files are preserved in the first commit and hashed in `SOURCE-MANIFEST.json`. Nothing was removed from the current website.

## Build and verify

Requires Node 22+ and Python 3; no package installation, database, API keys, or Supabase configuration.

```sh
node scripts/build.mjs
python3 scripts/check-links.py
node --test scripts/routing.test.cjs
python3 -m http.server 8000 --directory dist
```

Open `/` for the museum entrance. Historical `/wix_archive/…` paths remain intact. The current-club link points to `https://snhpinballclub.com/`. Only `dist/` is deployed.

## Inventory and limitations

The original snapshot contains 12 HTML files: the museum entrance, archived home, About Us, Events, Gallery (`grid`), Merch, and three saved variants each of Menu and Our Games. It also includes mirrored Wix JavaScript, styles, image variants, and fonts. Eight slideshow images and three PayPal image assets are now stored locally. The runtime navigation helper's incorrect home prefix has been corrected.

Local HTML/CSS references are validated at build time. The original mirror retains Wix runtime configuration. The build removes Wix executable scripts from published HTML because they overwrite saved images and request uncaptured workers; it keeps the archive navigation and slideshow scripts. Remaining external references include: Wix/Parastorage resource hints, Facebook, YouTube, Pintastic and Internet Archive links. This is a historical static snapshot; original payment, menu filtering, video, and other interactive integrations are not guaranteed to work offline or after their providers change. Do not use archived payment/membership information as current club instructions.

See [deployment instructions](DEPLOYMENT.md) and [verification results](VERIFICATION.md).

**Do not remove `wix_archive/` from the source repository until the new deployment and `archive.snhpinballclub.com` pass live acceptance checks.**
