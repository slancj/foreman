# foreman

A LangGraph project with dashboard support.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Configure your environment variables in `.env`:
```
API_KEY=your_api_key
UPSTREAM_API_URL=your_api_url
```

## Running the LangGraph Dashboard

Start the LangGraph dashboard:
```bash
langgraph dev
```

The dashboard will be available at `http://localhost:8123`

## Running the Graph Directly

```bash
python main.py
```
