.PHONY: init start stop clean user-create user-delete user-list help

# Default target - show help when just typing 'make'
default: help

# Initialize Airflow database and create admin user
init:
	docker compose up airflow-init

# Start Airflow services including Flower monitoring
start:
	docker compose --profile flower up -d --remove-orphans
	@echo -e "\n🚀 Airflow services are starting up..."
	@echo "📊 Airflow Web UI: http://localhost:8080"
	@echo "🌸 Flower monitoring: http://localhost:5555"

# Stop all Airflow services
stop:
	docker compose --profile flower down

# Complete cleanup: stop services, remove volumes and images
clean:
	docker compose --profile flower down --volumes --rmi all
	rm -rf logs/
	@echo "🧹 Cleaned up Docker resources and logs"

# Create a new Airflow user interactively
user-create:
	@echo "🔐 Creating new Airflow user..."
	@echo "Available roles:"
	@echo "  1) Admin   - Full administrative access"
	@echo "  2) User    - Can view and edit DAGs, tasks"
	@echo "  3) Op      - Can view DAGs, trigger runs"
	@echo "  4) Viewer  - Read-only access"
	@read -p "Select role (1-4): " role_choice; \
	case $$role_choice in \
		1) role="Admin" ;; \
		2) role="User" ;; \
		3) role="Op" ;; \
		4) role="Viewer" ;; \
		*) echo "❌ Invalid choice. Exiting."; exit 1 ;; \
	esac; \
	read -p "Enter username: " username; \
	read -p "Enter first name: " firstname; \
	read -p "Enter last name: " lastname; \
	read -p "Enter email: " email; \
	read -s -p "Enter password: " password; \
	echo; \
	docker compose exec airflow-scheduler airflow users create \
		--username "$$username" \
		--firstname "$$firstname" \
		--lastname "$$lastname" \
		--role "$$role" \
		--email "$$email" \
		--password "$$password" && \
	echo "✅ User '$$username' created successfully with role '$$role'"

# Delete an Airflow user
user-delete:
	@echo "🗑️  Deleting Airflow user..."
	@echo "Current users:"
	@docker compose exec airflow-scheduler airflow users list
	@read -p "Enter username to delete: " username; \
	read -p "Are you sure you want to delete user '$$username'? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		docker compose exec airflow-scheduler airflow users delete --username "$$username" && \
		echo "✅ User '$$username' deleted successfully"; \
	else \
		echo "❌ Operation cancelled"; \
	fi

# List all Airflow users
user-list:
	@echo "👥 Current Airflow users:"
	@docker compose exec airflow-scheduler airflow users list

# Show help information
help:
	@echo "Available commands:"
	@echo "  init        - Initialize Airflow database and create admin user"
	@echo "  start       - Start Airflow services including Flower monitoring"
	@echo "  stop        - Stop all Airflow services including Flower"
	@echo "  clean       - Complete cleanup: stop services, remove volumes and images"
	@echo "  user-create - Create a new Airflow user interactively"
	@echo "  user-delete - Delete an existing Airflow user"
	@echo "  user-list   - List all Airflow users"
	@echo "  help        - Show this help message"
