from typing import List

class WishlistManager:

    def __init__(self):
        self.wishlist = [
            'https://www.buscalibre.cl/v2/pendientes_486712_l.html',
            'https://www.buscalibre.cl/v2/daredevil-mark-waid_1520599_l.html',
            'https://www.buscalibre.cl/v2/software-development_503034_l.html',
            'https://www.buscalibre.cl/v2/comics_545021_l.html',
            'https://www.buscalibre.cl/v2/pendientes-2_567662_l.html',
            'https://www.buscalibre.cl/v2/historia_606807_l.html',
            'https://www.buscalibre.cl/v2/feminismo_624086_l.html',
            'https://www.buscalibre.cl/v2/pendientes-3_657656_l.html',
            'https://www.buscalibre.cl/v2/latinoamericana_711603_l.html',
            'https://www.buscalibre.cl/v2/estudio_727965_l.html',
            'https://www.buscalibre.cl/v2/literatura_729752_l.html',
            'https://www.buscalibre.cl/v2/contra_737670_l.html',
            'https://www.buscalibre.cl/v2/english-books_816771_l.html',
            'https://www.buscalibre.cl/v2/filosofia-sociologia_830510_l.html',
            'https://www.buscalibre.cl/v2/cortos_831079_l.html',
            'https://www.buscalibre.cl/v2/tolkien_921085_l.html',
            'https://www.buscalibre.cl/v2/fullmetal_1003773_l.html',
            'https://www.buscalibre.cl/v2/cuentos_1079781_l.html',
            'https://www.buscalibre.cl/v2/estudio2_1218140_l.html',
            'https://www.buscalibre.cl/v2/emprendimientos-y-finanzas_1450796_l.html',
            'https://www.buscalibre.cl/v2/literatura-2_1469636_l.html',
            'https://www.buscalibre.cl/v2/gantz_1488040_l.html',
            'https://www.buscalibre.cl/v2/manga_1488300_l.html',
            'https://www.buscalibre.cl/v2/chile_1536612_l.html',
        ]

    
    def add_url(self, url: str) -> None:
        self.wishlist.append(url)

    def remove_url(self, url: str) -> None:
        self.wishlist.remove(url)

    def get_wishlist(self) -> List[str]:
        return self.wishlist