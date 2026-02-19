## Health & Wellness Planner Agent System

## FastAPI

1.  Install FastAPI with:

    ```bash
    uv add "fastapi[standard]"
    ```

2.  Make a basic app with:

    ```bash
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"Hello": "World"}
    ```

3.  Run the app with:

    ```bash
    fastapi dev main.py
    ```
