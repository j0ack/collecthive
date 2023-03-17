MAKEFLAGS+="-j 2"

FLASK_DEV=FLASK_APP="collecthive.app:create_app('dev')"

init:
	pip install -r requirements.txt
	@npm --prefix "static/vue" install

dev-python:
	$(FLASK_DEV) flask run

dev-vue:
	@npm run --prefix "static/vue" build:dev

dev: dev-python dev-vue

prod-python:
	echo "You must implement your production service here"
	exit 1

prod-vue:
	@npm run --prefix "static/vue" build

prod: prod-vue prod-python

test-python:
	@python3 -m pytest tests

test-vue:
	@npm run --prefix "static/vue" test:unit
