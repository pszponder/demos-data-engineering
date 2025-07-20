# Apache Airflow Docker Setup

This repository contains a Docker Compose setup for running Apache Airflow locally with PostgreSQL, Redis, and Flower monitoring.

## 🏗️ Architecture

- **Airflow Web UI**: http://localhost:8080
- **Flower Monitoring**: http://localhost:5555
- **Database**: PostgreSQL
- **Message Broker**: Redis
- **Executor**: CeleryExecutor

## 🚀 Quick Start

### 1. Initial Setup

First, copy the example environment file and customize it:

```bash
cp .env.example .env
```

Edit `.env` and set your preferred admin username and password:

```bash
# Custom admin user credentials (CHANGE THESE!)
_AIRFLOW_WWW_USER_USERNAME=your_admin_username
_AIRFLOW_WWW_USER_PASSWORD=your_secure_password
```

### 2. Initialize Airflow

Initialize the database and create the admin user:

```bash
make init
```

### 3. Start Services

Start all Airflow services including Flower monitoring:

```bash
make start
```

After starting, you can access:
- **Airflow Web UI**: http://localhost:8080
- **Flower Monitoring**: http://localhost:5555

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `make init` | Initialize Airflow database and create admin user |
| `make start` | Start Airflow services including Flower monitoring |
| `make stop` | Stop all Airflow services including Flower |
| `make clean` | Complete cleanup: stop services, remove volumes and images |
| `make user-create` | Create a new Airflow user interactively |
| `make user-delete` | Delete an existing Airflow user |
| `make user-list` | List all Airflow users |
| `make help` | Show available commands |

## 👥 User Management

### Default Admin User

The default admin user is created during initialization using credentials from your `.env` file:
- Username: Set via `_AIRFLOW_WWW_USER_USERNAME`
- Password: Set via `_AIRFLOW_WWW_USER_PASSWORD`

### Creating Additional Users

Use the interactive user creation command:

```bash
make user-create
```

This will prompt you for:
1. **Role selection**: Admin, User, Op, or Viewer
2. **User details**: Username, first name, last name, email
3. **Password**: Securely entered (hidden input)

### User Roles Explained

| Role | Permissions |
|------|-------------|
| **Admin** | Full administrative access - can manage users, connections, configurations |
| **User** | Can view and edit DAGs, tasks, connections |
| **Op** | Can view DAGs and task instances, trigger DAG runs |
| **Viewer** | Read-only access to DAGs and task instances |

### Managing Existing Users

List all users:
```bash
make user-list
```

Delete a user:
```bash
make user-delete
```

## 📁 Directory Structure

```
airflow/
├── dags/           # Your DAG files go here
├── logs/           # Airflow logs
├── plugins/        # Custom Airflow plugins
├── config/         # Airflow configuration files
├── docker-compose.yaml
├── Makefile
├── .env           # Your environment variables (not committed)
├── .env.example   # Example environment file
└── README.md
```

## 🔧 Configuration

### Environment Variables

Key environment variables in `.env`:

- `AIRFLOW_UID`: User ID for Airflow containers (should match your system user ID)
- `_AIRFLOW_WWW_USER_USERNAME`: Default admin username
- `_AIRFLOW_WWW_USER_PASSWORD`: Default admin password
- `_PIP_ADDITIONAL_REQUIREMENTS`: Additional Python packages to install

### Customizing Airflow Configuration

You can customize Airflow by:

1. **Environment variables**: Add Airflow config variables to `.env`
   ```bash
   AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=false
   AIRFLOW__WEBSERVER__EXPOSE_CONFIG=true
   ```

2. **Configuration file**: Place custom `airflow.cfg` in the `config/` directory

3. **Custom image**: Build a custom Docker image with your requirements

## 🛠️ Development Workflow

### Adding DAGs

1. Place your DAG files in the `dags/` directory
2. They will be automatically detected by Airflow
3. Refresh the web UI to see new DAGs

### Installing Additional Packages

**Option 1: Environment variable (for testing)**
```bash
# Add to .env file
_PIP_ADDITIONAL_REQUIREMENTS=pandas==1.5.0 requests==2.28.0
```

**Option 2: Custom Docker image (recommended for production)**
1. Create a `Dockerfile`
2. Extend the official Airflow image
3. Build and use your custom image

### Accessing Logs

Logs are stored in the `logs/` directory and can be viewed:
- Through the Airflow Web UI
- Directly in the filesystem
- Using `docker compose logs [service-name]`

## 🐛 Troubleshooting

### Common Issues

**1. Permission Issues**
- Make sure `AIRFLOW_UID` in `.env` matches your system user ID
- Run: `echo $UID` to get your user ID

**2. Services Won't Stop Properly**
- Use `make clean` for complete cleanup
- Check for running containers: `docker ps`

**3. Database Connection Issues**
- Ensure PostgreSQL service is healthy: `docker compose ps`
- Check logs: `docker compose logs postgres`

**4. Web UI Not Accessible**
- Verify services are running: `docker compose ps`
- Check port conflicts: `lsof -i :8080`

### Viewing Logs

```bash
# View all service logs
docker compose logs

# View specific service logs
docker compose logs airflow-scheduler
docker compose logs postgres
docker compose logs redis
```

### Resetting Everything

To completely reset your Airflow setup:

```bash
make clean
# Remove local files if needed
sudo rm -rf logs/*
make init
make start
```

## 🔒 Security Considerations

1. **Change default passwords**: Always customize credentials in `.env`
2. **Don't commit `.env`**: The file contains sensitive information
3. **Use strong passwords**: Especially for admin users
4. **Regular backups**: Backup your DAGs and important configurations
5. **Network access**: Restrict access to ports 8080 and 5555 in production

## 📚 Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Docker Compose for Airflow](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Writing DAGs](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 Notes

- This setup is intended for **local development and testing**
- For production deployment, additional security and scaling considerations are needed
- Flower monitoring provides real-time task execution monitoring
