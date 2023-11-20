# RPN Calculator API

## Project Overview

This project is an API for a Reverse Polish Notation (RPN) Calculator, built using FastAPI and MongoDB. It provides endpoints for performing calculations in RPN format, converting infix expressions to RPN, and managing calculation records. The application is containerized using Docker, simplifying deployment and environment setup.

### Features

- **RPN Calculation**: Perform calculations using the Reverse Polish Notation.
- **Infix to RPN Conversion**: Convert standard infix arithmetic expressions to RPN.
- **MongoDB Integration**: Store and retrieve calculation records.
- **Dockerized Application**: Easy to set up and deploy with Docker and Docker Compose.

## Getting Started

These instructions will guide you through getting a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Shynexiii/rpn-calculator-api.git
   cd rpn-calculator-api
   ```

2. **Start the Application with Docker Compose**

   ```bash
   docker-compose up --build
   ```

3. **Access the Application**
   The FastAPI application will be accessible at [http://localhost:8000](http://localhost:8000).

4. **API Endpoints**
   - Calculate RPN: `POST /calculate_rpn`
   - Convert to RPN: `POST /convert_to_rpn`
   - Check if RPN: `POST /check_rpn`
   - Retrieve Operations: `GET /operations`
   - Operations as CSV: `GET /operations_csv`
   - Delete All Operations: `DELETE /delete_all_operations`

### Running Tests

Describe how to run the automated tests for this system:

```bash
python3 -m unittest tests/test_calculator.py
```

## Built With

- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [MongoDB](https://www.mongodb.com/) - Database
- [Docker](https://www.docker.com/) - Containerization
