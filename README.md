# DRF AI Image Labeler

**Status:** In Development (see [TODO.md](./TODO.md) for remaining work)

A Django REST Framework service for batch image labeling using AI. Upload images and the system asynchronously processes
them using Vision Language Models (via Celery/Redis), generating labels using VLM models that are stored and linked in PostgreSQL.

### Example

Upload an image of a dog, so then VLM generates labels like: `dog, smile, golden retriever`

These AI-generated labels enable workflows like:
- **LoRA model training** - Use labeled images to fine-tune custom diffusion models
- **Image search & filtering** - Find images by semantic labels
- **Dataset organization** - Automatically categorize and tag large image collections


## Installation

### Prerequisites
- Python 3.13.x
- Docker & Docker Compose
- PDM package manager

### Quick Start

After cloning the repository make sure to create a new `.env` file out of `.default.env` in the project root:
```bash
cp .default.env .env
```

Edit `.env` with your credentials.
Main 2 variables to focus on:
```dotenv
# VLM_PROVIDER could be anything (like, gemini, openai, aws-bedrock, etc.), but currently only ollama is supported
VLM_PROVIDER=ollama
VLM_MODEL=moondream:1.8b
```

**Install dependencies**:
```bash
pdm sync --prod --clean  # for runtime deps only
# or
pdm sync --clean  # runtime + dev dependencies
```

**Start services:**
```bash
pdm run dc up  # Start Docker services (PostgreSQL, MinIO, Redis, Celery workers)
```
About `dc` PDM script:
```toml
dc.help = "Utility PDM script which runs `docker compose` after populating environment variables from .env file."
dc.cmd = "docker compose"
dc.env_file = ".env"
```
It reads the root `.env` file for the necessary credentials.


**Run migrations and initialize storage:**
```bash
pdm run migrate
pdm run init_s3_storage
```

**Start the development server:**
```bash
pdm run server
```

The API will be available at `http://localhost:8000/`

## Development Commands

Get the full list of available commands explained with help messages:
```bash
pdm run --list
```

### Code Quality
```bash
pdm run lint           # Check code with ruff
pdm run lint-fix       # Auto-fix linting issues
pdm run isort .        # Sort imports
pdm run unit_tests     # Run pytest tests
```

### Database
```bash
pdm run makemigrations # Create migrations
pdm run migrate        # Apply migrations
pdm run shell          # Django interactive shell
```

## Technologies Used
- **Django + Django REST Framework** - REST API
- **PostgreSQL** - Primary database
- **Celery + Redis** - Asynchronous task processing
- **Ollama** - Vision Language Model provider
- **MinIO/S3** - Object storage
- **PDM** - Python package management
