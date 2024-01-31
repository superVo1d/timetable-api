install:
	$(shell ./make_env.sh)
	pip install -r requirements.txt

start:
	uvicorn app.main:app --port 8000 --reload

freeze:
	pip list --format=freeze > requirements.txt