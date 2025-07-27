FROM apache/airflow:3.0.3

# # Copy pyproject.toml to install dependencies
COPY pyproject.toml ./

# # Install Python dependencies individually
# RUN uv pip install --no-cache "requests>=2.32.4"
# RUN uv pip install --no-cache "boto3>=1.34.0"
# RUN uv pip install --no-cache "botocore>=1.34.0"

# Sync non-dev dependencies and symlink .venv with path
# TODO: In the future, may be able to use `uv sync --no-dev --no-cache --system`
RUN uv sync --no-dev --no-cache
RUN export PATH="$(pwd)/.venv/bin:$PATH"
