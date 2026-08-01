import logging
from datetime import datetime
from pathlib import Path


def configure_logging():
    log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
    logs_dir = Path(__file__).resolve().parent.parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file_path = logs_dir / log_file
    logging.basicConfig(
        filename=str(log_file_path),
        format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        force=True,
    )
    return log_file_path


