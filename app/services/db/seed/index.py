from services.db.products.index import get_all_products
from services.db.seed.drop import drop_all
from services.db.seed.product import seed_products
from services.db.seed.market import seed_markets
from services.db.seed.product_market_cotto import seed_products_markets_cotto
from services.db.seed.product_market_carrefour import seed_products_markets_carrefour
from services.db.seed.prices import seed_prices

def seed_data():
    drop_all()
    products = seed_products()
    markets = seed_markets()
    product_markets_cotto = seed_products_markets_cotto(markets_seeded=markets, products_seeded=products)
    product_markets_carrefour = seed_products_markets_carrefour(products_seeded=products)
    prices = seed_prices(markets=markets, products=products)
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
