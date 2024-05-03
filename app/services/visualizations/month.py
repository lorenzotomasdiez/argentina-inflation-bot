import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from config import get_month_from_date

def addlabels(x, y):
  for i in range(len(x)):
    plt.text(x[i], y[i], str(big_values_format(y[i])), ha='center', va='bottom')
    
def big_values_format(v):
  if v >= 1_000_000:
    return f'{v / 1_000_000:.2f}'
  else:
    return f'{v:,.0f}'


def generate_graph_month_message(id, data, date):
  month = get_month_from_date(date)
  
  values = data[::2] if len(data) > 12 else data
  
  # Convertir los valores a flotantes y las fechas a cadenas
  for item in values:
    item["valor"] = float(item["valor"].replace(".", "").replace(".", "").replace(",", "."))
    item["fecha"] = str(item["fecha"])
    
  labels = generate_labels(id=id, month=month)
  
  
  y_values = [item["valor"] for item in values]
  x_values = [item["fecha"].split("/")[0] for item in values]
  
  print(y_values)
  
  plt.figure(figsize=(10, 5))
  plt.bar(x_values, y_values, color='#ffe5b4')
  addlabels(x_values, y_values)
  plt.xlabel("Dia del mes")
  plt.ylabel(labels[1])
  plt.title(f'{labels[0]} | x:@bot_bcra')
  plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{big_values_format(x)}')) # Formato personalizado para el eje y
  plt.ylim(min(y_values)*0.9, max(y_values)*1.1)
  plt.tight_layout()
  plt.savefig('graph_month.png', bbox_inches='tight')
  plt.close()
  
  return labels[2]

  
def generate_labels(id, month):
  title = generate_title(id, month)
  value = generate_value_label(id)
  message = generate_message(id, month)
  return [title, value, message]


def generate_title(id, month):
  if id == 1:
    return f'Reservas Internacionales del BCRA en {month}'
  elif id == 4:
    return f'Tipo de Cambio Minorista en {month}'
  elif id == 5:
    return f'Tipo de Cambio Mayorista en {month}'
  elif id == 6:
    return f'Tasa de Política Monetaria en {month}'
  elif id == 15:
    return f'Base monetaria total en {month}'
  elif id == 16:
    return f'Circulación monetaria en {month}'
  elif id == 34:
    return f'Tasa de Política Monetaria en {month}'
  else:
    raise Exception("ID NOT FOUND")
    
def generate_value_label(id):
  if id == 1:
    return 'Valor en M de USD'
  elif id in [4, 5]:
    return 'Valor en pesos'
  elif id in [15, 16]:
    return 'Valor en Billones de pesos'
  elif id == 6:
    return 'Valor en % n.a.'
  elif id == 34:
    return 'Valor en % e.a.'
  else:
    raise Exception("ID NOT FOUND")
  
def generate_message(id, month):
  if id == 1:
    return f"‼️ RESUMEN BCRA ‼️\nReservas Internacionales del BCRA en el mes de {month} #BCRA #ReservasInternacionales"
  elif id in [4, 5]:
    return f"‼️ RESUMEN BCRA ‼️\nTipo de Cambio en el mes de {month} #BCRA #TipoDeCambio #Dolar"
  elif id == 6:
    return f"‼️ RESUMEN BCRA ‼️\nTasa de Política Monetaria en el mes de {month} #BCRA #PolíticaMonetaria"
  elif id == 15:
    return f"‼️ RESUMEN BCRA ‼️\nBase Monetaria en el mes de {month} #BCRA #BaseMonetaria"
  elif id == 16:
    return f"‼️ RESUMEN BCRA ‼️\nCirculación Monetaria en el mes de {month} #BCRA #CirculaciónMonetaria"
  elif id == 34:
    return f"‼️ RESUMEN BCRA ‼️\nTasa de Política Monetaria en el mes de {month} #BCRA #PolíticaMonetaria"
  else:
    raise Exception("ID NOT FOUND")
