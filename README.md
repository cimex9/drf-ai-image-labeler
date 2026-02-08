# DRF AI Image Labeler

[//]: # (You found an easter egg!)

# Notes
Use `moondream:1.8b` from Ollama as an initial model.

# TODO
## General
- Define TODOs.
- README.md.
- Configure logging.
- Add a Dockerfile (will need to configure static files handling beforehand).
- Create helm charts.
  Note: DB migration init-container is needed.
- (?) Remove TEMPLATES settings.
- (?) An interactive first-time project setup Django CLI utility.
- (?) Add ollama image pulling via optional 'dev' group dependency.
  In a CLI command probably + with a suggested tested list of models.
- (?) (low priority) GitHub actions workflows.

## Batch jobs
- Setup Celery + Redis.
- (?) Initialize workers in docker-compose.yml.
- ...

## API
- Setup DRF.
- Labels search.
- Export processed images endpoint.
- Tasks related endpoints.
- ...


## Testing
- Add unit tests.
- Add integration tests (with a selected Ollama model).
- Setup Allure reports.
- Setup code coverage.
