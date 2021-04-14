# tm-api
 - Basic REST API for Noyo Challenge

# Usage
 - Run app locally: `docker-compose up`
   - Swagger UI: `http://localhost:5000/api/ui/`
   - Run tests: `pytest -v tests`

# Things to Add/Improve
 - JWT authentication layer
 - data validation (e.g. email addresses)
 - response filtering, sorting, pagination
 - API users and permission roles
 - caching
 - rate-limiting
 - monitoring w/ grafana and influx
 - remove credentials from code, place in secrets manager
 - logging
 - pytest-docker-compose to spin up/tear down test containers