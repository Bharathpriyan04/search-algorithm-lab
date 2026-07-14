# Min-Max via Divide and Conquer (User Input Version)

CS5303 – DAA Lab, Ex. No. 5. Finds the minimum and maximum of a
user-entered array using the divide-and-conquer technique, and compares
the comparison count against the naive linear-scan approach and the
theoretical formula `3n/2 - 2`.

## Files

| File | Purpose |
|---|---|
| `min_max.py` | Core algorithm. Run directly for a command-line version that reads numbers from the keyboard. |
| `app.py` | Flask web app that serves an input form and shows results in the browser. |
| `templates/index.html` | HTML page for the web form/results. |
| `requirements.txt` | Python dependencies. |
| `render.yaml` | Deployment config for Render. |
| `.gitignore` | Keeps caches/venvs out of git. |

## 1. Run it locally

Command-line version (typed input, no web browser needed):

```bash
python min_max.py
# Enter the numbers separated by spaces or commas: 3, 1, 7, 4, 9, 2, 8, 5, 6, 0
```

Web version:

```bash
pip install -r requirements.txt
python app.py
# open http://localhost:5000 in your browser
```

## 2. Push this to your own GitHub repo

Run these commands inside this folder (replace the URL with your repo):

```bash
git init
git add .
git commit -m "Min-Max divide and conquer with user input"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

If you don't have a repo yet, create one first at https://github.com/new
(don't initialize it with a README, since this folder already has one),
then run the commands above.

## 3. Deploy on Render

1. Go to https://dashboard.render.com and log in.
2. Click **New +** → **Web Service**.
3. Connect your GitHub account and select the repo you just pushed.
4. Render should auto-detect `render.yaml`. If asked to confirm settings:
   - **Environment:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Create Web Service**. Render will build and deploy automatically.
6. Once the build finishes, Render gives you a live URL like
   `https://minmax-divide-and-conquer.onrender.com` — open it to use the app.

Any future `git push` to the connected branch will trigger an automatic
redeploy on Render.
