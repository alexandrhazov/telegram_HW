import json
import requests
import config


class ApiException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = config.exchanges[base.lower()]
        except KeyError:
            return ApiException(f'Валюта {base} не найдена')

        try:
            sym_key = config.exchanges[sym.lower()]
        except KeyError:
            return ApiException(f'Валюта {sym} не найдена')

        if base_key == sym_key:
            raise ApiException(f'Невозможно конвертировать одинакоые валюты!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise ApiException(f'Невозможно обработать количество валюты {amount}!')

        r = requests.get(f"http://api.exchangeratesapi.io/v1/latest?access_key="
                         f"{config.API_KEY}&base={base_key}&symbols={sym_key}")
        resp = json.loads(r.content)
        print(resp)
        new_price = resp['rates'][sym_key] * float(amount)
        return round(new_price, 2)
