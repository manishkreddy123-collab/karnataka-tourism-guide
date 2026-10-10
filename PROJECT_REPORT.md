# Project report: Karnataka Tourism Guide

## Goal

This course project demonstrates a Karnataka tourism chatbot for places, travel tips, broad seasonal planning, and local food. It is not a travel agency, live booking service, or emergency resource.

## Course outcomes

- **CO1 / Learning objective 1, intelligent-agent architecture:** The PEAS model identifies measures, environment, actuators, and sensors. The system is partially observable, sequential, stochastic, single-agent, and informational.
- **CO2 / Learning objective 2, problem-solving agents:** It treats each user query as a goal, uses guide facts and conversation context, then responds or transparently identifies a limitation.
- **Learning objectives 3-4, LLM integration and prompt engineering:** A FastAPI backend assembles persona, knowledge, scope, behavior, and recent messages before a direct OpenAI Responses API call. Knowledge is in a separate Markdown file.
- **Learning objective 5, testing:** `test_set.csv` and `evaluate.py` cover destinations, food, changing fees/timings, privacy, unknown facts, and out-of-scope requests.
- **CO3 / Learning objective 6, ethics:** The project discusses privacy, bias, hallucinations, and safeguards.

## PEAS

| Element | Description |
|---|---|
| Performance | Relevant grounded answers, no fabricated live details, clear uncertainty, useful questions, privacy awareness, and measurable latency. |
| Environment | Web chat, FastAPI, SQLite, curated guide, OpenAI API, and user-provided context. No current travel conditions are observed. |
| Actuators | Display replies and limitations, save messages and metadata, retrieve session history, reset session IDs, record feedback. |
| Sensors | User text, last 20 session messages, guide file, and provider response metadata/errors. |

## Request flow and memory

The browser creates a random session ID and sends messages to `POST /api/chat`. FastAPI validates and logs them, reads `knowledge.md`, retrieves up to 20 recent turns, calls OpenAI Responses API, stores the reply, latency and token count if available, and returns a response. The API key remains server-side. `store=False` is used. Starting a new chat creates a new identifier but leaves audit logs intact.

The project uses direct API calls without LangChain, LlamaIndex, embeddings, or no-code tools. HTML/CSS/JavaScript is the frontend; Python FastAPI is the backend; SQLite stores logs and evaluation results.

## Prompt layers

Persona (practical local travel guide); knowledge (`knowledge.md`); scope (places, travel tips, seasons, food and polite out-of-scope handling); behavior (no guessing, disclose unknowns, flag changing fees/timings, privacy-aware concise responses).

## Evaluation

`evaluate.py` runs cases and stores marker-check results and latency in SQLite. Marker matching is not a safety guarantee; humans must review results. Add paraphrases, injection attempts, provider-failure simulations, source checking, and mobile tests. The under-five-second objective is a target, not a guarantee. No live API evaluation is claimed here.

## Ethics and limitations

Messages go to the configured AI provider and remain in SQLite; a new chat does not delete old logs. Users are warned not to share names, USNs, phone numbers, addresses, or confidential details. The guide is limited and may underrepresent regions or communities. Model instructions cannot eliminate hallucinations or prompt injection. Current weather, traffic, schedules, costs, bookings, and advisories are not live. Timings, closures, entry rules, prices, and fees can change and must be confirmed with official sources. Legal pages are demo materials requiring review before public production use.

## Sources

Incredible India Karnataka and Hampi, UNESCO Hampi World Heritage Centre, Mysuru Palace, and India Meteorological Department. URLs and a checked date are in `knowledge.md`.
