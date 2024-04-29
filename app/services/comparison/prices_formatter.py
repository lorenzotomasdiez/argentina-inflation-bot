def prices_by_kg_and_units(prices, product_markets, markets, date):
  """
    {
      product_id: number,
      price: number,
      date: date,
      name: string,
      market_name: string,
      market_id: number,
    }
  """
  result = {}
  
  for product in product_markets:
    product_id = product["product_id"]
    product_name = product["name"]
    product_market_id = product["market_id"]
    product_type = product["measurement"]
    product_quantity = product["quantity"]
    
    price = next((price for price in prices if (price["product_id"] == product_id and price["market_id"] == product_market_id) ), None)
    market = next((market for market in markets if market["id"] == product_market_id), None)
    
    
    if price is not None and market is not None:
      # if product_type is kg then product_price is the product_quantity part of a kg
      if product_type == "kg" or product_type == "l":
        product_price = price["price"] / product_quantity
      else:
        product_price = price["price"] * product_quantity
        
      market_name = market["name"]
      
      result.update({product_id: {
        "product_id": product_id,
        "price": product_price,
        "date": date,
        "name": product_name,
        "market_name": market_name,
        "market_id": product_market_id
      }})
    
    else:
      print(f"COMPARISON_SERVICE - compare.py - prices_by_kg_and_units: price or market is None - {product_name}")
  
  return result
      
  
  
    