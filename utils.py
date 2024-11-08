from functools import reduce

class Utils:

    @staticmethod
    def extract_name_from_url(url: str):
        tokens = url.split('/')
        last_token = tokens[-1:]
        wishlist_name = last_token[0].split('_')[0]
        return wishlist_name

    @staticmethod
    def parse_price_into_number(price: str):
        if not price:
            return None

        tokens = price.split('$')
        last_token = tokens[-1:][0].strip()

        extracted_values = last_token.split('.')

        price = reduce(lambda x, y: x + y, extracted_values)
        return int(price)