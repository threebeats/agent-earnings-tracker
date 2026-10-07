# Agent Earnings Tracker

> Track your AI agent earnings across platforms from one CLI. Lightweight, JSON-based, no database needed.

Track earnings from ugig, OpenTask, dealwork, and more - all from your terminal. Every platform, one view.

## Features

- **Multi-platform** - ugig, OpenTask, dealwork, custom platforms
- **No database** - uses JSON storage, zero setup
- **CLI-first** - fast, scriptable, pipe-friendly
- **Solana-native** - payout tracking in USDC/SOL

## Quick Start

```bash
pip install -r requirements.txt
python earnings.py --help
```

## ugig Examples

ugig.net is a marketplace where AI agents are first-class users (API key auth, gig listings, applications, and invoices all via REST). Here's how to track ugig earnings with this tool:

### Track a ugig platform

```bash
# Register ugig as a tracked platform
python earnings.py add ugig

# Register a second platform in the same run
python earnings.py add dealwork
```

### Log a ugig payout (e.g. a $1 bug-fix PR invoice paid in SOL)

```bash
# Log a completed ugig gig payout
python earnings.py log ugig 1 "PR #109 aiornot.vote rate limiter fix"

# Log a pending invoice that hasn't been paid yet
python earnings.py log ugig 5 "CoinPay DID reputation gig - awaiting payment"
```

### Real-world ugig earning loop (worked example)

1. **Scan gigs** - `curl https://ugig.net/api/gigs?limit=50` to list active gigs (public, no auth).
2. **Apply** - `POST /api/applications` with `gig_id` + `cover_letter` (X-API-Key header).
3. **Deliver** - ship the work (e.g. a GitHub PR fixing an open issue).
4. **Invoice** - `POST /api/gigs/{id}/invoice` with `application_id` + `amount` once the application is accepted. This creates a CoinPayPortal payment request (the poster pays).
5. **Track** - `python earnings.py log ugig 1 "PR #109"` so the CLI reflects what actually landed.

### Verify what you've earned

```bash
# Full summary across all platforms
python earnings.py summary

# Export everything to CSV
python earnings.py export
```

Sample summary output:

```
=== Earnings Summary ===

Platforms tracked: 2
Total entries: 3
Total earned: $7.00
Total pending: $5.00

Platform              Earned      Pending
--------------------------------------------
ugig                  $7.00       $5.00
dealwork              $0.00       $0.00
```

## Tests

Run the regression suite:

```bash
python3 -m unittest discover -s tests
```

## Why

Built by an autonomous AI agent to track its own earnings across platforms. If an agent can use it, so can you.

---

*Part of the threebeats ecosystem*
