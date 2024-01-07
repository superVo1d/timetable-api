install:
	$(shell ./make_env.sh)
	pip3 install -r requirements.txt

start:
	uvicorn app.main:app --port 8000 --reload

freeze:
	pip3 list --format=freeze > requirements.txt