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
   POSTGRES_USER=<POSTGRES_USER>
   POSTGRES_PASSWORD=<POSTGRES_PASSWORD>
   POSTGRES_DB=JamAndFlow
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   FROM_EMAIL=<EMAIL_ID_TO_SEND_EMAILS_FROM>
   SMTP_PASSWORD=<SMTP_PASSWORD>
   SMTP_USERNAME=<EMAIL_ID_TO_SEND_EMAILS_FROM>
   SECRET_KEY=<SECRET_KEY>
   ALGORITHM=<ALGORITHM>
   ACCESS_TOKEN_EXPIRE_MINUTES=<ACCESS_TOKEN_EXPIRE_MINUTES>
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

# How to create a new migration
1. Accessing the jam_and_flow_api Docker Container
   ```bash
   docker exec -it jam_and_flow_api bash
   ```
2. Run command:
   ```bash
   cd app
   alembic revision --autogenerate -m "migration_name"
   alembic upgrade head
   ```

# How to inspect postgres table
1. Accessing the postgres_db Docker Container
   ```bash
   docker exec -it postgres_db bash
   ```
2. Run command:
   ```bash
   psql -U postgres -d JamAndFlow
   ```
3. To list tables:
   ```sql
   \dt
   ```
4. To view a specific table:
   ```sql
   SELECT * FROM table_name;
   ```

# TODO: Add testing instructions below
