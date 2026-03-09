# FPL Draft League Tracker

A free, hosted web app that shows your FPL Draft league standings in near real-time.

## Deploy to Render (free) — Step by Step

### Step 1: Create a GitHub account (if you don't have one)
Go to https://github.com and sign up for free.

### Step 2: Create a new GitHub repository
1. Click the **+** icon (top right) → **New repository**
2. Name it `fpl-tracker`
3. Set it to **Public**
4. Click **Create repository**

### Step 3: Upload the files
On your new repo page, click **uploading an existing file** and upload ALL of these files:
- `app.py`
- `requirements.txt`
- `Procfile`
- The `static/` folder containing `index.html`

(Make sure `static/index.html` is inside a folder called `static`)

Commit the files.

### Step 4: Create a Render account
Go to https://render.com and sign up for free (use "Sign in with GitHub" — easiest).

### Step 5: Create a new Web Service on Render
1. Click **New +** → **Web Service**
2. Connect your GitHub account if prompted
3. Select your `fpl-tracker` repository
4. Fill in the settings:
   - **Name**: fpl-tracker (or anything you like)
   - **Region**: pick closest to you (e.g. Frankfurt for UK)
   - **Branch**: main
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free

### Step 6: Add your credentials as Environment Variables
Still on the Render setup page, scroll to **Environment Variables** and add:

| Key | Value |
|-----|-------|
| `FPL_EMAIL` | your FPL login email |
| `FPL_PASSWORD` | your FPL password |
| `LEAGUE_ID` | 86512 |

### Step 7: Deploy!
Click **Create Web Service**. Render will build and deploy your app (takes ~2 minutes).

Once done, you'll get a URL like `https://fpl-tracker-xxxx.onrender.com` — share this with your league!

## Notes
- The free Render tier "sleeps" after 15 minutes of inactivity — the first load after a period of inactivity may take 30–60 seconds to wake up. Subsequent loads are instant.
- To keep it always awake, you can use a free service like https://uptimerobot.com to ping your URL every 10 minutes.
- Your credentials are stored securely as environment variables in Render — they are never in your code.
