"""Небольшой воспроизводимый профиль командного обработчика (cProfile)."""

import cProfile
import io
import pstats
import sys
from pathlib import Path
from contextlib import redirect_stdout

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from processor import CommandProcessor  # pylint: disable=wrong-import-position


def run_commands() -> None:
    """Прогнать один и тот же набор команд многократно."""
    with redirect_stdout(io.StringIO()):
        for index in range(100):
            processor = CommandProcessor()
            processor.process_command(f'ADD SONG "Песня {index}" 4.25 "Автор"')
            processor.process_command(f'ADD SYMPHONY "Симфония {index}" 31.2 "Композитор"')
            processor.process_command('REM duration > 30')
            processor.process_command('PRINT')


if __name__ == "__main__":
    profile = cProfile.Profile()
    profile.runcall(run_commands)
    stats = pstats.Stats(profile)
    stats.strip_dirs().sort_stats("cumulative").print_stats(15)
