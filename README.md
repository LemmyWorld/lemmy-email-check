# Lemmy Email Checker

This script checks for disposable emails in registrations. 

# Setup
```bash
pip install . --upgradepip install . --upgrade
```

# How to let the checker run
1. Copy emai.list to run dir
   1. Add / remove unwanted lists
2. Copy manual_blocklist.list to run dir
   1. Add manual domain blocklists to manual_blocklist.list
3. Rename .env_example to .env
4. Put your fitting values into it.
5. Run 

```bash
lemmyemailchecker
```
