import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

load_dotenv(override=True)


if __name__ == "__main__":
    import ipdb

    from dex.cli import app

    ipdb.set_trace()

    app()
