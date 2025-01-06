import os
import subprocess
import json
import asyncio

class SubprocessManager:
    def __init__(self, script_name):
        self.script_path = os.path.join(os.path.dirname(__file__), "..", "scrapers", script_name)
        if not os.path.exists(self.script_path):
            raise FileNotFoundError(f"Subprocess script not found: {self.script_path}")

    def run_subprocess(self, prompt, source_url):
        """
        Run the subprocess for the specified scraper script.
        """
        python_executable = os.path.join(
            os.getenv("VIRTUAL_ENV") or "", "bin", "python3"
        )
        if not os.path.exists(python_executable):
            python_executable = "python3"

        process = subprocess.run(
            [
                python_executable,
                self.script_path,
                json.dumps({"prompt": prompt, "source_url": source_url}),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if process.returncode != 0:
            raise RuntimeError(f"Subprocess failed with error: {process.stderr}")

        return json.loads(process.stdout)

    async def run(self, prompt, source_url):
        """
        Async wrapper for subprocess execution.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.run_subprocess, prompt, source_url)
