from services.db.seed.drop import drop_all
from services.db.seed.product import seed_products
from services.db.seed.market import seed_markets
from services.db.seed.product_market import seed_products_markets
from services.db.seed.prices import seed_prices


def seed_data():
    drop_all()
    products = seed_products()
    markets = seed_markets()
    product_markets = seed_products_markets(markets_seeded=markets, products_seeded=products)
    prices = seed_prices(markets=markets, products=products)
    return "Data table seed succesfully done!"
