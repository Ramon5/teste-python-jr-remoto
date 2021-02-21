run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

test:
	pytest -vv . --cov api/

test-open:
	dir=$(pwd)
	cd -
	k6 run -e API_BASE="http://localhost:8000/" /home/ramon/Workspace/Python/tech_challengers/instruct/teste-python-jr-remoto/tests-open.js 