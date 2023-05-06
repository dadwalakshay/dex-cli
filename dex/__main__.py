import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

load_dotenv(override=True)


if __name__ == "__main__":
    from dex.cli import app

    app()
