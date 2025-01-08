import asyncio
import json
import subprocess
import os

def run_scraper_subprocess(prompt, source_url):
    """
    Run the scraper in a separate subprocess to avoid asyncio conflicts.

    Args:
        prompt (str): The prompt to pass to the LLM.
        source_url (str): The URL of the page to scrape.

    Returns:
        dict: The result from the scraper.
    """
    script_path = os.path.join(os.path.dirname(__file__), "subprocess_scraper.py")

    # Ensure the script exists
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Subprocess script not found: {script_path}")
    # Path to the Python executable within the virtual environment
    python_executable = os.path.join(
        os.getenv("fintech-env") or "", "bin", "python3"
    )
    # Fallback to system Python if VIRTUAL_ENV is not set
    if not os.path.exists(python_executable):
        python_executable = "python3"

    # Command to execute the scraper script in a subprocess
    process = subprocess.run(
        [
            "python3",
            script_path,
            json.dumps({"prompt": prompt, "source_url": source_url}),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if process.returncode != 0:
        raise RuntimeError(
            f"Subprocess failed with error: {process.stderr}"
        )

    return json.loads(process.stdout)



async def run_scraper(prompt, source_url):
    """
    Wrapper for the subprocess call to integrate with FastAPI's async system.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, run_scraper_subprocess, prompt, source_url
    )

async def run_searchscraper(prompt):
    """
    Wrapper for the subprocess call to integrate with FastAPI's async system.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, run_searchscraper_subprocess, prompt
    )

def run_searchscraper_subprocess(prompt):
    """
    Run the scraper in a separate subprocess to avoid asyncio conflicts.

    Args:
        prompt (str): The prompt to pass to the LLM.
        source_url (str): The URL of the page to scrape.

    Returns:
        dict: The result from the scraper.
    """
    script_path = os.path.join(os.path.dirname(__file__), "subprocess_searchscraper.py")

    # Ensure the script exists
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Subprocess script not found: {script_path}")
    # Path to the Python executable within the virtual environment
    python_executable = os.path.join(
        os.getenv("venv") or "", "bin", "python3"
    )
    # Fallback to system Python if VIRTUAL_ENV is not set
    if not os.path.exists(python_executable):
        python_executable = "python3"

    # Command to execute the scraper script in a subprocess
    process = subprocess.run(
        [
            "python3",
            script_path,
            json.dumps({"prompt": prompt}),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Log subprocess output
    print(f"STDOUT: {process.stdout}")
    print(f"STDERR: {process.stderr}")

    # Check if the output is empty or invalid
    if not process.stdout.strip():
        raise RuntimeError("Subprocess returned no output")

    if process.returncode != 0:
        raise RuntimeError(
            f"Subprocess failed with error: {process.stderr}"
        )

    return process.stdout
