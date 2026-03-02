from pathlib import Path
from typing import Generator, Any

from .decorators import log_calls, measure_time
from .filters import is_file_filtered_by_args


@measure_time("<SCAN_TIME>")
@log_calls
def scanner(args) -> Generator[dict[str, Any], None, None]:
    """
    Recursively scans the directory and returns information about the files.

    """

    current_dir_path = Path(args.path)

    if not current_dir_path.exists():
        print(current_dir_path)
        raise FileNotFoundError(f"{current_dir_path} does not exist")

    if not current_dir_path.is_dir():
        try:
            yield {
                "path": str(current_dir_path.absolute()),
                "size": current_dir_path.stat().st_size,
                "extension": current_dir_path.suffix
            }
        except PermissionError as e:
            raise e(f"Critical directory access error {current_dir_path}")
        except OSError as e:
            raise e(f"Failed to read to {current_dir_path}")

        return

    try:
        # Recursive walk along path     
        for inner_file in current_dir_path.rglob('*'):
            if inner_file.is_file():
                try:
                    if is_file_filtered_by_args(inner_file, args):
                        yield {
                            "path": str(inner_file.absolute()),
                            "size": inner_file.stat().st_size,
                            "extension": str(inner_file.suffix)
                        }
                except PermissionError:
                    continue
    except PermissionError as e:
        print(f"Critical directory access error {current_dir_path}: {e}")
    except OSError as e:
        print(f"Failed to read {current_dir_path}: {e}")