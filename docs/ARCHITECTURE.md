# BusFlow architecture

## Design objective

BusFlow is an event-driven transit operations platform. The system separates durable history, live state, event transport, prediction, and presentation so that each concern can be measured and evolved independently.

The first deployment is intentionally a modular monorepo rather than a collection of prematurely distributed microservices. Each module has a clear responsibility and process boundary where a real operational requirement justifies it.

## Logical components

### GPS simulator

Produces versioned location events for one or more buses. It supports deterministic seeds and fault injection so the system can be tested against realistic bad data.

### Ingestion service

Accepts events, validates the contract, attaches receive metadata, rejects or quarantines invalid data, and publishes accepted events to a Redis Stream.

### Processing service

Consumes the stream using a consumer group, enforces idempotency and ordering rules, persists historical events, and updates the live bus-state projection.

### ETA and anomaly modules

Calculate arrival predictions and evaluate operational rules such as delay, route deviation, stale GPS, and impossible movement. These begin as modules used by the processor and can become independently deployed workers later.

### API service

Exposes management, live-state, historical, ETA, alert, health, and metrics endpoints. It also owns the WebSocket connection layer.

### React dashboard

Uses REST for initial snapshots and WebSockets for incremental updates. It presents operational state, data-quality problems, alerts, and ETA evaluation rather than only rendering a map.

## Data ownership

| Data | System of record | Read optimization |
|---|---|---|
| Routes, stops, buses, schedules | PostgreSQL | API query indexes |
| Raw accepted location events | PostgreSQL | Time and trip indexes |
| Current bus state | Redis projection | Redis hashes / API cache |
| Event transport | Redis Streams | Consumer groups |
| Active alerts | PostgreSQL | Redis cache later if measured necessary |
| ETA predictions | PostgreSQL | Redis for current ETAs later |

## Initial event path

```text
Simulator
  -> ingestion validation
  -> Redis Stream: bus.location.v1
  -> processor consumer group
  -> idempotency/order checks
  -> PostgreSQL history + Redis current state
  -> ETA/anomaly evaluation
  -> WebSocket publication
  -> dashboard
```

## Important trade-offs

### Redis Streams first, Kafka later

Redis Streams gives the project consumer groups, message IDs, pending entries, and replay behavior with a small local footprint. Kafka is a future option when partitioning, retention, replication, and independent consumer scaling become first-class requirements.

### PostgreSQL first, specialized time-series storage later

PostgreSQL keeps the first system understandable and supports relational transit data plus historical events. We will measure write volume and query behavior before considering partitioning, TimescaleDB, or another storage system.

### Modular monorepo first

The code will have explicit modules and contracts without creating network hops merely for appearance. Process boundaries will be added when they improve isolation, scaling, or failure behavior.

## Reliability principles

- Event IDs are idempotency keys.
- Event time, receive time, and process time are separate fields.
- Newer accepted state cannot be overwritten by an older event.
- Invalid events remain observable through quarantine records and metrics.
- WebSocket delivery is best-effort; REST remains the source for a fresh snapshot.
- Current state is a projection and can be rebuilt from accepted history.

## Scaling boundary to measure later

The first version is not claimed to be production-scale. Load testing will identify limits around:

- Redis Stream ingestion and consumer lag
- PostgreSQL historical write rate
- WebSocket fan-out
- API query latency under concurrent users
- Memory required for current-state projections

Those measurements will determine whether to introduce Kafka, database partitioning, multiple processor workers, or a shared WebSocket broker.
