#!/bin/bash
cd backend
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
echo "Backend running on http://localhost:8000"
cd ../frontend
python3 -m http.server 3000 &
FRONTEND_PID=$!
echo "Frontend running on http://localhost:3000"
echo "Press Ctrl+C to stop both servers."
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
