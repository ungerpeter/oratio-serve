import uvicorn
from oratio_serve.main import app

def main() -> None:
    uvicorn.run("oratio_serve.main:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
