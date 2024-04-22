import psycopg2
import pandas as pd
from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER, prices_dir
def seed_prices(products, markets):
    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

    cursor = connection.cursor()

    #create table if not exists
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prices (
            id SERIAL PRIMARY KEY,
            product_id  INTEGER REFERENCES products(id) NOT NULL,
            market_id INTEGER REFERENCES markets(id) NOT NULL,
            price FLOAT NOT NULL,
            date DATE NOT NULL
        )
        """
    )

    prices_df = pd.read_csv(prices_dir, sep=",", encoding="utf-8")

    # iterate through df and insert into table
    # match product.format_name with row in prices_df
    market = next((market for market in markets if market["name"] == "coto"), None)
    if market is None:
        return "Market not found"

    # example of df headers:
    #id,fecha,pan_frances,galletitas_dulces,galletitas_de_agua,harina_de_trigo,harina_de_maiz,arroz,fideos_secos,asado,carnaza_comun,hueso_con_carne,paleta,carne_picada,nalga,higado,pechito_de_cerdo,pollo,carne_de_pescado,mortadela,paleta_cocida,salchich¢n,salame,aceite_de_girasol,margarina_para_cocinar,leche_fluida,leche_en_polvo_entera,queso_crema,queso_cuartirolo,queso_de_rallar,manteca,yogur,dulce_de_leche,huevo,manzana,naranja,banana,pera,batata,papa,acelga,cebolla,choclo,lechuga,tomate_perita,zanahoria,zapallo,tomate_envasado,arvejas_en_lata,lentejas_secas,azucar,dulce_de_batata,mermelada,sal_fina,mayonesa,vinagre,caldo_concentrado,gaseosas,jugos_concentrados,soda,cerveza,vino,cafe,yerba,te_en_saquitos,mandarina
    # example of df row
    # 8,2023-03-18,1027.14,198.49,349.99,201.75,229.02,223.89,355.5,1599.9,1049.9,429.9,1499.9,999.9,1299.9,299.9,1049.9,479.9,1690.0,1220.0,1909.0,1049.0,4263.33,574.74,277.05,242.15,1485.55,264.2,1469.0,2699.0,1592.0,236.25,736.12,1361.0,499.0,499.0,419.0,199.0,479.0,239.0,329.0,229.0,199.0,899.0,699.0,249.0,199.0,614.16,509.04,1313.15,304.22,726.0,581.26,316.3,640.49,179.6,0.0,92.52,224.67,117.5,397.0,454.0,8305.800000000001,770.85,418.56,1.0

    for product in products:
        product_name = product["format_name"]
        product_id = product["id"]
        for index, row in prices_df.iterrows():
            date = row["fecha"]
            price = row[product_name]
            cursor.execute(
                """
                INSERT INTO prices (product_id, market_id, price, date)
                VALUES (%s, %s, %s, %s)
                """,
                (product_id, market["id"], price, date)
            )

    connection.commit()

    cursor.execute(
        """
        SELECT * FROM prices
        """
    )
    prices = cursor.fetchall()
    prices_json = []
    for price in prices:
        price_dict = {
            "id": price[0],
            "product_id": price[1],
            "market_id": price[2],
            "price": price[3],
            "date": price[4]
        }
        prices_json.append(price_dict)

    return prices_json
