## Project setup

Run the following command inside the root directory to install its dependencies:

```
docker-compose build
```

To run the server in development mode, use:

```
docker-compose up
```

The server runs on port 8888 by default and can be accessed at [http://localhost:8888/](http://localhost:8888/).

There are fixtures that run automatically to populate the database with initial medspas and services, besides a superuser.

The database can be easily debugged through Django admin, which is also configured and available at [http://localhost:8888/admin/](http://localhost:8888/admin/). For it, use the login and password _admin_.


## Request examples

### Service API

- GET Request

Endpoint: localhost:8888/api/v1/medspas/1/services

This request retrieves all services offered by the MedSpa with ID 1.

- POST Request

Endpoint: localhost:8888/api/v1/medspas/1/services

Request body:

{
  "name": "Botox Treatment",
  "description": "Reduces wrinkles and fine lines",
  "price": 250.00,
  "duration": "01:00:00"
}

This request creates a new service for the MedSpa with ID 1.


- PUT Request

Endpoint: localhost:8888/api/v1/medspas/1/services/1

Request body:

{
  "name": "Botox Treatment",
  "description": "Considerably reduces wrinkles and fine lines",
  "price": 250.00,
  "duration": "00:50:00"
}

This request updates the service with ID 1 for the MedSpa with ID 1.


### Appointment API

- GET Request

Endpoint: localhost:8888/api/v1/medspas/1/appointments

This request retrieves all appointments offered by the MedSpa with ID 1.

- POST Request

Endpoint: localhost:8888/api/v1/medspas/1/appointments

Not fully implemented.


- PUT Request

Endpoint: localhost:8888/api/v1/medspas/1/appointments/1

Not fully implemented.
