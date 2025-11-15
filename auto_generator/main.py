import re
import json
import copy
import random
from nAi import nAi
from parameters import init_parameters, PARAMETERS

init_parameters()

NUM_REQUESTS : int = 300

AI : nAi = nAi(
    PARAMETERS['AI_MODEL'],
    PARAMETERS['AI_TOKEN'],
    PARAMETERS['AI_URL'],
    PARAMETERS['AI_RESPONSE_TIMEOUT'],
    PARAMETERS['AI_POST_JSON'],
    PARAMETERS['AI_HISTORY_CHAT_LIMIT']
)

GENERATE_CONFLICT : str = open(PARAMETERS['INSTRACTION_FILE'], "r", encoding="utf-8").read()
TO_RECORD : str = open(PARAMETERS['TO_RECORD_FILE'], "r", encoding="utf-8").read()
EXTRA : str = """
    Поле instructions добно оставаться пустым.
    Все остальные поля должны быть заполненными, исходя и ситуации.
    Поле quality_score - случайное число от 0.8 - 0.98
"""

PROMPT : str = " ".join([
    GENERATE_CONFLICT,
    TO_RECORD,
    EXTRA
])

HISTORY : list = []

RECORD_SCHEME : dict = json.loads(
    open(PARAMETERS['RECORD_SCHEME'], "r", encoding="utf-8").read()
)

def rand_2digit() -> int:
    return random.randint(10,99)

def create_dataset(data: list[dict], filename: str, format: str = "json") -> None:
    if format == "json":
        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    else:
        raise ValueError(f"Unsupported format: {format}")

def format_to_dict(content: str) -> dict:
    output: dict = copy.deepcopy(RECORD_SCHEME)

    for char in ["`", "json", "txt", "\n"]:
        content = content.replace(char, "")

    data = json.loads(content)

    output['input'] = data['input']
    output['output'] = data['output']

    output['conflict_info']['situation'] = data['conflict_info']['situation']
    output['conflict_info']['conflict_type'] = data['conflict_info']['conflict_type']

    output['conflict_info']['attack']['name'] = data['conflict_info']['attack']['name']
    output['conflict_info']['attack']['formal_role'] = data['conflict_info']['attack']['formal_role']

    output['conflict_info']['defence']['name'] = data['conflict_info']['defence']['name']
    output['conflict_info']['defence']['formal_role'] = data['conflict_info']['defence']['formal_role']

    output['conflict_info']['is_public'] = data['conflict_info']['is_public']
    output['conflict_info']['negotiation_subject'] = data['conflict_info']['negotiation_subject']
    output['conflict_info']['attack_trigger'] = data['conflict_info']['attack_trigger']

    output['context'] = data['context']
    output['quality_score'] = data['quality_score']
    output['metadata']['industry'] = data['metadata']['industry']

    return output

def main() -> None:
    records : list[dict] = list()
    plaint_records : list[dict] = list()

    for _ in range(NUM_REQUESTS):

        print("Отпавка запроса...")

        try:
            response = AI.generate(
                PROMPT,
                HISTORY
            )

            try:
                response = format_to_dict(response)
                print(f"ЧИСЛО ГЕНЕРАЦИЙ: {_}\n\n")

                records.append(response)
            except Exception as e:
                print(f"{e}\n\n")
                print(f"ERROR: \n {response} \n")

                plaint_records.append({
                    "record" : response
                })
        except Exception as e:
            print(f"Ошибка получения запроса:\n {e}")

    serios : str = f"{rand_2digit()}_{rand_2digit()}_{rand_2digit()}_{rand_2digit()}"

    if len(records) > 0:
        create_dataset(records, f"conflict_situations_{serios}.json")

    if len(plaint_records) > 0:
        create_dataset(plaint_records, f"plaint_records_{serios}.json")

    print("Генерация завершена")
    print(f"Статистика:\n Кол-во записей: {len(records)}\n Кол-во не обработанных записей: {len(plaint_records)}")

if __name__ == "__main__":
    main()