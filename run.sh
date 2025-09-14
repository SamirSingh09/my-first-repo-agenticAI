#!/bin/bash
export OPENAI_API_KEY="your_api_key_here"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
