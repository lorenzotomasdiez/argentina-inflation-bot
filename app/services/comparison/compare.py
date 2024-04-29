import datetime as dt
import pandas as pd
from services.db.market.index import get_markets_info
from services.db.products_markets.index import get_all_products_markets
from services.db.prices.index import get_all_prices_by_date
from .prices_formatter import prices_by_kg_and_units
from config import get_date_now


def compare_markets():
  """
    Compare the prices of the products in the markets
    prices_lists: list of prices with market_id and product_id
    return: list of prices with the comparison
  """
  
  markets = get_markets_info()
  
  today = get_date_now()
  
  prices = get_all_prices_by_date(today)
  
  market_1_products = get_all_products_markets(market_id = 1)
  market_2_products = get_all_products_markets(market_id = 4)
  
  market_1_prices = prices_by_kg_and_units(prices, market_1_products, markets, today)
  market_2_prices = prices_by_kg_and_units(prices, market_2_products, markets, today)
  
  for product_id in market_1_prices:
    if product_id in market_2_prices:
      product_1_price = market_1_prices[product_id]["price"]
      product_2_price = market_2_prices[product_id]["price"]
      
      product_name = market_1_prices[product_id]["name"]
      
      market_1_name = market_1_prices[product_id]["market_name"]
      market_2_name = market_2_prices[product_id]["market_name"]
      
      if product_1_price < product_2_price:
        print(f"Product {product_name} is cheaper in {market_1_name} - ${product_1_price} than in {market_2_name} - ${product_2_price}")  
      elif product_1_price > product_2_price:
        print(f"Product {product_name} is cheaper in {market_2_name} - ${product_2_price} than in {market_1_name} - ${product_1_price}")
        
      else:
        print(f"Product {product_name} has the same price in {market_1_name} and {market_2_name} -> ${product_1_price}")
      
    else:
      print(f"Product {market_1_prices[product_id]['name']} is not in market 2")
  
  return{
    "market_1": market_1_prices,
    "market_2": market_2_prices
  }