import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from collections import defaultdict

def addlabels(x, y):
  for i in range(len(x)):
    plt.text(x[i], y[i], str(big_values_format(y[i])), ha='center', va='bottom')
    
def big_values_format(v):
  if v >= 1_000_000:
    return f'{v / 1_000_000:.2f}'
  else:
    return f'{v:,.0f}'


def generate_graph_government(id, data):
  monthly_values = defaultdict(float)
  for item in data:
    fecha = item["fecha"]
    valor = float(item["valor"].replace(".", "").replace(".", "").replace(",", "."))
    year_month = fecha[3:]
    if year_month == "12/2023":
      if monthly_values[year_month] == 0 or valor > monthly_values[year_month]:
          monthly_values[year_month] = valor
    else:  
      if monthly_values[year_month] == 0 or valor < monthly_values[year_month]:
        monthly_values[year_month] = valor
  
  x_values = list(monthly_values.keys())
  y_values = list(monthly_values.values())
  
  last_date = x_values[-1]
  
  labels = generate_labels(id=id, last_date=last_date)
  
  plt.figure(figsize=(10, 5))
  plt.bar(x_values, y_values, color='#ffe5b4')
  addlabels(x_values, y_values)
  plt.xlabel("Mes / Año")
  plt.ylabel(labels[1])
  plt.title(f'{labels[0]} | x:@bot_bcra')
  plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{big_values_format(x)}')) # Formato personalizado para el eje y
  plt.tight_layout()
  plt.savefig('graph_government.png', bbox_inches='tight')
  plt.close()
  
  return labels[2]

  
def generate_labels(id, last_date):
  title = generate_title(id=id, last_date=last_date)
  value = generate_value_label(id=id)
  message = generate_message(id=id, last_date=last_date)
  return [title, value, message]


def generate_title(id, last_date):
  if id == 1:
    return f'Reservas Internacionales del BCRA desde 11/12/23 al {last_date}'
  elif id == 4:
    return f'Tipo de Cambio Oficial Minorista  desde 11/12/23 al {last_date}'
  elif id == 5:
    return f'Tipo de Cambio Oficial Mayorista desde 11/12/23 al {last_date}'
  elif id == 6:
    return f'Tasa de Política Monetaria Nominal Anual desde 11/12/23 al {last_date}'
  elif id == 15:
    return f'Base monetaria total desde 11/12/23 al {last_date}'
  elif id == 16:
    return f'Circulación monetaria desde 11/12/23 al {last_date}'
  elif id == 34:
    return f'Tasa de Política Monetaria Efectiva Anual desde 11/12/23 al {last_date}'
  else:
    raise Exception("ID NOT FOUND", id)
    
def generate_value_label(id):
  if id == 1:
    return 'Valor en M de $USD'
  elif id in [4, 5]:
    return 'Valor en $ARS'
  elif id in [15, 16]:
    return 'Valor en Billones de $ARS'
  elif id == 6:
    return 'Valor % '
  elif id == 34:
    return 'Valor %'
  else:
    raise Exception("ID NOT FOUND", id)
  
def generate_message(id, last_date):
  if id == 1:
    return f"‼️ RESUMEN BCRA ‼️\nReservas Internacionales del BCRA desde 11/12/2023 al {last_date} #BCRA #ReservasInternacionales"
  elif id == 4:
    return f"‼️ RESUMEN BCRA ‼️\nTipo de Cambio Oficial Minorista desde 11/12/2023 al {last_date} #BCRA #TipoDeCambio #Dolar"
  elif id == 5:
    return f"‼️ RESUMEN BCRA ‼️\nTipo de Cambio Oficial Mayorista desde 11/12/2023 al {last_date} #BCRA #TipoDeCambio #Dolar"
  elif id == 6:
    return f"‼️ RESUMEN BCRA ‼️\nTasa de Política Monetaria desde 11/12/2023 al {last_date} #BCRA #PolíticaMonetaria"
  elif id == 15:
    return f"‼️ RESUMEN BCRA ‼️\nBase Monetaria desde 11/12/2023 al {last_date} #BCRA #BaseMonetaria"
  elif id == 16:
    return f"‼️ RESUMEN BCRA ‼️\nCirculación Monetaria desde 11/12/2023 al {last_date} #BCRA #CirculaciónMonetaria"
  elif id == 34:
    return f"‼️ RESUMEN BCRA ‼️\nTasa de Política Monetaria desde 11/12/2023 al {last_date} #BCRA #PolíticaMonetaria"
  else:
    raise Exception("ID NOT FOUND", id)
