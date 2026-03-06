# Blocker Aging Metric

## Definition
Blocker aging = elapsed time from blocker first recorded to explicit resolution timestamp.

## Formula
`aging_hours = resolved_at - detected_at`

## Buckets
- Green: < 4h
- Yellow: 4h - 24h
- Red: > 24h

## Weekly reporting minimum
- Open blockers by bucket
- Longest aging blocker
- Breach count and owner
