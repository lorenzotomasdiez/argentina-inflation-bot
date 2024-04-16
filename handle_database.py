import psycopg2 # type: ignore
import pandas as pd
import os
from config import psql_host, psql_port, script_dir, tabla

global lista_larga

def cargar_ddbb_local(listado_productos):
    """
    Si la tabla no existe, créela. Si la tabla existe, verifique si la fecha ya está en la tabla. Si no
    es así, inserte los datos. Si es así, no hagas nada.

    :param listado_productos: un diccionario los productos y el precio
    """
    print(f"Listado desde cargar_ddbb_local \n{listado_productos}")
    if "null" in listado_productos.values():
        print("hay un Nan en el diccionario")
        return
    conn = psycopg2.connect(
        host=psql_host,
        port=psql_port,
        database="variation",
        user="postgres",
        password="postgres",
    )
    # Crear la tabla si no existe
    with conn.cursor() as cur:
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS precios ({', '.join([f'{columna} {tipo}' for columna, tipo in tabla.items()])})"
        )
        conn.commit()

    # Insertar los datos en la tabla
    with conn.cursor() as cur:
        columnas = []
        valores = []
        for columna, valor in listado_productos.items():
            columnas.append(columna)
            valores.append(valor)

        data_fecha = cur.execute(
            "SELECT fecha FROM precios WHERE fecha = %s", (valores[0],)
        )
        data_fecha = cur.fetchone()

        if data_fecha == None:
            print("no hay fecha")
            print("Cargando datos")
            query = f"INSERT INTO precios ({', '.join(columnas)}) VALUES ({', '.join(['%s'] * len(valores))})"
            cur.execute(query, valores)
            conn.commit()
        else:
            print("Ya se cargaron los datos de hoy")

    # Cerrar la conexión a la base de datos
    cur.close()
    conn.close()

def guardar_csv_excel():
    """
    Se conecta a una base de datos de Postgres, obtiene los datos de una tabla, crea un marco de datos,
    guarda el marco de datos como un archivo csv y excel, y luego crea un nuevo marco de datos con los
    datos en formato largo.
    """
    conn = psycopg2.connect(
        host=psql_host,
        port=psql_port,
        database="variation",
        user="postgres",
        password="postgres",
    )
    # Obtener los datos de la tabla
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM precios")
        rows = cur.fetchall()
        conn.commit()

    # si la tabla tiene nan salir
    print(f"Listado desde guardar_csv_excel \n {rows}")
    if "nan" in rows:
        print("hay un Nan en la tabla")
        return None

    # crear un dataframe si no existe o actualizarlo
    csv_dir = os.path.join(script_dir, "base", "prices.csv")
    xlsx_dir = os.path.join(script_dir, "base", "prices.xlsx")
    prices_long_list_dir = os.path.join(script_dir, "base", "prices_long_list.csv")
    try:
        df = pd.read_csv(csv_dir)

        for row in rows:
            fecha = row[1].strftime("%Y-%m-%d")

            if fecha not in df["fecha"].values:
                df = pd.concat(
                    [df, pd.DataFrame([row], columns=[desc[0] for desc in cur.description])],
                    ignore_index=True,
                )
                df["fecha"] = pd.to_datetime(df["fecha"])
                df = df.sort_values(by="fecha")

                df = df.drop_duplicates()
                df = df.reset_index(drop=True)
                print("actualizando datos")
            else:
                print("no hay datos nuevos")
                continue

    except FileNotFoundError:
        df = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
        print("creando dataframe")

    # Cerrar la conexión a la base de datos
    cur.close()
    conn.close()

    # Guardar el dataframe en un archivo csv
    df.to_csv(csv_dir, index=False)

    # guardar el dataframe en un archivo excel
    df.to_excel(xlsx_dir, index=False)

    lista_tabla = df.columns.to_list()

    lista_tabla.remove("id")
    lista_tabla.remove("fecha")

    # Crear un dataframe con los datos en formato largo
    lista_larga = df.melt(
        id_vars=["fecha"],
        value_vars=lista_tabla,
        var_name="producto",
        value_name="precio",
    )
    lista_larga.to_csv(prices_long_list_dir, index=False)
    lista_larga["fecha"] = pd.to_datetime(lista_larga["fecha"])