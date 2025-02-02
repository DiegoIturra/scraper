from functools import reduce

class Utils:

    @staticmethod
    def parse_price_into_number(price: str) -> int:
        if not price:
            return None

        tokens = price.split('$')
        last_token = tokens[-1:][0].strip()

        extracted_values = last_token.split('.')

        price = reduce(lambda x, y: x + y, extracted_values)
        return int(price)