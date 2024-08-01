create_network:
	docker network create inventory_system_network

upgrade_alembic_head:
	docker compose -f .//docker//docker-compose.yml run --remove-orphans inventory_system_api alembic upgrade head

remove_db_volume:
	sudo rm -rf .//..//msd_db_mount_location
	mkdir .//..//msd_db_mount_location

generate_revision:
	make upgrade_alembic_head
	docker compose -f .//docker//docker-compose.yml run --remove-orphans inventory_system_api alembic revision --autogenerate

build_app_image:
	docker build -t inventory_system .

start_app:
	docker compose -f .//docker//docker-compose.yml up -d

stop_app:
	docker compose -f .//docker//docker-compose.yml down --remove-orphans 

follow_app_log:
	docker logs -f inventory_system

follow_app_frontend_log:
	docker logs -f inventory_system_frontend