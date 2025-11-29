import logging
from logging.handlers import RotatingFileHandler
import datetime
from pathlib import Path
from pathfinder.helpers.config_loader import load_config
from pathfinder.tui import PathfinderTUI

"""
Main execution entry point for the entire project.
Global logging settings are configured here as well.
"""

def set_logging_options():
    """ Used to set global logging options """

    config_file = 'config.json'

    root_path = Path(__file__).resolve().parent

    # Load data from config.json
    config_data = load_config(root_path / config_file)

    # Set the deault logging level to INFO
    level = logging.INFO

    # Checks there is config_data, then set the logging level
    if config_data:
        logging_level = config_data.get("logging_level", "INFO")
        if logging_level != "INFO":
            level = logging_level

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
        level=level,
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