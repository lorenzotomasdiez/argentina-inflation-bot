def generate_messages(variables):
  reservas_internacionales = next((item for item in variables if item["idVariable"] == 1), None)
  res_int_message = generate_res_int_message(reservas_internacionales) if reservas_internacionales else None
  
  cambio_minorista = next((item for item in variables if item["idVariable"] == 4), None)
  cambio_minorista_message = generate_cambio_minorista_message(cambio_minorista) if cambio_minorista else None
  
  cambio_mayorista = next((item for item in variables if item["idVariable"] == 5), None)
  cambio_mayorista_message = generate_cambio_mayorista_message(cambio_mayorista) if cambio_mayorista else None
  
  tasa_politica_monetaria_percentage_na = next((item for item in variables if item["idVariable"] == 6), None)
  tasa_politica_monetaria_percentage_na_message = generate_tasa_politica_monetaria_percentage_na_message(tasa_politica_monetaria_percentage_na) if tasa_politica_monetaria_percentage_na else None
  
  base_monetaria = next((item for item in variables if item["idVariable"] == 15), None)
  base_monetaria_message = generate_base_monetaria_message(base_monetaria) if base_monetaria else None
  
  circulante_monetario = next((item for item in variables if item["idVariable"] == 16), None)
  circulante_monetario_message = generate_circulante_monetario_message(circulante_monetario) if circulante_monetario else None
  
  tasa_politica_monetaria_ea = next((item for item in variables if item["idVariable"] == 34), None)
  tasa_politica_monetaria_ea_message = generate_tasa_politica_monetaria_ea_message(tasa_politica_monetaria_ea) if tasa_politica_monetaria_ea else None
    
  return [res_int_message, cambio_minorista_message, cambio_mayorista_message, tasa_politica_monetaria_percentage_na_message, base_monetaria_message, circulante_monetario_message, tasa_politica_monetaria_ea_message]

def generate_res_int_message(variable):
  """
    return: 📈 Reservas Internacionales del BCRA al 24/04/2024: $30.023 millones de dólares. #BCRA #ReservasInternacionales
  """
  id = variable["idVariable"]
  value = variable["valor"]
  date = variable["fecha"]
  message = f"📈 Reservas Internacionales del BCRA al {date}: ${value} millones de dólares. #BCRA #ReservasInternacionales"
  return [id, message]

def generate_cambio_minorista_message(variable):
  """
    return: 💵 Tipo de Cambio Minorista al 26/04/2024: $918,36 por USD. #BCRA #TipoDeCambio #Dolar
  """
  id = variable["idVariable"]
  value = variable["valor"]
  date = variable["fecha"]
  message = f"💵 Tipo de Cambio Minorista al {date}: ${value} por USD. #BCRA #TipoDeCambio #Dolar"
  return [id, message]
  

def generate_cambio_mayorista_message(variable):
  """
    return: 💵 Tipo de Cambio Mayorista al 26/04/2024: $918,36 por USD. #BCRA #TipoDeCambio #Dolar
  """
  id = variable["idVariable"]
  value = variable["valor"]
  date = variable["fecha"]
  message = f"💵 Tipo de Cambio Mayorista al {date}: ${value} por USD. #BCRA #TipoDeCambio #Dolar"
  return [id, message]

def generate_tasa_politica_monetaria_percentage_na_message(variable):
  """
    return: 📊 Tasa de Política Monetaria al 26/04/2024: 60,00%(Nominal anual). #BCRA #PolíticaMonetaria
  """
  id = variable["idVariable"]
  value = variable["valor"]
  date = variable["fecha"]
  message = f"📊 Tasa de Política Monetaria al {date}: {value}%(Nominal anual). #BCRA #PolíticaMonetaria"
  return [id, message]


def generate_base_monetaria_message(variable):
  """
    📊 Base Monetaria al 24/04/2024: $13.344.121 millones de pesos. #BCRA #BaseMonetaria
  """
  id = variable["idVariable"]
  value = variable["valor"]
  date = variable["fecha"]
  message = f"📊 Base Monetaria al {date}: ${value} millones de pesos. #BCRA #BaseMonetaria"
  return [id, message]

def generate_circulante_monetario_message(variable):
  """
    return: 📊 Circulación Monetaria al 24/04/2024: $8.561.894 millones de pesos. #BCRA #CirculaciónMonetaria
  """
  id = variable["idVariable"]
  value = variable["valor"]
  date = variable["fecha"]
  message = f"📊 Circulación Monetaria al {date}: ${value} millones de pesos. #BCRA #CirculaciónMonetaria"
  return [id, message]


def generate_tasa_politica_monetaria_ea_message(variable):
  """
    return: 📊 Tasa de Política Monetaria al 26/04/2024: 82,12% (Efectiva anual). #BCRA #PolíticaMonetaria
  """
  id = variable["idVariable"]
  value = variable["valor"]
  date = variable["fecha"]
  message = f"📊 Tasa de Política Monetaria al {date}: {value}% (Efectiva anual). #BCRA #PolíticaMonetaria"
  return [id, message]