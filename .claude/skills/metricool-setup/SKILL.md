---
name: metricool-setup
description: Use this skill whenever the user wants to set up the Metricool API, get their Metricool API key, find their user ID or blog ID, connect Claude to Metricool, or asks how to access their Metricool credentials. Trigger on phrases like "set up Metricool API", "get my Metricool token", "connect to Metricool", "find my Metricool user ID", or any first-time Metricool API setup request.
---

# Metricool API — Setup Walkthrough

This skill walks the user step-by-step through getting their three Metricool credentials so they can use the API.

The end state is a `.env` file containing:

```
METRICOOL_USER_TOKEN=...
METRICOOL_USER_ID=...
METRICOOL_BLOG_ID=...
```

Once those exist, the user can use them with any Metricool API tool or script.

---

## How to run this walkthrough

Go through the steps below in order. After each step, wait for the user to confirm before moving to the next. Be patient — most users have never touched an API before.

### Step 0 — Paid plan check

**Tell the user:**

> "The Metricool API is only available on paid plans (Starter tier or higher). If you're on the free tier, the API won't work. Open https://metricool.com/pricing in a tab and confirm you're on Starter or above. Are you?"

If they say no, stop here. Tell them: *"Upgrade first, then come back and we'll continue."*

If yes, continue.

### Step 1 — Get the User Token

**Tell the user:**

> "Now let's get your API token.
>
> 1. Log into https://app.metricool.com
> 2. Click your avatar in the top-right corner → **My Profile**
> 3. Scroll down to the **API access** section
> 4. Click **Generate token** (or copy the existing one if it's already there)
> 5. Paste the long token string back to me here in chat."

Wait for them to paste the token. It will look something like a 60-character string of uppercase letters.

When they paste it, save it as `METRICOOL_USER_TOKEN`.

### Step 2 — Get the User ID

**Tell the user:**

> "Now your User ID. This is the numeric ID Metricool assigns to your account. Easiest way to find it:
>
> - Stay on the My Profile page from before
> - Look for the **User ID** field (it's a number, usually 7 digits)
> - Or check the URL after you log in — it'll look like `https://app.metricool.com/<number>/...` — that number is your User ID
>
> Paste it here."

When they paste it, save it as `METRICOOL_USER_ID`.

### Step 3 — Get the Blog ID

**Tell the user:**

> "Last one. In Metricool, a 'Blog' is one brand workspace. If you only manage one brand, you only have one Blog ID. If you manage several (agency setup), pick the one you want this skill to work with.
>
> Easiest way to find it:
>
> 1. Open https://app.metricool.com and select the brand you want
> 2. Look at the URL — it'll show `blogId=<number>` somewhere, usually after `?`
> 3. Or go to **Settings → Brand** and the ID is shown there
>
> Paste the number here."

When they paste it, save it as `METRICOOL_BLOG_ID`.

### Step 4 — Write the .env file

Once you have all three values, ask the user where they want to save the credentials. Default: in the current working directory, in a file called `.env`.

Write the file like this:

```
METRICOOL_USER_TOKEN=<the token they pasted>
METRICOOL_USER_ID=<the user id they pasted>
METRICOOL_BLOG_ID=<the blog id they pasted>
```

Confirm to the user: *"Done. Your credentials are saved at `<path>`. Anything that needs Metricool API access can now read them from there. Never share this file or commit it to git — it has full write access to your Metricool account."*

### Step 5 — Verify it works

**Tell the user:**

> "Want me to test the connection to make sure everything's right?"

If yes, run this Python snippet (or write it to a file and run it) — it hits a known-good Metricool endpoint and reports back:

```python
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # reads the .env we just wrote

token = os.environ["METRICOOL_USER_TOKEN"]
user_id = os.environ["METRICOOL_USER_ID"]
blog_id = os.environ["METRICOOL_BLOG_ID"]

r = requests.get(
    "https://app.metricool.com/api/admin/simpleProfiles",
    params={"userToken": token},
    timeout=30,
)
if not r.ok:
    print(f"✗ Connection failed: {r.status_code} {r.text[:200]}")
else:
    brands = r.json() if isinstance(r.json(), list) else r.json().get("data", [])
    print(f"✓ Auth works. {len(brands)} brand(s) on this account:")
    for b in brands:
        bid = b.get("id") or b.get("blogId")
        label = b.get("label") or b.get("url") or "(no name)"
        marker = "  ← current METRICOOL_BLOG_ID" if str(bid) == str(blog_id) else ""
        print(f"  • {bid}  {label}{marker}")
```

If the user doesn't have `requests` and `python-dotenv` installed, tell them to run:

```bash
pip install requests python-dotenv
```

If it prints ✓ and shows their brand, setup is complete. If not, troubleshoot:

- **401 or 403:** the token is wrong or expired. Go back to Step 1 and regenerate.
- **Empty brand list:** the token is for a different account than expected. Double-check Step 1.
- **Blog ID not in the list:** they grabbed the wrong number in Step 3. Try the ones from the printed list.

---

## What's next (tell the user this once setup is complete)

> "You're set. From here you can use the Metricool API to schedule posts, batch-upload content, pull analytics — whatever the API exposes. Common next moves:
>
> - Schedule a single post (one image + caption + time + platforms)
> - Batch-schedule a folder of media on a cadence (e.g. one every 6 hours)
> - List all your scheduled posts for the next 30 days
>
> Just tell me what you want to do."

---

## Important — the `media` field gotcha

If the user moves on to creating posts (not part of *this* skill, but in case they ask):

When creating a post via `POST /api/v2/scheduler/posts`, the `media` field MUST be a list of plain URL strings:

- ✅ `"media": ["https://...png", "https://...png"]`
- ❌ `"media": [{"url": "https://...png"}]` — returns 200 OK but the post is created with **zero media**, silently

This is a Metricool API quirk that costs hours if you don't know.

## Don'ts

- Don't print the API token in full once it's stored — show last 4 characters only if you need to confirm it.
- Don't commit the `.env` file to git.
- Don't proceed past Step 0 if the user is on the free tier.
