from config import get_month_from_date
from services.variation.variation import calculate_products_more_variation
from .send import send_message

def send_general_variation():
    variation = calculate_products_more_variation()

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

    return {"success": "General Variation Sent"}


def generate_general_message(price_variation, to_var):
    to_day = to_var.split("-")[2]
    to_month = get_month_from_date(to_var)

    """
        EXAMPLE MESSAGE:
        La variación de precios de la canasta básica en el mes de Abril al día 22 es del 1.94%.
    """
    message_to_send = f"La variación de precios de la canasta básica en el mes de {to_month} al día {to_day} es del {price_variation}%."
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
