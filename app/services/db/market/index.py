from config import get_db_connection
def get_markets_info():
  connection = get_db_connection()
  cursor = connection.cursor()

  cursor.execute(
    """
    SELECT * FROM markets
    """
  )
  
  markets = []
  
  for market in cursor.fetchall():
    markets.append({
      "id": market[0],
      "name": market[1],
    })

  cursor.close()
  
  return markets