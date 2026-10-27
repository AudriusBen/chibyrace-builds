# ChibyRace builds

Downloads page for ChibyRace Android test builds, served by GitHub Pages from this repo.
The APKs are attached to this repo's releases (tag `v<version>`, asset `ChibyRace-<version>.apk`).

To add a build: create the release with its APK, add the build at the top of `builds.json`
(version, date, size, sha256, notes), run `python3 tools/make_site.py`, and push.
