# Jackpot Watcher

A production-style automation system that monitors the next EuroMillions jackpot estimate and sends operational alerts based on configurable rules.

This project was intentionally designed as more than a simple Python script. The goal was to simulate the mindset and trade-offs behind a lightweight real-world monitoring service:
- resilient data ingestion,
- external orchestration,
- degraded-mode handling,
- state persistence,
- operational observability,
- fault tolerance.

---

# Why This Project Exists

Most portfolio projects stop at:

```text
fetch data -> print result
```

This project explores what happens after that.

What happens when:
- the provider fails,
- the endpoint rate limits,
- scraping changes,
- retries are needed,
- alerts should not duplicate,
- the system silently dies,
- external orchestration is required,
- observability becomes necessary.

The project focuses heavily on operational reliability and engineering trade-offs instead of UI-heavy complexity.

---

# Core Features

## EuroMillions Jackpot Monitoring

The system scrapes the next EuroMillions jackpot estimate and evaluates it against a configurable threshold.

Example:

```text
Threshold: €100,000,000
Current estimate: €118,000,000
→ Alert triggered
```

---

## Resilient Scraping Strategy

Instead of relying on fragile CSS selectors such as:

```python
nth-child(...)
```

the scraper uses a semantic contextual extraction strategy:

1. Locate the EuroMillions section.
2. Extract only the surrounding contextual block.
3. Parse jackpot values from that block.

This reduces false positives and improves resilience against layout drift.

---

## Retry + Exponential Backoff

Network instability and temporary provider issues are handled with retry logic.

Strategy:

```text
Attempt 1
↓
2s delay
↓
Attempt 2
↓
4s delay
↓
Attempt 3
↓
8s delay
↓
Fallback provider
```

This avoids unnecessary degraded-mode activations caused by transient failures.

---

## Fallback Estimation Mode

If the primary provider fails:

```text
LottoStar unavailable
↓
Fallback estimation activated
↓
Email warning sent
```

The system intentionally enters degraded mode instead of failing silently.

Fallback alerts are tracked independently from jackpot alerts.

---

## Heartbeat Monitoring

The system sends weekly heartbeat emails to confirm operational health.

This solves a common automation problem:

```text
No alerts
```

can mean:
- jackpot below threshold,
- OR the system is dead.

Heartbeat monitoring removes that ambiguity.

---

## Persistent State Management

The system persists runtime state using GitHub Gists as lightweight remote storage.

Stored state includes:
- last threshold alert,
- last fallback alert,
- last heartbeat alert,
- last observed jackpot,
- last successful execution.

This prevents duplicate notifications across executions and enables stateless runners.

---

## Structured Logging

The application uses structured runtime logs for operational visibility.

Example:

```text
INFO | Jackpot amount: €92,000,000
INFO | Provider source: lottoster-scraper
INFO | Threshold exceeded: False
WARNING | Request failed. Retrying in 2s...
ERROR | All retries failed.
```

---

## External Orchestration

Scheduling is intentionally externalized using:

- cron-job.org
- GitHub Actions workflow_dispatch

This architecture was chosen to:
- reduce unnecessary GitHub Actions usage,
- separate orchestration from execution,
- simulate lightweight production scheduling patterns.

---

# Architecture

```text
cron-job.org
        ↓
GitHub Actions workflow_dispatch
        ↓
Docker container execution
        ↓
Primary provider scrape
        ↓
Retry / backoff
        ↓
Fallback estimation if needed
        ↓
Rule evaluation
        ↓
Email notification
        ↓
GitHub Gist state persistence
```

---

# Technical Stack

| Area | Technology |
|---|---|
| Language | Python 3.13 |
| Containerization | Docker |
| CI Runtime | GitHub Actions |
| Scheduling | cron-job.org |
| HTML Parsing | BeautifulSoup |
| HTTP | requests |
| State Persistence | GitHub Gists |
| Email Delivery | SMTP |

---

# Example Alert Emails

## Threshold Alert

```text
🚨 EuroMillions Alert - Jackpot Above Threshold
```

Includes:
- jackpot amount,
- provider source,
- formatted HTML email.

---

## Fallback Warning

```text
⚠️ EuroMillions Warning - Fallback Mode Activated
```

Signals degraded operational mode.

---

## Weekly Heartbeat

```text
💓 Jackpot Watcher Heartbeat
```

Confirms:
- service operational,
- latest jackpot estimate,
- provider source.

---

# Trade-Offs and Engineering Decisions

This project intentionally prioritizes operational simplicity over theoretical purity.

## Why GitHub Gists Instead of a Database?

### Chosen
- lightweight,
- free,
- persistent,
- easy API integration.

### Trade-off
- not ideal for high write concurrency,
- limited scalability,
- not suitable for multi-instance distributed systems.

### Reasoning
The project is single-runner and low-frequency. A database would introduce unnecessary operational overhead.

---

## Why External Scheduling Instead of Native GitHub Cron?

### Chosen
- cron-job.org + workflow_dispatch.

### Trade-off
- additional external dependency,
- more setup complexity.

### Reasoning
This reduces unnecessary GitHub Actions executions and gives explicit orchestration control.

---

## Why Semantic Scraping Instead of DOM Selectors?

### Chosen
- contextual text extraction.

### Trade-off
- slightly less strict parsing,
- requires careful validation logic.

### Reasoning
Highly specific selectors are fragile and often break after small frontend changes.

---

## Why Retry Before Fallback?

### Chosen
- exponential backoff.

### Trade-off
- increased execution time during failures.

### Reasoning
Most provider failures are transient. Immediate fallback would create unnecessary degraded-mode alerts.

---

## Why No Database / Queue / Cloud Infrastructure?

### Chosen
- lightweight operational footprint.

### Trade-off
- limited horizontal scalability.

### Reasoning
The goal was to demonstrate reliability engineering principles without introducing infrastructure complexity unrelated to the problem.

---

# What This Project Demonstrates

This project was intentionally built to demonstrate engineering maturity beyond CRUD applications.

Key areas:

- fault tolerance,
- operational thinking,
- runtime resilience,
- graceful degradation,
- observability,
- automation design,
- infrastructure pragmatism,
- trade-off awareness,
- lightweight system architecture.

---

# Local Development

## Clone Repository

```bash
git clone <repo-url>
cd jackpot-watcher
```

---

## Build Docker Image

```bash
docker build -t jackpot-watcher .
```

---

## Run Locally

```bash
docker run --env-file .env jackpot-watcher
```

---

# Required Environment Variables

```env
SMTP_HOST=
SMTP_PORT=
SMTP_USERNAME=
SMTP_PASSWORD=
EMAIL_FROM=
EMAIL_TO=

GIST_ID=
GIST_TOKEN=

JACKPOT_THRESHOLD=
```

---

# Operational Flows

## Monday / Thursday

```text
Monitor EuroMillions jackpot
→ evaluate threshold
→ send alert if needed
```

---

## Sunday

```text
Send heartbeat email
→ confirm operational health
```

---

# Future Improvements Considered

Several features were intentionally NOT implemented.

Examples:
- dashboards,
- ML jackpot prediction,
- databases,
- microservices,
- distributed queues.

Reason:

The project intentionally optimizes for:

```text
high signal engineering decisions
```

instead of unnecessary architectural complexity.

---

# Final Notes

This project is intentionally small in scope but deep in operational concerns.

The focus was never building a lottery application.

The focus was designing a lightweight automation system with:
- resilience,
- observability,
- degraded-mode handling,
- pragmatic infrastructure decisions,
- production-style operational thinking.
