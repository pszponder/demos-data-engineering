# MinIO S3-Compatible Storage

This directory contains a dockerized MinIO setup that simulates AWS S3 for local development and testing.

## Quick Start

```bash
# Start MinIO
make up

# Check status
make status

# Watch logs
make logs

# Stop MinIO
make down
```

## What's Included

- **MinIO Server**: S3-compatible object storage server
- **MinIO Console**: Web-based administration interface
- **MinIO Client (mc)**: Automatically creates a demo bucket on startup
- **Persistent Storage**: Data persists between container restarts

## Access Information

After running `make up`, you'll have access to:

- **MinIO API**: http://localhost:9000 (S3-compatible endpoint)
- **MinIO Console**: http://localhost:9001 (Web UI)
- **Default Credentials**: minioadmin / minioadmin123
- **Default Bucket**: `demo-bucket` (created automatically)

## Configuration

Environment variables are stored in `.env`:

```bash
# MinIO ports
MINIO_PORT=9000
MINIO_CONSOLE_PORT=9001

# Credentials
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123

# S3 API configuration for your apps
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY_ID=minioadmin
S3_SECRET_ACCESS_KEY=minioadmin123
S3_REGION=us-east-1
S3_BUCKET_NAME=demo-bucket
```

## Using with Python (boto3)

```python
import boto3
from botocore.config import Config

# Configure S3 client for MinIO
s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin123',
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

# Example: Upload a file
s3_client.upload_file('local_file.txt', 'demo-bucket', 'remote_file.txt')

# Example: Download a file
s3_client.download_file('demo-bucket', 'remote_file.txt', 'downloaded_file.txt')

# Example: List objects
response = s3_client.list_objects_v2(Bucket='demo-bucket')
for obj in response.get('Contents', []):
    print(f"Object: {obj['Key']}")
```

## Available Commands

| Command | Description |
|---------|-------------|
| `make help` | Show available commands |
| `make up` | Start MinIO containers |
| `make down` | Stop MinIO containers |
| `make downall` | Stop containers and remove volumes |
| `make destroy` | Remove all Docker artifacts |
| `make logs` | Watch container logs |
| `make status` | Show container and volume status |
| `make clean` | Remove data volumes (containers must be stopped) |

## Data Persistence

- MinIO data is stored in a Docker volume named `minio_data`
- Data persists between container restarts
- Use `make clean` to remove all stored data (requires containers to be stopped)
- Use `make destroy` to remove everything including Docker images

## Security Notes

⚠️ **For Development Only**: The default credentials (`minioadmin/minioadmin123`) are for development purposes only. Change them for any production or shared environment.

## Troubleshooting

### Container Won't Start
```bash
# Check if ports are already in use
lsof -i :9000
lsof -i :9001

# View detailed logs
make logs
```

### Reset Everything
```bash
# Complete reset (removes all data!)
make destroy
make up
```

### Custom Configuration
Edit `.env` file and restart containers:
```bash
make down
# Edit .env file
make up
```
