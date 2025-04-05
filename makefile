# Makefile

# Variables
APP_MODULE=main:app  # Replace with your FastAPI app module
WORKERS=2

# Alembic commands
revision:
	alembic revision --autogenerate -m "$(name)"

migrate:
	alembic upgrade head

# Start FastAPI app with 2 workers
start:
	uvicorn $(APP_MODULE) --workers $(WORKERS)

# Phony targets
.PHONY: revision migrate start