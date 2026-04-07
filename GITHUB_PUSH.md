# GitHub Push Instructions

Repo:
https://github.com/vghattavi/suburbrank

Note: Render should use `app/requirements.txt` and `app.main:app`.

## Push from a terminal in the project directory
```bash
cd /data/.openclaw/workspace/suburbrank
git init
git branch -M main
git remote add origin https://github.com/vghattavi/suburbrank.git
git add .
git commit -m "Initial SuburbRank FastAPI MVP"
git push -u origin main
```

## If prompted for GitHub auth
Use either:
- GitHub CLI auth, or
- a personal access token, or
- browser-based auth depending on the environment

## If remote already exists
```bash
git remote set-url origin https://github.com/vghattavi/suburbrank.git
git push -u origin main
```

## If branch has no commits yet
Make sure `git add .` and `git commit` succeed before pushing.
