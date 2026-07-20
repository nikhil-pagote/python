from pathlib import Path

from granian import Granian
from granian.constants import Interfaces

# import uvicorn

if __name__ == "__main__":
    Granian(
        "my_fapi:app",
        address="0.0.0.0",
        port=8000,
        interface=Interfaces.ASGI,
        working_dir=Path(__file__).parent / "src",
        reload=True,
    ).serve()
    # uvicorn.run("my_fapi:app", app_dir="src", host="0.0.0.0", port=8000, reload=True)
