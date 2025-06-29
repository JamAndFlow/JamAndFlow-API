# Follow this steps to set up your local environment for development.

# Requirements:
# - Python 3.13


1. Clone the repository:


2. Navigate to the project directory:
   ```bash
    cd JamAndFlow
    ```

3. Setup virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - A. for windows: `./venv/Scripts/activate`
   - B. for macOS/Linux: `source venv/bin/activate`

5. Run FastAPI server through uvicorn:
   ```bash
   uvicorn app.main:app --host localhost --port 80
   or
   uvicorn app.main:app --reload
   ```

## Settings up environment variables
6. Create a `.env` file in the root directory of the project and add the following environment variables:
   ```env
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_DB=JamAndFlow
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   ```

# TODO: Add docker setup instructions below

1. Install Docker if you haven't already.
2. Build the Docker images:
```bash
   docker compose build --no-cache
```
3. Start the Docker containers:
   ```bash
   docker compose up
   ```
4. access the application `http://localhost:8000`
5. stop the containers:
   ```bash
   docker compose down
   ```

# How to crete a new migration
1. go to root directory
2. run the following command:
   ```bash
   alembic -c app/alembic.ini revision --autogenerate -m "testing"
   ```
# TODO: Add testing instructions below
