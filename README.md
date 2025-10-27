# Async Friendly Functions Project: Synchronous Block

`Synchronous Block` is a small Fast-API authentication app that implements synchronous password hashing.
We will use it to solve the task `Observe blocking behavior` from the `Async Friendly Functions` project.

## 1. Running the Application Locally

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

## 2. Password Hashing Function

The password hashing function can be found at `api/apps/auth/passwords.py`

## 3. Endpoints

This is a standard Fast-API application hence the edpoints can be found at the `/docs` endpoint.

User registration endpoint: POST: `/api/register/`
Health endpoint: GET: `/api/health/`

## 4. Assignments
1) Use `hash_password` function in a FastAPI user registration endpoint. [+]
2) Implement a health-check endpoint that simply returns {"status": "OK"}.[+]
3) Measure user registration endpoint response time. [+]
4) Measure health-check endpoint response time. [+]
5) Measure registration endpoint response time when registration requests are running concurrently. Execute the experiment with 10, 100, 1000 concurrent requests. [-]
6) Measure `health` endpoint response time when running concurrently with the registration requests. [-]
7) Analyze the results: [-]
    - how the event loop behaves when blocked?
    - how responsiveness is affected under load?
    - how does the health-check endpoint behave when multiple registration requests are running concurrently? How does its response time change with concurrency?
    - how does the average response time of registration end-point change with concurrency?
8) Measure CPU and memory usage during the experiments. [-]

## 5. Solution

### 5.1. Password Hashing Function

- The password hashing function `hash_password` is located at `api/apps/auth/passwords.py`. This function is used in the user registration endpoint to hash the user's password before storing it.

- There is also password verification function `verify_password` that is used to verify the user's password during login. It is located at the same file `api/apps/auth/passwords.py`.


### 5.2. Endpoints

- User registration endpoint is implemented at `/api/users/register/`

- API health-check endpoint is implemented at `/api/health/`


### 5.3. Measuring the Response times of the `/api/users/register/` and `/api/health/` Endpoints

#### 5.3.1 Introduction

At this stage we will keep things simple and measure the endpoints response time using server side logging
middleware.

In order to measure the response time of a single endpoint we will send 100 consecutive requests to the endpoint and calculate the average response time.

The major goal at this stage is to set up correctly the server side logging.

For server side logging we will be using the `asgi-logging-middleware` package, however you can use any other package of your choice, or create a logging middleware of your own. 


#### 5.3.2 Setting up the `asgi-logging-middleware`

1) We need to install the `asgi-logging-middleware` package:

```bash
pip install asgi-logging-middleware
```

2) We will add a separate performance logger, and use it with the `AccessLoggerMiddleware`. The logger is located 
at `api/loggers/performance_logger.py`.

3) We need to add the `AccessLoggerMiddleware` middleware to the Fast-API application. To do that we need to modify the 
`api/main.py`. The modification have been done following the FastAPI documentation on adding ASGI middleware ([Adding ASGI Middlewares](https://fastapi.tiangolo.com/advanced/middleware/#adding-asgi-middlewares))  and the documentation of[asgi-logging-middleware](https://github.com/alv2017/asgi-logging-middleware) package. 


#### 5.3.3 Measuring the Response Time of the `/api/health/` Endpoint

We will create our own script that sends 100 consecutive requests to the `/api/health/` endpoint. Then we will parse the performance log file and calculate the average response time.

Essentially in our script that sends requests to the endpoint we can also measure the response time, this time on the client's side. This means that we will be able to compare the server side response time with the client side response time!

Script location: `measurements/response_times/api_health_endpoint/response_time.py`

Server log results: `measurements/response_times/api_health_endpoint/api_health_performance.log`

**Results:**

1) Server side average response time for `/api/health/` endpoint: 0.6151 ms 
2) Client side average response time for `/api/health/` endpoint: 1.8200 ms

#### 5.3.4 Measuring the Response Time of the `/api/users/register/` Endpoint

We will create our own script that sends 100 consecutive requests to the `/api/users/register/` endpoint. Then we will 
parse the performance log file and calculate the average response time. In our script we will also measure the response time on the client's side. This means that we will be able to compare the server side response time with the client side response time!

Script location: `measurements/response_times/api_register_endpoint/response_time.py`

Server log results: `measurements/response_times/api_register_endpoint/api_health_performance.log`

**Results:**

1) Server side average response time for `/api/user/register/` endpoint: 222.0682 ms
2) Client side average response time for `/api/user/register` endpoint: 223.5300 ms

### 5.3. Measuring `/api/users/register/` Endpoint Response Time Under Concurrent Load

Our next challenge is to measure the `/api/users/register/` endpoint response time when registration requests are running concurrently.

We will use `locust` to perform the load testing. [locust](https://locust.io/) is an open source load testing tool that allows you to define user behavior with Python code, and swarm your system with millions of simultaneous users. 😊

