from pathlib import Path
from filters import is_filtered_by_extension, is_filtered_by_min_size, is_filtered_by_max_size, is_filtered_by_name
from typing import Generator, Any


def scanner(args) -> Generator[dict[str, Any], None, None]:
    """

    Recursively scans the directory and returns information about the files.

    """

    current_dir_path = Path(args.path)

    if not current_dir_path.exists():
        print(current_dir_path)
        raise FileNotFoundError(f"{current_dir_path} does not exist")

    if not current_dir_path.is_dir():
        yield {
                "path": str(current_dir_path.absolute()),
                "size": current_dir_path.stat().st_size,
                "extension": current_dir_path.suffix
            }
        return

    # Recursive walk along path
    for inner_file in current_dir_path.rglob('*'):
        if inner_file.is_file():
            # Filter file by arguments
            if is_filtered_by_extension(inner_file, args.ext) and \
               is_filtered_by_min_size(inner_file, args.min_size) and \
               is_filtered_by_max_size(inner_file, args.max_size) and \
               is_filtered_by_name(inner_file, args.name):
                yield {
                    "path": str(inner_file.absolute()),
                    "size": inner_file.stat().st_size,
                    "extension": str(inner_file.suffix)
                }
    


