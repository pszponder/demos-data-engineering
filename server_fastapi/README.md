# FastAPI

## Running with Docker

This project includes a Docker setup for running the FastAPI application in a containerized environment.

- **Python version:** 3.13 (as specified in the Dockerfile)
- **Dependencies:** Managed via `pyproject.toml` and `uv.lock`, installed using [uv](https://github.com/astral-sh/uv) in a virtual environment
- **Exposed port:** 8000 (FastAPI default)
- **Environment variables:**
    - You may use a `.env` file for environment variables. An example is provided as `.env.example`.

### Build and Run

To build and start the application using Docker Compose:

```sh
# Build and run the FastAPI app
docker compose up --build
```

The application will be available at [http://localhost:8000](http://localhost:8000).

- The container runs as a non-root user for improved security.
- No external services (databases, caches) are required or configured by default.
- No persistent volumes or custom networks are defined.

If you need to set environment variables, copy `.env.example` to `.env` and adjust as needed, then uncomment the `env_file` line in `docker-compose.yml`.

## Resources / References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [NeuralNine - FastAPI Full Crash Course](https://youtu.be/rvFsGRvj9jo?si=_4Mic5NmL__LH9vE)
