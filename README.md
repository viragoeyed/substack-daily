# substack daily: setup (about 10 minutes, one time)

1. Make a free account at github.com, then click **New repository**. Name it anything (e.g. `substack-daily`), set it to **Public**, and create it.
2. Click **Add file → Upload files**, drag in everything from this folder (`index.html`, `fetch_feeds.py`, `feeds.json`, `data.json`, `README.md`) and commit.
3. The hidden `.github` folder may not upload by dragging. If you don't see `.github/workflows/daily.yml` in the repo: **Add file → Create new file**, type `.github/workflows/daily.yml` as the name, paste in the contents of `daily.yml` from this folder, and commit.
4. **Settings → Pages**: under "Build and deployment" choose *Deploy from a branch*, branch `main`, folder `/ (root)`, Save. After a minute your site is at `https://YOURNAME.github.io/REPO/`. Bookmark it.
5. **Actions** tab → "Refresh Substack feed" → **Run workflow** once, so real posts replace the placeholder data. After that it refreshes by itself every morning around 6:00 IST.

## Adding more newsletters
Edit `feeds.json` on GitHub (pencil icon) and add a line. Any Substack's feed is its address plus `/feed`, e.g.
`{"name": "plum pits", "url": "https://SUBDOMAIN.substack.com/feed"}`

## If a newsletter shows nothing
Check the Actions run log. Substack sometimes refuses requests from cloud servers. The script keeps the last good posts for that newsletter, so the page doesn't go blank. If it keeps failing, run `python fetch_feeds.py` on your own computer and upload the new `data.json`.
