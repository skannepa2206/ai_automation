import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_FOLDER = "sample_inputs/"  # Folder where emails & PDFs arrive
VENV_PYTHON = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv", "Scripts", "python.exe")


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Triggers when a new file is created in the folder."""
        if event.is_directory:
            return

        file_path = event.src_path
        print(f"New file detected: {file_path}")

        # Run extract.py to process the new file using virtual environment Python
        print("Running extraction script...")
        try:
            subprocess.run([VENV_PYTHON, "extract.py"], check=True)

            # Run Trello automation script after extraction
            print("Running Trello automation...")
            subprocess.run([VENV_PYTHON, "trello_automation.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running script: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)

    print(f"📂 Watching folder: {WATCH_FOLDER} for new emails & PDFs...")
    observer.start()

    try:
        while True:
            time.sleep(5)  # Keep checking for new files
    except KeyboardInterrupt:
        observer.stop()

    observer.join()