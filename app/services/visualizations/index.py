import matplotlib.pyplot as plt
from config import get_month_from_date

def generate_variation_bar_chart(products, to_var, market_name, top_n=10):
  to_day = to_var.split("-")[2]
  to_month = get_month_from_date(to_var)
  
  filtered_products = [product for product in products if product.get("variation") is not None]

  sorted_products = sorted(filtered_products, key=lambda x: x.get("variation"), reverse=True)

  top_products = sorted_products[:top_n] + sorted_products[-top_n:]

  product_names = [product.get("name") for product in top_products]
  variations = [product.get("variation") for product in top_products]

  plt.figure(figsize=(10, 6))
  plt.barh(product_names, variations, color='skyblue')
  plt.xlabel('Variación (%)')
  plt.ylabel('Producto')
  plt.title(f'Variación de precios al día {to_day} de {to_month} | Supermercado: {market_name} | x:@ahorro_bot')
  plt.gca().invert_yaxis()  
  plt.grid(axis='x')  
  plt.tight_layout()

  # Guardar el gráfico como imagen en lugar de mostrarlo en pantalla
  plt.savefig('variation_chart.png', bbox_inches='tight')
  plt.close()  # Cerrar la figura para liberar recursos
