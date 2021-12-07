import requests  # type: ignore


def get_data() -> list:
    r = requests.post(
        "https://service.nalog.ru/addrno-proc.json",
        data={"step": 1, "oktmmf": 40913000, "ifns": 7840, "npKind": "fl", "c": "next"},
    )

    info = r.json()
    return [
        info["payeeDetails"]["payeeName"],
        info["payeeDetails"]["payeeInn"],
        info["payeeDetails"]["payeeKpp"],
        info["payeeDetails"]["bankName"],
        info["payeeDetails"]["bankBic"],
        info["payeeDetails"]["payeeAcc"],
    ]


if __name__ == "__main__":
    print(get_data())
