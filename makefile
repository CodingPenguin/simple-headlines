install:
	python3 -m pip install -r requirements.txt

freeze:
	python3 -m pip freeze > requirements.txt

run:
	source env/bin/activate && source .env && pc run