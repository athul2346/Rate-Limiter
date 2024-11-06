# Interactive API Application

This project consists of a backend API built with FastAPI and a frontend developed using React. The backend API handles authentication, rate-limiting, and resource access, while the frontend allows users to interact with the API. The application is containerized using Docker for easy deployment.

## Features

- **Rate Limiting**: The API implements rate-limiting using Redis to limit the number of requests a user can make in a given time period.
- **JWT Authentication**: Secure access with JSON Web Tokens (JWT) for user authentication.
- **API Versioning**: Supports multiple versions of the API to maintain backward compatibility.
  
## Prerequisites

Make sure you have the following tools installed:

- Docker and Docker Compose
- Python 3.7+ (for backend development)
- Node.js and npm (for frontend development)

## How to Run

### 1. Clone this repository:
```bash
git clone https://github.com/yourusername/interactive-api-application.git
cd interactive-api-application
```
### 2. For the backend:

The backend is a FastAPI application, and we use Docker to containerize the application for easy deployment.
Backend Setup with Docker:

Navigate to the backend directory:

      cd backend
Create a .env file to store environment variables (like SECRET_KEY, REDIS_HOST, etc.) and set them accordingly:

      SECRET_KEY=<your_secret_key>
      REDIS_HOST=<your_redis_host>

Run docker-compose up --build to build and start the backend container:

      docker-compose up --build

The backend will be available at http://localhost:8000 (by default). The API will be exposed and ready for interaction.

### 3. For the frontend:

The frontend is built using React and is also containerized with Docker.
Frontend Setup with Docker:
Navigate to the frontend directory:

      cd frontend
Run docker-compose up --build to build and start the frontend container:

      docker-compose up --build
The frontend will be available at http://localhost:3000 (by default). You can interact with the backend API through the frontend interface.

### 4. Usage
Login for Access Token: Send a POST request to /token with a valid username to receive a JWT access token.

Access Protected Resources: Use the JWT token to make GET requests to /api/resource/v1 or /api/resource/v2, depending on the API version. The response will be rate-limited based on your IP address.

### Example Postman Requests

POST /token
Request body:

      {
        "username": "Athul"
      }

Response:

      {
        "access_token": "<JWT_TOKEN>",
        "token_type": "bearer"
      }

GET /api/resource/v1

Response:

      {
        "message": "Resource accessed successfully"
      }

GET /api/resource/v2

Authorization: Bearer <JWT_TOKEN>
Response:

    {
      "message": "Resource accessed successfully"
    }

Technologies Used

 --FastAPI (Backend): Python web framework for building APIs with automatic documentation, high performance, and ease of use.
 --React (Frontend): A JavaScript library for building user interfaces.
 --Docker (Containerization): For packaging the application into containers that can be run anywhere.
 --Redis (For caching and rate-limiting): In-memory data structure store used to manage rate-limiting information.
 --JWT (Authentication): JSON Web Tokens for securely transmitting information between frontend and backend.

Rate Limiting

--Per minute: Max 5 requests in 60 seconds.

--Per hour: Max 15 requests in 3600 seconds.

API Versioning

--/api/resource/v1: The first version of the API with no authentication or JWT-based access.

--/api/resource/v2: The second version of the API with JWT authentication and rate-limiting enabled.

Development

--To contribute to the project, clone the repository, make changes in your local environment, and push to the repository with a pull request.
--Ensure that all environment variables are configured before running the application.



