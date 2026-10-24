# BusFlow engineering rules

These rules exist to keep BusFlow credible as an engineering project.

## Evidence over claims

- Never claim throughput, latency, accuracy, or scalability without a recorded measurement.
- Every benchmark records hardware, configuration, dataset size, and command.
- A failed experiment is documented rather than hidden.

## Small vertical slices

- Each change should connect to a user-visible or operationally meaningful behavior.
- Avoid creating placeholder services that have no real responsibility.
- Prefer a working end-to-end path over disconnected scaffolding.

## Correct event processing

- Event IDs are unique and idempotency is explicit.
- Event time and processing time are separate.
- Invalid events are observable and never silently discarded.
- Out-of-order events cannot overwrite newer live state.

## Honest machine learning

- Start with a transparent baseline.
- Use time-aware evaluation for time-series prediction.
- Compare against baselines with reproducible metrics.
- Keep the ML component only if it provides measured value or useful analysis.

## Reviewability

- Keep commits focused and explain non-obvious decisions.
- Add tests with new behavior.
- Keep API and event contracts versioned.
- Update documentation when behavior or architecture changes.
