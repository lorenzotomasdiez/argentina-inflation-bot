from config import get_month_from_date
from services.variation.variation import calculate_products_more_variation
from .send import send_message
import matplotlib.pyplot as plt

def send_general_variation(market_id):
    variation = calculate_products_more_variation(market_id)

    products = variation.get("products")
    price_variation = variation.get("price_variation")
    to_var = variation.get("to") # YYYY-MM-DD

    if (
        products is None
        or len(products) < 1
        or price_variation is None
        or to_var is None
    ):
        return None

    general_message = generate_general_message(price_variation, to_var)
    send_message(general_message)

    most_variation_message = generate_most_variation_message(products, to_var)
    send_message(most_variation_message)

    generate_negative_message = generate_negative_variation_message(products, to_var)
    send_message(generate_negative_message)
    
    generate_variation_bar_chart(products, to_var, market_name="Coto")

    return {"success": "General Variation Sent"}


def generate_general_message(price_variation, to_var):
    to_day = to_var.split("-")[2]
    to_month = get_month_from_date(to_var)

    """
        EXAMPLE MESSAGE:
        La variación de precios de la canasta básica en el mes de Abril al día 22 es del 1.94%.
    """
    message_to_send = f"La variación de precios de la canasta básica en el mes de {to_month} al día {to_day} es del {round(price_variation, 2)}%."
    return message_to_send

def generate_most_variation_message(products, to_var):
    """
        EXAMPLE MESSAGE:
            Los productos con mayor aumento de Abril al día de hoy 22 son:
            125.23% para batata,
            66.72% para choclo,
            58.05% para cafe,
            44.60% para yerba
    """
    to_day = to_var.split("-")[2]
    to_month = get_month_from_date(to_var)

    message_to_send = f"Los productos con mayor aumento de {to_month} al día de hoy {to_day} son:"

    # get products with more variation in "variation" key
    subproducts = sorted(products, key=lambda x: x.get("variation"), reverse=True)[:4]

    for product in subproducts:
        product_name = product.get("name")
        product_variation = product.get("variation")
        message_to_send += f"\n{product_variation}% para {product_name}"

    return message_to_send

def generate_negative_variation_message(products, to_var):
    """
        EXAMPLE MESSAGE:
            Los productos con mayor disminución de Abril al día de hoy 22 son:
            -125.23% para batata,
            -66.72% para choclo,
            -58.05% para cafe,
            -44.60% para yerba
    """
    to_day = to_var.split("-")[2]
    to_month = get_month_from_date(to_var)

    message_to_send = f"Los productos con mayor disminución de {to_month} al día de hoy {to_day} son:"

    # get products with more variation in "variation" key
    subproducts = sorted(products, key=lambda x: x.get("variation"), reverse=False)[:4]

    for product in subproducts:
        product_name = product.get("name")
        product_variation = product.get("variation")
        message_to_send += f"\n{product_variation}% para {product_name}"

    return message_to_send


def generate_variation_bar_chart(products, to_var, market_name, top_n=10):
    to_day = to_var.split("-")[2]
    to_month = get_month_from_date(to_var)

    # Filtrar productos con variación no nula
    filtered_products = [product for product in products if product.get("variation") is not None]

    # Ordenar los productos por variación de mayor a menor
    sorted_products = sorted(filtered_products, key=lambda x: x.get("variation"), reverse=True)

    # Obtener los top_n productos con las mayores variaciones (positivas y negativas)
    top_products = sorted_products[:top_n] + sorted_products[-top_n:]

    # Extraer nombres y variaciones de los productos seleccionados
    product_names = [product.get("name") for product in top_products]
    variations = [product.get("variation") for product in top_products]

    plt.figure(figsize=(10, 6))
    plt.barh(product_names, variations, color='skyblue')
    plt.xlabel('Variación (%)')
    plt.ylabel('Producto')
    plt.title(f'Variación de precios al día {to_day} de {to_month} | Supermercado: {market_name}')
    plt.gca().invert_yaxis()  
    plt.grid(axis='x')  
    plt.tight_layout()

    # Guardar el gráfico como imagen en lugar de mostrarlo en pantalla
    plt.savefig('variation_chart.png', bbox_inches='tight')
    plt.close()  # Cerrar la figura para liberar recursos
