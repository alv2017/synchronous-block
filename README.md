# Async Friendly Functions Project: Synchronous Block

`Synchronous Block` is a small Fast-API authentication app that implements synchronous password hashing.
We will use it to solve the task `Observe blocking behavior` from the `Async Friendly Functions` project.

## Running the Application Locally

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

## Password Hashing Function

The password hashing function can be found at api/apps/auth/passwords.py


## Endpoints

This is a standard Fast-API application hence the edpoints can be foud at the `/docs` endpoint.