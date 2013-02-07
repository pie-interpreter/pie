import os
import glob

__all__ = [
    os.path.basename(filename)[:-3] for filename in glob.glob(
        os.path.dirname(__file__) + "/*.py"
    )
]
