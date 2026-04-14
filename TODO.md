# TODO (done items not included)
## General
- Define TODOs.
- README.md.
- Configure logging. See: https://docs.djangoproject.com/en/6.0/topics/logging/.
- Add a Dockerfile (will need to configure static files handling beforehand).
- Migrate to langchain instead of manual REST API calling (+ support multiple VLM providers).
- Create helm charts.
  Note: DB migration init-container is needed.
- Remove TEMPLATES settings.
- Django management command for an interactive first-time project setup.
- Add ollama image pulling via optional 'dev' group dependency.
  In a CLI command probably + with a suggested tested list of models.

## Batch jobs
- Setup Celery + Redis.
- Initialize workers in docker-compose.yml for dev purposes.
- ...

## API
- Search images by labels.
- Export processed images endpoint.
- Tasks related endpoints.
- ...


## Testing
- Add integration tests (with a selected Ollama model).
- Setup Allure reports.
- Setup code coverage.
