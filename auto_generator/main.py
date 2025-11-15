import json
import re
import copy
import random
from nAi import nAi
from parameters import init_parameters, PARAMETERS

init_parameters()

NUM_REQUESTS : int = 1

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


def create_dataset(data: list[dict], filename: str, format: str = "json") -> None:
    if format == "json":
        with open(filename, mode='w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
def fromat_to_dict(content : str) -> dict:
    
    raise Exception("Can't format to dict")

def main() -> None:
    records : list[dict] = list()

    plaint_records : list[dict] = list()

    for _ in range(NUM_REQUESTS):
        response = AI.generate(
            PROMPT,
            HISTORY
        )

        try:
            response = fromat_to_dict(response)
            print(f"ЧИСЛО ГЕНЕРАЦИЙ: {_}\n\n")
            print(response)

            records.append(response)
        except Exception as e:
            print(f"{e}\n\n")
            print(f"ERROR: {response} \n")

            plaint_records.append({
                "record" : response
            })

    create_dataset(records, f"conflict_situations_{random.randint(10,99)}_{random.randint(10,99)}_{random.randint(10,99)}_{random.randint(10,99)}")

    if len(plaint_records) > 0:
        create_dataset(plaint_records, f"plaint_records.json")

if __name__ == "__main__":
    main()