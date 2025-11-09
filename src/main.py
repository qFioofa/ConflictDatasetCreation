from src.parameters import dec_init_parameters, PARAMETERS


def read_json(filename : str) -> str | None:
    output : str | None = None

    try:
        with open(file=filename, mode="r", encoding=""):
            pass
    except Exception as e:
        print(e)

    return output

@dec_init_parameters()
def main() -> None:
    global PARAMETERS

    try:
        pass
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()