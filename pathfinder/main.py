import logging
from logging.handlers import RotatingFileHandler
import datetime
from pathlib import Path
from pathfinder.helpers.config_manager import config
from pathfinder.tui import PathfinderTUI

"""
Main execution entry point for the entire project.
Global logging settings are configured here as well.
"""

def set_logging_options():
    """ Used to set global logging options """

    root_path = Path(__file__).resolve().parent

    # Configuring global logging options
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_filename = f"app_{current_date}.log"
    log_path = root_path / "logs" / log_filename
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=100*1024*1024,
        backupCount=5
    )

    logging.basicConfig(
        level=config.logging_level,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[file_handler]
    )

def main():
    set_logging_options()    

    # Run the PathfinderTUI
    app = PathfinderTUI()
    app.run()

if __name__ == "__main__":
    main()