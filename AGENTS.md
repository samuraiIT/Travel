# Travel project delta

Read `/opt/project_llm/AGENTS.md` first, then this file.

## Canon

- `README.md` is the human operational plan.
- `data/china-2026.json` is the machine-checkable fact set.
- Ticket screenshots in `China/` are primary evidence and must not be edited.
- Run `python3 scripts/validate_itinerary.py` after every itinerary change.

## Status and sources

Use only `Confirmed`, `Book`, and `Backup`. A fixed ticket or current
authoritative source may be `Confirmed`; chosen but unbooked inventory is
`Book`; conditional sightseeing is `Backup`.

Do not silently change a confirmed flight, add a required excursion on a
long-transfer day, invent a train number before the 12306 sales window, or
present a planning price as booked.

For route work use the skills in this order:
`travel-agent-skill` → `travel-concierge` → `travel-day-optimizer`, with
`china-travel-operations` as the project wrapper.
