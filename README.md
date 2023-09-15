# Lemmy Email Checker

This script checks for disposable emails in registrations. 

# How to prepare

Install dependencies with pip install -r requirements.txt

1. Check emai.list and add / remove unwanted lists
2. Add manual domain blocklists to manual_blocklist.list
3. Run "python emailchecker/fetchList.py" ( it can take a while! )

# How to let the checker run

1. Rename .env_example to .env
2. Put your fitting values into it.
3. Run "python emailchecker/main.py"