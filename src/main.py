import os
import json
from parameters import dec_init_parameters, PARAMETERS

SCHEME: dict | None = None
INTRUCTION: str | None = None

INTRUCTION_DEFAULT : str = "Придумай конфликтную ситуацию"

def read_json(filename: str) -> dict | None:
    output: dict | None = None

    try:
        with open(file=filename, mode="r", encoding="utf-8") as file:
            content: str = file.read()
            output = json.loads(content)
    except Exception as e:
        print(e)
        output = None

    return output

def record_check(record: dict) -> bool:
    global PARAMETERS, SCHEME

    if SCHEME is None:
        SCHEME = read_json(PARAMETERS['RECORD_SCHEME'])

    def _check_structure(data, schema) -> bool:
        if isinstance(schema, dict):
            if not isinstance(data, dict):
                return False
            if set(schema.keys()) != set(data.keys()):
                return False
            for key, value in schema.items():
                if not _check_structure(data[key], value):
                    return False
            return True
        elif isinstance(schema, list):
            if not isinstance(data, list):
                return False
            if not schema:
                return True
            for item in data:
                if not _check_structure(item, schema[0]):
                    return False
            return True
        else:
            return type(data) == type(schema)

    return _check_structure(record, SCHEME)

def instruction_insertion(record : dict, instruction_field : str = "instruction") -> dict:
    global INTRUCTION, INTRUCTION_DEFAULT, PARAMETERS

    if INTRUCTION is None:
        filename : str = PARAMETERS['INSTRACTION_FILE']
        try:
            with open(file=filename, mode="r", encoding="utf-8") as file:
                INTRUCTION = file.read()
        except Exception:
            print("Instruction is not loaded...\nInserting default instruction...\n")
            INTRUCTION = INTRUCTION_DEFAULT

    record[instruction_field] = INTRUCTION

    return record

def read_files_from_folder(folder: str) -> list[str]:
    try:
        files: list[str] = os.listdir(folder)
        file_paths: list = []
        for file in files:
            path: str = os.path.join(folder, file)
            if os.path.isfile(path):
                file_paths.append(path)
        return file_paths
    except Exception as e:
        print(e)
        return []

def create_dataset(data: list[dict], filename: str, format: str = "json") -> None:
    if format == "json":
        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    else:
        raise ValueError(f"Unsupported format: {format}")

@dec_init_parameters()
def main() -> None:
    global PARAMETERS

    valid_records : list[dict] = list()
    try:
        folder : str = PARAMETERS['RECORDS_FOLDER']
        record_files : list[str] = read_files_from_folder(folder)
        if len(record_files) == 0:
            raise Exception(f"No records in folder: {folder} provided")

        for record_file in record_files:
            record_file_content : dict = read_json(record_file)

            if not isinstance(record_file_content, list):
                print(f"Root in file: {record_file} is not list.\nContinue merging...\n")
                continue

            for record_instance in record_file_content:
                if not record_check(record_instance):
                    print(f"Record: {record_instance}\nDoes not match with scheme")
                    continue

                record_instance_full: dict = instruction_insertion(record_instance)
                valid_records.append(record_instance_full)

        dataset_name : str = PARAMETERS['OUTPUTFILE']
        create_dataset(valid_records, dataset_name)
        print("Dataset has been created")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()