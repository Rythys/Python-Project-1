from pathlib import Path
from typing import Generator, Dict, Any


def scanner(PATH: str) -> Generator[Dict[str, Any], None, None]:

    """
    Рекурсивно сканирует директорию и возвращает информацию о файлах.

    Аргументы:
        directory_path (str): Путь к директории для сканирования.

    Возвращает:
        Generator: Генерирует словари с данными о файлах:
            - path (str): Абсолютный путь к файлу.
            - size (int): Размер файла в байтах.
            - extension (str): Расширение файла (например, '.py').

    Исключения:
        FileNotFoundError: Если указанный путь не существует.
    """

    # Создание типа Path для текущей директории
    current_dir_path = Path(PATH)

    # Проверка существования полученного пути
    if not current_dir_path.exists():
        raise FileNotFoundError(f"{current_dir_path} does not exist")

    # Проверка является ли полученный путь файлом
    if not current_dir_path.is_dir():
        yield {
                "path": str(current_dir_path.absolute()),
                "size": current_dir_path.stat().st_size,
                "extension": current_dir_path.suffix
            }
        return

    # Рекурсивный обход полученного пути
    for inner_file in current_dir_path.rglob('*'):
        if inner_file.is_file():
            yield {
                "path": str(inner_file.absolute()),
                "size": inner_file.stat().st_size,
                "extension": inner_file.suffix
            }
    


