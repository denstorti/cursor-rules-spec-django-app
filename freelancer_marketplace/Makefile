.PHONY: run migrations stop clean shell superuser test

# Start the app and run migrations
run:
	docker-compose down
	docker-compose up -d
	docker-compose exec web python manage.py migrate

# Create migrations
migrations:
	docker-compose exec web python manage.py makemigrations $(app)

# Create migrations for a specific app
# Usage: make app-migrations app=jobs
app-migrations:
	docker-compose exec web python manage.py makemigrations $(app)

# Stop containers
stop:
	docker-compose down

# Remove containers and volumes
clean:
	docker-compose down -v
	docker-compose rm -f

# Access Django shell
shell:
	docker-compose exec web python manage.py shell

# Create superuser
superuser:
	docker-compose exec web python manage.py createsuperuser

# Run tests
test:
	docker-compose exec web python manage.py test $(app)

# Help
help:
	@echo "Available commands:"
	@echo "  make run              - Start the app and run migrations"
	@echo "  make migrations       - Create migrations for all apps"
	@echo "  make app-migrations   - Create migrations for a specific app (e.g., make app-migrations app=jobs)"
	@echo "  make stop             - Stop containers"
	@echo "  make clean            - Remove containers and volumes"
	@echo "  make shell            - Access Django shell"
	@echo "  make superuser        - Create superuser"
	@echo "  make test             - Run tests (e.g., make test app=jobs)" 