dev:
  uv run fastapi dev oratio_serve/main.py --host 0.0.0.0 --port 8000

compose:
  docker compose up --build