# Karnataka Tourism Guide

A course-project chatbot for exploring destinations, broad seasonal considerations, travel tips, and regional food in Karnataka. Built with a Python FastAPI backend, the OpenAI Responses API, SQLite, and a plain HTML/CSS/JavaScript frontend. The API key stays on the server.

The chatbot uses a sourced guide, carries recent session context, records chat logs and response times, and warns that attraction timings, closures, entry rules, and fees may change. It is not a live booking, weather, or emergency service.

## Setup

1. Install Python 3.10 or later and run `pip install -r requirements.txt`.
2. Copy `.env.example` to `.env` and provide an OpenAI API key. Never commit `.env`.
3. Start with `uvicorn main:app --reload` and open `http://127.0.0.1:8000`.

The curated facts and source links are in `knowledge.md`; edit that file to update the guide.

## Public hosting

`render.yaml` configures public Render access without an app login. Connect this private repository to Render as a Blueprint, enter `OPENAI_API_KEY` in Render's secret settings, and deploy to receive a public `onrender.com` URL. This repository alone does not make the app live. Add spending controls and abuse protection before broadly promoting an unauthenticated public chatbot.