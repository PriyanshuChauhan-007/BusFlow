# BusFlow event contracts

## Contract conventions

- Event names are versioned: `bus.location.v1`.
- `event_id` is globally unique for the event producer's logical event.
- `occurred_at` is when the bus device or simulator observed the position.
- `produced_at` is when the producer emitted the event.
- `received_at` and `processed_at` are added by BusFlow services.
- Coordinates use decimal degrees and WGS84 semantics.
- Speeds are meters per second.
- Headings are degrees clockwise from north.

## `bus.location.v1`

```json
{
  "event_id": "gps-01JABC123",
  "event_type": "bus.location.v1",
  "schema_version": 1,
  "occurred_at": "2026-10-25T10:30:15.250Z",
  "produced_at": "2026-10-25T10:30:15.300Z",
  "source": "simulator",
  "bus_id": "bus-42",
  "trip_id": "trip-1001",
  "route_id": "route-7",
  "sequence_number": 1284,
  "position": {
    "latitude": 12.971600,
    "longitude": 77.594600,
    "accuracy_meters": 8.5
  },
  "motion": {
    "speed_mps": 7.2,
    "heading_degrees": 84.0
  }
}
```

## Validation rules

An event is invalid when:

- `event_id`, `bus_id`, `trip_id`, or `route_id` is missing.
- `latitude` is outside `[-90, 90]`.
- `longitude` is outside `[-180, 180]`.
- `accuracy_meters` is negative or not finite.
- `speed_mps` is negative, not finite, or above the configured maximum.
- `heading_degrees` is outside `[0, 360)`.
- `occurred_at` is unparseable or unreasonably far in the future.
- Required timestamps violate `occurred_at <= produced_at` beyond an allowed clock-skew policy.

Invalid events are not silently dropped. They receive a rejection reason and are published to a quarantine path or persisted as rejected-ingestion records.

## Processing semantics

### Duplicate event

An event with an already-seen `event_id` is acknowledged without applying another state mutation. The system increments a duplicate counter and records the duplicate outcome.

### Out-of-order event

An event older than the latest accepted event for the same bus/trip can be retained for historical analysis, but cannot replace the live-state projection.

### Stale event

An event whose age exceeds the configured live-data threshold may be stored, but is excluded from current ETA updates and can trigger a stale-data signal.

### Impossible movement

If the distance and elapsed event time imply a speed above the configured physical limit, the event is marked suspicious. Policy may quarantine it or accept it as history without applying it to live state.

## Processor outcome vocabulary

```text
ACCEPTED
DUPLICATE
OUT_OF_ORDER
STALE
INVALID
SUSPICIOUS_MOVEMENT
UNKNOWN_BUS
UNKNOWN_TRIP
```

## WebSocket message envelope

```json
{
  "type": "bus.position.updated",
  "schema_version": 1,
  "sequence": 9031,
  "occurred_at": "2026-10-25T10:30:16.000Z",
  "data": {
    "bus_id": "bus-42",
    "latitude": 12.971700,
    "longitude": 77.594800,
    "speed_mps": 6.9,
    "next_stop_id": "stop-18",
    "eta_seconds": 142,
    "delay_seconds": 38
  }
}
```

Clients use REST to obtain an initial snapshot, then subscribe to topics such as `route:route-7`, `bus:bus-42`, and `alerts`. WebSocket messages are incremental notifications, not the durable source of truth.
