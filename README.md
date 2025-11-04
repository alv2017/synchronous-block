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
5) Measure registration endpoint response time when registration requests are running concurrently. [+]
6) Measure `health` endpoint response time when running concurrently with the registration requests. [+]
7) Analyze the results: [-]
    - how the event loop behaves when blocked?
    - how responsiveness is affected under load?
    - how does the health-check endpoint behave when multiple registration requests are running concurrently? 
    - how does its response time change with concurrency?
    - how does the average response time of registration end-point change with concurrency?
8) Measure CPU and memory usage during the experiments. [-]

## 5. Solution

### 5.1. Password Hashing Function

- The password hashing function `hash_password` is located at `api/apps/auth/passwords.py`. This function is used in 
the user registration endpoint to hash the user's password before storing it.

- There is also password verification function `verify_password` that is used to verify the user's password during 
login. It is located at the same file `api/apps/auth/passwords.py`.


### 5.2. Endpoints

- User registration endpoint is implemented at `/api/users/register/`

- API health-check endpoint is implemented at `/api/health/`


### 5.3. Measuring the Response times of the `/api/users/register/` and `/api/health/` Endpoints

#### 5.3.1 Introduction

At this stage we will keep things simple and measure the endpoints response time using server side logging
middleware.

In order to measure the response time of a single endpoint we will send 100 consecutive requests to the endpoint and 
calculate the average response time.

The major goal at this stage is to set up correctly the server side logging.

For server side logging we will be using the `asgi-logging-middleware` package, however you can use any other package 
of your choice, or create a logging middleware of your own. 


#### 5.3.2 Setting up the `asgi-logging-middleware`

1) We need to install the `asgi-logging-middleware` package:

```bash
pip install asgi-logging-middleware
```

2) We will add a separate performance logger, and use it with the `AccessLoggerMiddleware`. The logger is located 
at `api/loggers/performance_logger.py`.

3) We need to add the `AccessLoggerMiddleware` middleware to the Fast-API application. To do that we need to modify the 
`api/main.py`. The modification have been done following the FastAPI documentation on adding ASGI middleware 
([Adding ASGI Middlewares](https://fastapi.tiangolo.com/advanced/middleware/#adding-asgi-middlewares))  and the documentation of[asgi-logging-middleware](https://github.com/alv2017/asgi-logging-middleware) package. 


#### 5.3.3 Measuring the Response Time of the `/api/health/` Endpoint

We will create our own script that sends 100 consecutive requests to the `/api/health/` endpoint. Then we will parse 
the performance log file and calculate the average response time.

Essentially in our script that sends requests to the endpoint we can also measure the response time, this time on the 
client's side. This means that we will be able to compare the server side response time with the client side response 
time!

Script location: `measurements/response_times/api_health_endpoint/response_time.py`

Server log results: `measurements/response_times/api_health_endpoint/api_health_performance.log`

**Results:**

1) Server side average response time for `/api/health/` endpoint: 0.6151 ms 
2) Client side average response time for `/api/health/` endpoint: 1.8200 ms

#### 5.3.4 Measuring the Response Time of the `/api/users/register/` Endpoint

We will create our own script that sends 100 consecutive requests to the `/api/users/register/` endpoint. Then we will 
parse the performance log file and calculate the average response time. In our script we will also measure the response 
time on the client's side. This means that we will be able to compare the server side response time with the client side 
response time!

Script location: `measurements/response_times/api_register_endpoint/response_time.py`

Server log results: `measurements/response_times/api_register_endpoint/api_health_performance.log`

**Results:**

1) Server side average response time for `/api/user/register/` endpoint: 222.0682 ms
2) Client side average response time for `/api/user/register` endpoint: 223.5300 ms

### 5.3.5 Measuring `/api/users/register/` Endpoint Response Time Under Concurrent Load

#### 5.3.5.1 Introduction

Our next challenge is to measure the `/api/users/register/` endpoint response time when registration requests are 
running concurrently. 

We will use `locust` to perform the load testing. [locust](https://locust.io/) is an open source load testing tool that allows to 
define user behavior with Python code, and swarm your system with millions of simultaneous users. 

In this project everything is supposed to be executed locally. First, we need to understand how do the things
work, and then we can think about Docker and cloud deployments.

The plan for the task is the following:

- Run the experiments with different number of workers: 1, 2, and 4. Do not hesitate to change the number of workers
depending on your needs.
- Run the experiments with 1, 5, 10, 15, and 20 concurrent users for various number of workers. Again do not hesitate
to change those numbers whenever you find it reasonable.
- Remember, our main goal in this exercise is to observe how the blocking function affects the performance of our 
FastAPI application. 

#### 5.3.5.2 `locust` Setup

1) First of all we need to install `locust`, if you use pip:
```bash
pip install locust
```

2) Next we need to add a `locustfile` containing a test scenario.
`locustfile` location for `/api/user/register` endpoint: `measurements/concurrency/api_register_endpoint/locustfile.py`

3) Finally, we need to execute our test scenario. I was using `locust` UI to setup the number of concurrent users, the host,
and the test duration time.

You can start `locust` by pointing out to your `locustfile`:

```bash
locust -f <your-locust-scenario-location> 
```

I our particular this command becomes as follows:

```bash
locust -f measurements/concurrency/api_register_endpoint/locustfile.py
```

As the `locust` starts the UI can be accessed via a web browser at `http://localhost/8089`.
In the `locust` UI you can define the test settings: number of concurrent users, number of new users per second,
an API host, and a test duration time. As soon as you are ready click the ENTER button.

#### 5.3.5.3 Results 

Results file location: `measurements/concurrency/api_register_endpoint/results.csv`

We start with 1 worker and 1 user (no concurrency).
- The average response time is around 243 ms. 

Increasing the number of users to 5 revealed the impact of the blocking password hashing function.
- The average response time rose to 936 ms, demonstrating that concurrent requests begin to queue behind 
the blocking operation.

As we kept increasing the number of users, the `registration` endpoint performance degraded. 
- When we reached 20 users with 1 worker the average response time was around 4.2 seconds, and we started observing 
failing requests. 
- The requests failed due to database locking. 
- In the current setup we are using SQLite database, and it doesn't handle concurrent writes very well, 
especially when multiple requests attempt to write to the database simultaneously.

Increasing the number of workers improved performance: 
- With 4 workers and 5 users, the average response time dropped to 267 ms.
- However, keeping the number of workers fixed to 4, and increasing the number of users resulted in performance
degradation, though it was not as severe as with 1 worker.

**Conclusions**
- The system performs well when the number of concurrent users is approximately equal to the number of workers.
- When the number of users exceeds the number of workers, the blocking password hashing function causes requests 
to queue, leading to higher latency and, in extreme cases, database lock errors.

### 5.3.6 Measuring `/api/health/` Endpoint Response Time Under Concurrent Load

#### 5.3.6.1 Introduction

In this task we will measure the `health` endpoint response time when running concurrently with the registration requests.
We will use `locust` to perform the load testing.

The plan for the experiment is the following:

We will create a test scenario in locust that will simulate user access to both the `/api/users/register/` and 
`/api/health/` endpoints. The frequency of requests to the `/api/users/register/` endpoint will be approximately 5 times 
higher than that to the `/api/health/` endpoint. By doing this we want to simulate a system performing blocking
operations of high CPU intensity. Our goal is to observe how the blocking operations affect the responsiveness of the 
`/api/health/` endpoint, which is expected to be lightweight and fast.

Our plan is pretty much the same as for the previous task:

- Run the experiments with different number of workers: 1, 2, and 4. Do not hesitate to change the number of workers
depending on your needs.
- Run the experiments with 1, 5, 10, 15, and 20 concurrent users for various number of workers. Do not hesitate
to change those numbers whenever you find it reasonable.
- Our main goal is to observe how the blocking function affects the performance of our FastAPI application. 
In this particular case we want to observe how the application server handles lightweight requests
when it is busy processing blocking requests.

#### 5.3.6.2 `locust` Setup

The `locustfile` for the task scenario is located in `measurements/concurrency/api_health_endpoint/locustfile.py` 

#### 5.3.6.3 Results

Results file location: `measurements/concurrency/api_health_endpoint/results.csv`

We start with 1 worker and 1 user (no concurrency).
- The average response time for the `/api/health/` endpoint is around 6.25 ms.

Increase of the number of users to 5 reveals the impact of the blocking password hashing function.
- The average response time rose to 338.25 ms, demonstrating that the lightweight requests are significantly affected
by the blocked event loop.

As we kept increasing the number of users, the `health` endpoint performance degraded further.
- When we reached 20 users with 1 worker the average response time of the `/api/health` endpoint reached 2.34 seconds.

Increasing the number of workers improved performance on the `/api/health/` endpoint:
- With 4 workers and 5 users, the average response time was 13.45 ms.
- With 4 workers and 10 users, the average response time was 109.74 ms.
- With 4 workers and 15 users, the average response time rose to 158.27 ms.
- With 4 workers and 20 users, the average response time rose to 360.45 ms. 

At the same time as we kept increasing the number of users, the average response time of the `/api/users/register/` 
endpoint also increased, but not as severely as with one worker.

**Conclusions**

- Blocking CPU-bound operations stall the async event loop. A synchronous bcrypt hash prevents other coroutines 
from executing until the CPU work completes. This results in blocking of other concurrently called endpoints,
even the lightweight ones.
- The effect of the blocking behavior is especially apparent when the number of workers is equal to 1. The average 
response time of the `/api/health/` endpoint increases dramatically as the number of users increases. This happens
because the event loop is blocked by the CPU-intensive password hashing operations, causing lightweight requests 
to queue up and wait.
- As we increase the number of workers, the performance of the `/api/health/` endpoint improves.
- Parallel workers isolate blocking operations in separate processes, so lightweight requests can still be served 
promptly. The latency still increases with concurrency but remains an order of magnitude lower than the 
single-worker case.

### 5.6.7 Results Summary

1) How the event loop behaves when blocked?

When the event loop is blocked by a synchronous, CPU-bound operation (like password hashing, or file compression),
it can't switch to other tasks. As a result, all pending coroutines are paused until the blocking operation
completes. This leads to increased latency for all requests, even lightweight ones.


2) How responsiveness is affected under load?

Under load, especially when the number of concurrent requests exceeds the number of workers, responsiveness degrades 
significantly. Requests queue up behind the blocking operation, leading to higher latency and, in extreme cases, 
database lock errors.


3) How does the health-check endpoint behave when multiple registration requests are running concurrently? How does
its response time change with concurrency?

The health-check endpoint's response time increases dramatically as the number of concurrent registration requests
grows. This is happening because the event-loop is blocked by the CPU-intensive password hashing operations, causing
all the incoming requests (including lightweight ones) to queue up and wait.


4) How does the average response time of registration end-point change with concurrency?

The average response time of the registration endpoint increases significantly with higher concurrency. Since the 
registration process is resource-intensive (it involves passwords hashing and database writes), concurrent requests 
compete for CPU and I/O resources, overloading the system and causing response times to rise rapidly.


### 5.6.8 Measuring CPU and Memory Usage During the Experiments

This project does not include CPU and memory usage measurements during the experiments. The main reason for that
is the fact that we are running everything locally on a development machine, hence the CPU and memory usage
measurements are not very representative. However, during the next stage of the project we will work with the 
dockerized apps, in this case we will have a full control over the environment where the apps are running, and at
this stage we will perform CPU and memory usage measurements.