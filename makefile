create_network:
	docker network create inventory_system_network

upgrade_alembic_head:
	docker compose -f .//docker//docker-compose.yml run --remove-orphans inventory_system_api alembic upgrade head

generate_revision:
	docker compose -f .//docker//docker-compose.yml run --remove-orphans inventory_system_api alembic revision --autogenerate

build_app_api:
	docker build -t inventory_system_api .//src//backends

build_app_frontend:
	docker build -t inventory_system_frontend .//src//frontend

start_app:
	docker compose -f .//docker//docker-compose.yml up -d

stop_app:
	docker compose -f .//docker//docker-compose.yml down --remove-orphans 

start_app_frontend:
	docker compose -f .//docker//docker-compose.yml up -d

follow_app_log:
	docker logs -f inventory_system_api

follow_app_frontend_log:
	docker logs -f inventory_system_frontend
	docker logs -f inventory_system
