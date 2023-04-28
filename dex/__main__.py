import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))


if __name__ == "__main__":
    from dex.cli import app

    app()
