# E-Commerce Microservices

A hands-on **microservices-based e-commerce application** built to understand how independent services communicate, manage their own data, and evolve toward a production-ready distributed architecture.

The project is being implemented incrementally. The **first implementation demonstrates synchronous service-to-service communication using HTTP/REST with JSON**, with additional communication mechanisms such as **gRPC, RabbitMQ, and Kafka** planned for later stages.

---

## 🚀 Project Objective

The main objective of this project is to understand and demonstrate:

* Microservices architecture
* Service-to-service communication
* REST API communication using HTTP/JSON
* Independent service ownership
* Database-per-service architecture
* Authentication and authorization
* API Gateway
* Synchronous vs asynchronous communication
* Message brokers
* Event-driven architecture
* Docker-based deployment
* Distributed system concepts

Rather than implementing everything at once, the project will evolve step-by-step to demonstrate different approaches to microservice communication.

---

# 🏗️ Current Architecture

The current implementation contains two independent services:

```text
                         Client
                           │
                           │ HTTP/JSON
                           ▼
                 ┌─────────────────────┐
                 │    User Service     │
                 │   Django + Ninja    │
                 └──────────┬──────────┘
                            │
                            ▼
                         User DB


                 ┌─────────────────────┐
                 │  Product Service    │
                 │       FastAPI       │
                 └──────────┬──────────┘
                            │
                            ▼
                       Product DB
```

The services communicate with each other using:

```text
HTTP
  +
REST
  +
JSON
```

For example:

```text
Product Service
      │
      │ GET /api/users/{user_id}
      │
      ▼
User Service
      │
      ▼
User Database
```

The Product Service does **not directly access the User Service database**.

---

# 🧩 Services

## 1. User Management Service

**Technology:** Django + Django Ninja

Responsible for user-related operations.

### Responsibilities

* User registration
* User management
* User retrieval
* Address management
* User authentication
* User-related APIs

### Example APIs

```http
POST /api/users/
GET  /api/users/{user_id}
PUT  /api/users/{user_id}
DELETE /api/users/{user_id}

POST /api/users/{user_id}/addresses/
GET  /api/users/{user_id}/addresses/
PUT  /api/addresses/{address_id}
DELETE /api/addresses/{address_id}
```

---

## 2. Product Management Service

**Technology:** FastAPI

Responsible for product-related operations.

### Responsibilities

* Product CRUD
* Category management
* Product images
* Inventory management
* Product search/filtering

### Example APIs

```http
POST /api/products/
GET  /api/products/
GET  /api/products/{product_id}
PUT  /api/products/{product_id}
DELETE /api/products/{product_id}

POST /api/categories/
GET  /api/categories/

GET /api/inventory/{product_id}
```

---

# 🔗 Service-to-Service Communication

The first communication mechanism demonstrated in this project is:

> **Synchronous HTTP/REST communication using JSON.**

For example, suppose the Product Service needs to verify whether a user exists.

The Product Service sends:

```http
GET http://user-service/api/users/101
```

The User Service processes the request and returns:

```json
{
    "id": 101,
    "name": "John Doe",
    "email": "john@example.com"
}
```

The communication flow is:

```text
Product Service
       │
       │ HTTP Request
       │
       │ GET /api/users/101
       ▼
 User Service
       │
       │ Query
       ▼
   User Database
       │
       │ User Data
       ▼
 User Service
       │
       │ JSON Response
       ▼
Product Service
```

This demonstrates **synchronous request-response communication**.

The Product Service waits for the User Service to return a response.

---

# 🗄️ Database Architecture

The project follows the **database-per-service principle**.

The User Service owns its database:

```text
User Service
      │
      ▼
   User DB
      │
      ├── users
      └── addresses
```

The Product Service owns its database:

```text
Product Service
      │
      ▼
 Product DB
      │
      ├── products
      ├── categories
      ├── product_images
      └── inventory
```

### Important principle

Services should **not directly access another service's database**.

Incorrect:

```text
Product Service ───────► User DB ❌
```

Correct:

```text
Product Service
      │
      │ HTTP/REST
      ▼
 User Service
      │
      ▼
 User DB
```

---

# 📊 Initial Database Design

### User Service

```text
users
├── id
├── name
├── email
├── phone
├── password_hash
├── is_active
├── created_at
└── updated_at

addresses
├── id
├── user_id
├── address_line
├── city
├── state
├── postal_code
├── country
└── is_default
```

### Product Service

```text
categories
├── id
├── name
├── description
└── parent_category_id

products
├── id
├── category_id
├── name
├── description
├── sku
├── price
├── discount_price
├── brand
└── is_active

product_images
├── id
├── product_id
├── image_url
├── is_primary
└── display_order

inventory
├── id
├── product_id
├── quantity
├── reserved_quantity
└── updated_at
```

---

# 🔐 Authentication

Authentication will be implemented using **JWT-based authentication**.

The expected architecture is:

```text
Client
   │
   │ Login
   ▼
User Service
   │
   │ JWT
   ▼
Client
   │
   │ Authorization: Bearer <token>
   ▼
Product Service
```

The Product Service can validate the JWT and identify the authenticated user without directly accessing the User database.

---

# 🔄 Current Communication Flow

A simple example:

### Step 1 — User exists

```text
User Service

User ID: 101
Name: John
Email: john@example.com
```

### Step 2 — Client requests product creation

```http
POST /api/products/
Authorization: Bearer <JWT>
```

```json
{
    "name": "Laptop",
    "price": 75000
}
```

### Step 3 — Product Service identifies the user

```text
JWT
 ↓
user_id = 101
```

### Step 4 — Product Service can communicate with User Service

```http
GET /api/users/101
```

### Step 5 — User Service responds

```json
{
    "id": 101,
    "name": "John",
    "email": "john@example.com"
}
```

### Step 6 — Product Service performs its business operation

```text
Product Service
      │
      ▼
Product DB
```

---

# 🧱 Project Structure

```text
ecommerce-microservices/
│
├── user-service/
│   │
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── api.py
│   │
│   └── users/
│       ├── models.py
│       ├── schemas.py
│       ├── api.py
│       ├── services.py
│       └── migrations/
│
│
├── product-service/
│   │
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   │
│   ├── app/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── database.py
│   │   └── main.py
│   │
│
├── docker-compose.yml
│
└── README.md
```

---

# 🐳 Docker Architecture

The services will eventually run independently as containers:

```text
                     Docker Compose
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    User Service     Product Service     User DB
     Django Ninja       FastAPI          PostgreSQL
                           │
                           ▼
                      Product DB
                      PostgreSQL
```

Inside the Docker network, services communicate using service names rather than `localhost`.

For example:

```text
http://user-service:8000
```

instead of:

```text
http://localhost:8000
```

---

# 🛣️ Development Roadmap

The project will be implemented progressively to demonstrate different microservice communication patterns.

## Phase 1 — HTTP/REST + JSON ✅

Current phase.

```text
Service A
    │
    │ HTTP/REST
    │ JSON
    ▼
Service B
```

Technologies:

* Django
* Django Ninja
* FastAPI
* PostgreSQL
* HTTP/JSON

---

## Phase 2 — Authentication & Authorization

Implement:

* JWT
* Access tokens
* Refresh tokens
* Role-based authorization
* Service authentication

Architecture:

```text
Client
   │
   ▼
User Service
   │
   ▼
JWT
   │
   ├──────────────► Product Service
   └──────────────► Other Services
```

---

## Phase 3 — Docker

Containerize each service:

```text
User Service       → Docker Container
Product Service    → Docker Container
User DB            → PostgreSQL Container
Product DB         → PostgreSQL Container
```

Use Docker Compose for local development.

---

## Phase 4 — API Gateway

Introduce an API Gateway:

```text
                       Client
                         │
                         ▼
                    API Gateway
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       User Service           Product Service
```

Responsibilities:

* Request routing
* Authentication
* Rate limiting
* CORS
* API versioning
* Request logging

---

## Phase 5 — gRPC

Introduce gRPC for internal synchronous communication.

```text
Service A
    │
    │ gRPC
    ▼
Service B
```

Compare:

```text
REST/JSON
vs
gRPC/Protobuf
```

in terms of:

* Performance
* Payload size
* Type safety
* Development complexity
* Use cases

---

## Phase 6 — RabbitMQ

Introduce asynchronous communication.

Example:

```text
Order Service
      │
      │ OrderCreated
      ▼
   RabbitMQ
      │
      ├────────► Notification Service
      │
      └────────► Inventory Service
```

Topics to demonstrate:

* Producers
* Consumers
* Exchanges
* Queues
* Routing keys
* Acknowledgements
* Retries
* Dead-letter queues

---

## Phase 7 — Kafka

Introduce event streaming.

```text
                    Kafka
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
 Inventory       Notification     Analytics
 Service           Service         Service
```

Demonstrate:

* Topics
* Partitions
* Consumer groups
* Offsets
* Event-driven architecture

---

## Phase 8 — Order & Payment Services

Expand the e-commerce platform:

```text
User Service
Product Service
Cart Service
Order Service
Payment Service
Inventory Service
Notification Service
```

---

# 🏪 Final Target Architecture

The eventual architecture will look like:

```text
                              CLIENT
                                │
                                ▼
                         ┌──────────────┐
                         │ API GATEWAY  │
                         └──────┬───────┘
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
       User Service       Product Service     Order Service
       Django Ninja          FastAPI             FastAPI
             │                  │                  │
             ▼                  ▼                  ▼
          User DB           Product DB          Order DB
                                                   │
                                                   │
                                                   ▼
                                              Event Broker
                                           RabbitMQ / Kafka
                                             /     |      \
                                            ▼      ▼       ▼
                                        Payment  Email   Analytics
                                        Service  Service   Service
```

---

# 🔑 Microservices Principles Demonstrated

This project focuses on the following principles:

### 1. Independent Services

Each service has its own responsibility.

### 2. Loose Coupling

Services communicate through APIs/events rather than sharing implementation details.

### 3. Database Ownership

Each service owns its data.

### 4. API Contracts

Communication happens through clearly defined request/response contracts.

### 5. Synchronous Communication

```text
REST / HTTP
gRPC
```

### 6. Asynchronous Communication

```text
RabbitMQ
Kafka
```

### 7. Fault Tolerance

Future implementations will demonstrate:

```text
Timeout
Retry
Circuit Breaker
Dead Letter Queue
Idempotency
```

---

# 🧪 Learning Goals

By completing this project, the goal is to understand not only **how to build microservices**, but also **why particular communication mechanisms are used**.

For example:

```text
Need immediate response?
        │
        ├── YES → REST / gRPC
        │
        └── NO
             │
             ▼
       Event / Message
             │
             ├── RabbitMQ
             └── Kafka
```

---

# 📚 Technology Stack

### Backend

* Python
* Django
* Django Ninja
* FastAPI

### Database

* PostgreSQL

### Communication

* HTTP
* REST
* JSON
* gRPC
* RabbitMQ
* Kafka

### Infrastructure

* Docker
* Docker Compose

### Future

* Redis
* API Gateway
* Kubernetes
* Monitoring
* Distributed tracing

---

# 🎯 Project Philosophy

This project is intentionally being built **incrementally**.

The first goal is to understand the simplest form of microservice communication:

```text
HTTP + REST + JSON
```

Once that is working correctly, more advanced approaches will be introduced and compared:

```text
HTTP/REST
     ↓
gRPC
     ↓
RabbitMQ
     ↓
Kafka
```

The objective is not just to implement different technologies, but to understand **when, why, and where each communication mechanism should be used in a real-world distributed system**.

---

# 👨‍💻 Author

**Rishu Kumar**

Backend / Integration Engineer

Technologies of interest:

```text
Python
Django
FastAPI
REST APIs
Microservices
Data Engineering
AWS
Docker
LLMs / AI
```

---

## ⭐ Status

🚧 **Work in Progress**

### Current

* [x] Microservice architecture defined
* [x] User Management Service — Django + Django Ninja
* [x] Product Management Service — FastAPI
* [x] Separate service responsibilities
* [x] HTTP/REST + JSON communication design

### Upcoming

* [ ] JWT authentication
* [ ] Docker Compose
* [ ] API Gateway
* [ ] gRPC communication
* [ ] RabbitMQ
* [ ] Kafka
* [ ] Order Service
* [ ] Payment Service
* [ ] Notification Service
* [ ] Distributed tracing
* [ ] Monitoring
* [ ] Kubernetes deployment
