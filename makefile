create-docker-image:
	docker build -t myapp:1.0 .

container-run:
	docker run -p 8080:80 myapp:1.0
	
create-database:
	python manage.py makemigrations && \
	python manage.py migrate

update-database-data:
	python manage.py loaddata message_service/fixtures/coupon.json && \
	python manage.py loaddata message_service/fixtures/user.json && \
	python manage.py loaddata message_service/fixtures/promotional_message.json

update-requirements:
	python -m pip install pip-tools 
	python -m piptools compile --generate-hashes requirements.in --output-file requirements.txt

requirements-install:
	pip install -r requirements.txt 

run:
	python manage.py runserver

test:
	python manage.py test
