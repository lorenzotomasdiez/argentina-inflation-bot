from .product_market_dia import seed_products_markets_dia
from services.db.products.index import get_all_products
from .drop import drop_all
from .product import seed_products
from .market import seed_markets
from .product_market_cotto import seed_products_markets_cotto
from .product_market_carrefour import seed_products_markets_carrefour
from .prices import seed_prices
from .variables import create_bcra_variables

def seed_data():
    drop_all()
    products = seed_products()
    markets = seed_markets()
    seed_products_markets_cotto(products_seeded=products)
    seed_products_markets_dia(products_seeded=products)
    seed_prices(markets=markets, products=products)
    return "Data table seed succesfully done!"

def single_seed_markets():
    seed_markets()
    return "Markets table seed succesfully done!"

def single_seed_products_markets_carrefour():
    products = get_all_products()
    seed = seed_products_markets_carrefour(products_seeded=products)
    if "error" in seed:
        raise Exception(seed)
    return "Products markets carrefour table seed succesfully done!"

def seed_bcra_variables():
    variables = create_bcra_variables()
    return variables