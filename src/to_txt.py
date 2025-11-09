import os
from pathlib import Path

MD_PATH : str = "../prompts/md/"
TXT_PATH : str = "../prompts/txt/"

def main() -> None:
    global MD_PATH, TXT_PATH

    source_folder = Path(MD_PATH)
    destination_folder = Path(TXT_PATH)

    if not source_folder.exists():
        print(f"Папка {source_folder} не найдена.")
        return

    destination_folder.mkdir(parents=True, exist_ok=True)

    md_files = list(source_folder.glob("*.md"))

    for md_file in md_files:
        txt_file: Path = destination_folder / f"{md_file.stem}.txt"

        with md_file.open('r', encoding='utf-8') as f:
            content: str = f.read()

        with txt_file.open('w', encoding='utf-8') as f:
            f.write(content)

        print(f"Файл {md_file.name} преобразован в {txt_file.name}")

if __name__ == "__main__":
    main()