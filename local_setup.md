# Follow this steps to set up your local environment for development.

# Requirements: 
# - Python 3.12.1


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
   ```


# TODO: Add docker setup instructions below 

# TODO: Add testing instructions below
