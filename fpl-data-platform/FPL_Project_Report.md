# Project Implementation Report

---

## Project Overview

This project is a web-based data platform built around the Fantasy Premier League (FPL) API. It demonstrates key concepts from the course including data collection, API integration, data persistence, unit/integration testing, and event collaboration messaging.

**Technologies Used**: Python, Flask, SQLite, RabbitMQ, unittest, pika

Website Address: https://fpl-data-platform-9ca2312a1972.herokuapp.com/

The application allows users to:

- View top-performing players (sorted by total points)
- View upcoming fixtures within the next 7 days
- See detailed team and player information
- Trigger asynchronous message queue events using RabbitMQ

---

## System Requirements

- Fetch player, fixture, and team data from the official FPL API
- Display it via a Flask web interface
- Persist data in a SQLite database
- Run unit and integration tests to ensure reliability
- Demonstrate event collaboration messaging using RabbitMQ + Pika
- Support RESTful API endpoints for `/api/teams`, `/api/players`, `/api/fixtures`, `/api/top-players`

## Architecture Diagram & Description

```
           ┌────────────┐
           │ FPL API    │
           └────┬───────┘
                │ (REST GET)
                ▼
        ┌───────────────┐
        │ Flask Backend │
        └─────┬─▲─┬─────┘
              │ │ │
     ┌────────┘ │ └────────┐
     ▼          ▼          ▼
RabbitMQ    SQLite DB   HTML Pages
 (via Pika)  (Persist)   (Jinja2 UI)
```

- **FPL API**: External REST API serving live football data
- **Flask Backend**: Core application logic for routing and rendering
- **RabbitMQ**: Asynchronous message queue for credit card transaction events
- **SQLite**: Simple data persistence for API results
- **HTML UI**: Jinja2 templated front-end rendering

## Implementation of Grading Criteria

### 1. Data Collection from External Source

- Implemented in: `src/collect_fpl_data.py`
- Uses the FPL public API: `https://fantasy.premierleague.com/api/bootstrap-static/`
- Extracts information about players, teams, and fixtures.

### 2. Data Persistence (Database)

- Data is stored using SQLite.
- Supports structured storage of player statistics, teams, and match fixtures.

### 3. Web Application with Routing

- Implemented in: `src/app.py`
- Built with Flask and provides the following API endpoints:
  - `/players`: Returns all player data.
  - `/teams`: Returns team information.
  - `/fixtures`: Returns fixture details.
- Designed for easy integration with frontend or external services.

### 4. Unit Testing

- Used `unittest` to implement:
  - Unit tests for endpoint responses
  - Integration tests for app lifecycle
- Used mock/doubles to avoid hitting external FPL API during testing
- Testable requirements:
  - API returns `200 OK`
  - Correct number of players returned
  - Valid HTML rendering of fixture data

- Implemented in: `tests/test_routes.py`
- Covers all primary routes and status code checks.
- Command to run:  
  ```bash
  python -m unittest discover -s tests
  ```

### 5. Mock Testing (Test Doubles)

- Implemented in: `tests/mock_test.py`
- Mocks external API (`requests.get`) using `unittest.mock`.
- Verifies that the logic works correctly without actual API calls.

### 6. Event Collaboration Messaging

- Producer: `send_fpl_event.py`  

- Consumer: `fpl_event_consumer.py`  

- Implements RabbitMQ with `pika` as a messaging broker.

- Demonstrates producer sending FPL events and consumer listening to transactions via queues.

- Illustrates asynchronous decoupled communication between modules.

  Demonstrated using `pika` and `RabbitMQ`. A producer sends credit card-like events to a queue, and a consumer subscribes to this queue and prints them.
  
  - **Producer**:
  
  ```python
  channel.basic_publish(
      exchange="",
      routing_key="transactions",
      body=json.dumps({"card_num": 12340000, "total": 4.10})
  )
  ```
  
  - **Consumer**:
  
  ```python
  channel.basic_consume(
      queue="transactions",
      on_message_callback=callback,
      auto_ack=True
  )
  ```
  

### 7. Continuous Integration & Monitoring

- The project structure supports:
  - Testable and modular code.
  - Easy integration into GitHub Actions or other CI platforms.
  - Potential for instrumentation and monitoring through event queue tracking.

---

##  Directory Overview

```
fpl-data-platform/
├── src/
│   ├── app.py
│   ├── collect_fpl_data.py
├── tests/
│   ├── test_routes.py
│   ├── mock_test.py
├── instance/
├── README.md
├── requirements.txt
├── send_fpl_event.py
├── fpl_event_consumer.py
```

---

## Summary

This project demonstrates a full-stack data platform that includes:

- API data collection and parsing.
- Local database storage.
- RESTful web services.
- Unit testing and mocking for reliability.
- Event-driven architecture using RabbitMQ.

It serves as a practical implementation of modern software architecture best practices and satisfies all required grading criteria.

---
