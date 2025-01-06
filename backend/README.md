# Backend Setup and API Testing Guide

This guide explains how to set up the backend environment, run the server, and test the endpoints for the project.

## Prerequisites

- **Python**: Ensure you have Python 3.10 or later installed.
- **pip**: Comes pre-installed with Python. If not, install it.
- **Postman** (or cURL): For API testing.
- **Git**: For cloning the repository.

## Steps to Set Up and Run the Backend Server

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/fintech-hackathon.git
cd fintech-hackathon/backend
```

### 2. Create a Virtual Environment

Create and activate a Python virtual environment to isolate dependencies.

#### macOS/Linux:

```bash
python3 -m venv fintech-env
source fintech-env/bin/activate
```

#### Windows:

```bash
python -m venv fintech-env
fintech-env\Scripts\activate
```

### 3. Install Dependencies

Install all required Python libraries:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the `backend/` directory with the following content:

```
OPENAI_API_KEY=<your-openai-api-key>
```

Replace `<your-openai-api-key>` with your actual OpenAI API key.

### 5. Run the Backend Server

Start the FastAPI server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will be available at `http://127.0.0.1:8000`.

---

## Testing the API Endpoints

You can test the API endpoints using **Postman** or **cURL**.

### 1. Using Postman

1. Open Postman and create a new **POST** request.
2. Set the URL to:
   ```
   http://127.0.0.1:8000/scrape
   ```
3. In the **Body** tab, select `raw` and set the content type to `JSON`.
4. Enter the following JSON payload:

   ```json
   {
       "prompt": "List all projects with their description.",
       "url": "https://perinim.github.io/projects/"
   }
   ```

5. Click **Send**.

6. You should receive a response similar to this:

   ```json
   {
       "result": [
           {
               "name": "Project A",
               "description": "Description of Project A",
               "link": "https://example.com/project-a"
           },
           {
               "name": "Project B",
               "description": "Description of Project B",
               "link": "https://example.com/project-b"
           }
       ]
   }
   ```

### 2. Using cURL

Alternatively, you can use `cURL` to test the endpoint:

```bash
curl -X POST http://127.0.0.1:8000/scrape \
-H "Content-Type: application/json" \
-d '{"prompt": "List all projects with their description.", "url": "https://perinim.github.io/projects/"}'
```

Expected Output:
```json
{
    "result": [
        {
            "name": "Project A",
            "description": "Description of Project A",
            "link": "https://example.com/project-a"
        },
        {
            "name": "Project B",
            "description": "Description of Project B",
            "link": "https://example.com/project-b"
        }
    ]
}
```

---

## Troubleshooting

### Common Issues

1. **Virtual Environment Not Found**:
   - Ensure the virtual environment was created and activated correctly.

2. **ModuleNotFoundError**:
   - Check that all dependencies are installed by running:
     ```bash
     pip install -r requirements.txt
     ```

3. **500 Internal Server Error**:
   - Verify your `.env` file contains a valid `OPENAI_API_KEY`.

4. **Subprocess Errors**:
   - Ensure the `subprocess_scraper.py` file is in the correct directory (`backend/app/`).

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── scrape_utils.py
│   └── subprocess_scraper.py
├── fintech-env/  # Virtual environment (not in Git)
├── requirements.txt
└── README.md
```

---