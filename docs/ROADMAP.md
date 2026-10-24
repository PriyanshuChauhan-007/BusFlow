# BusFlow implementation roadmap

## How to use this roadmap

Each session is intentionally bounded. A session should produce a reviewable engineering increment, not a vague collection of generated files. Before moving on, the increment must have:

1. A clear acceptance criterion.
2. Tests appropriate to the change.
3. A short design note when a decision is non-obvious.
4. A reproducible command or walkthrough.
5. A commit with a focused message.

## Phase 0 — Product and engineering foundation

### Session 01: Repository foundation

Deliverables:

- Git repository and GitHub remote
- README, roadmap, contribution notes, and engineering rules
- Initial directory layout
- `.gitignore`, environment template, and Makefile/task commands

Evidence:

- Clean initial project check
- Documentation review
- Repository can be cloned and understood by a new contributor

### Session 02: Architecture and contracts

Deliverables:

- Architecture decision record
- Service boundaries
- Event envelope specification
- Error and idempotency rules
- Initial OpenAPI and WebSocket contract notes

Evidence:

- Example valid, duplicate, stale, invalid, and out-of-order events
- Contract tests for the event schema

## Phase 1 — First working vertical slice

### Session 03: Docker and service bootstrap

- Docker Compose with PostgreSQL and Redis
- FastAPI service skeleton
- Configuration management
- Liveness and readiness endpoints
- Structured logging baseline

### Session 04: Transit domain model

- Routes, stops, buses, route-stop ordering, assignments, and trips
- SQLAlchemy models and Alembic migration
- Seed data
- CRUD APIs for the core resources

### Session 05: Deterministic GPS simulator

- Route-following simulator
- Multiple concurrent buses
- Configurable interval and random seed
- Canonical `bus.location.v1` event
- Simulator tests that verify route progress and reproducibility

### Session 06: Ingestion service

- Event validation
- Redis Stream publishing
- Invalid-event quarantine
- Ingestion outcome metrics
- Contract and integration tests

### Session 07: Processing and live state

- Consumer group
- Idempotency by event ID
- Out-of-order protection
- Redis current-state projection
- PostgreSQL historical event persistence

Acceptance milestone:

> Two simulated buses produce events, valid events are processed once, history is stored, and current state is queryable.

## Phase 2 — Real-time user experience

### Session 08: Live tracking APIs

- Current bus and route endpoints
- Last-update age and state freshness
- Pagination and filtering
- API integration tests

### Session 09: WebSocket protocol

- Subscription messages
- Route and bus topics
- Position and state-update messages
- Reconnection behavior
- WebSocket integration tests

### Session 10: Operations dashboard

- React/TypeScript application
- Live map with routes, stops, and buses
- Bus freshness and status indicators
- Route and bus search
- Error and degraded-state UI

Acceptance milestone:

> An operator can open the dashboard, see multiple buses moving without refresh, search a route, and inspect a bus.

## Phase 3 — Transit intelligence

### Session 11: Schedule-based ETA baseline

- Stop schedules and scheduled offsets
- Baseline ETA calculation
- ETA API and WebSocket event
- Unit tests with boundary cases

### Session 12: Segment-based ETA

- Route segment representation
- Distance and speed calculation
- Recent-speed and historical-speed features
- Baseline comparison fixtures

### Session 13: Delay detection

- Delay policy configuration
- Delay state transitions
- Alert persistence and resolution
- Dashboard delay indicators

### Session 14: Route deviation detection

- Route geometry representation
- Distance-to-route calculation
- Consecutive-sample thresholding
- Deviation alert lifecycle

### Session 15: GPS quality and fault injection

- Missing, duplicate, delayed, invalid, and impossible events
- Simulator fault profiles
- Quarantine and diagnostics views
- Data-quality metrics

Acceptance milestone:

> Fault injection creates predictable alerts without corrupting current state or historical truth.

## Phase 4 — Historical analysis and experimentation

### Session 16: Trip history and replay

- Historical trip API
- Track replay endpoint
- Frontend replay timeline
- Query-performance indexes

### Session 17: ETA evaluation pipeline

- Actual arrival-time detection
- Prediction/actual matching
- MAE, RMSE, median error, and P90 error
- Reproducible evaluation report

### Session 18: ML ETA experiment

- Feature extraction
- Time-based train/test split
- First interpretable model
- Comparison against baselines
- Explicit failure analysis

The ML model is optional if it does not improve measured results. A well-explained baseline can be more credible than an unjustified model.

## Phase 5 — Reliability and scale evidence

### Session 19: Observability

- Prometheus metrics
- Correlation IDs
- Event age and processing latency
- Consumer lag
- Structured logs
- Grafana or documented metric queries

### Session 20: Failure handling

- Retry policy
- Dead-letter/quarantine behavior
- Graceful shutdown
- Redis/PostgreSQL outage behavior
- Recovery tests

### Session 21: Load testing

- Locust scenarios for REST, events, and WebSockets
- Controlled fleet sizes
- Measured throughput and latency
- Resource observations
- No invented performance claims

### Session 22: Scalability review

- Redis Streams versus Kafka discussion
- Database write and retention limits
- WebSocket fan-out limitations
- Partitioning and horizontal-scaling options
- Documented next-generation architecture

## Phase 6 — Final project quality

### Session 23: Security and operational polish

- Input limits
- CORS policy
- Secret handling
- Rate-limit discussion
- Admin/public API separation

### Session 24: Final documentation and demonstration

- Architecture diagrams
- API documentation
- Event-contract documentation
- Setup guide
- Evaluation report
- Demo script
- Resume-ready project summary

## Definition of done for the complete project

- A new user can run the system locally from documented commands.
- The core event path is covered by unit and integration tests.
- The dashboard receives live updates through WebSockets.
- Invalid and abnormal GPS behavior is visible and testable.
- ETA models are compared using measured data.
- Load-test results identify actual limits and are not fabricated.
- Architecture trade-offs and future improvements are documented.
