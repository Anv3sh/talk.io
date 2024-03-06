install_backend:
	poetry lock
	poetry install
	
backend:
	uvicorn --factory src.backend.talk.main:create_app --host localhost --port 8080 --reload --log-level debug

format:
	poetry run black .
	poetry run ruff . --fix