from elasticsearch import Elasticsearch
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# Configuración de Elasticsearch
es = Elasticsearch(['http://localhost:9200'])  # Reemplaza con la URL y el puerto de tu instancia de Elasticsearch
index_name = 'my-application-logs'  # Nombre del índice de logs

# Configuración del servidor de correo
smtp_host = 'smtp.sendgrid.net'  # Reemplaza con la dirección del servidor SMTP
smtp_port = 587  # Puerto del servidor SMTP
smtp_username = 'apikey'
# Reemplaza con tu dirección de correo electrónico
smtp_password = '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'  
# Reemplaza con tu contraseña de correo electrónico
from_address = 'sms.afk@gmail.com'
# Reemplaza con tu dirección de correo electrónico
to_address = 'nico50829@gmail.com'
# Reemplaza con la dirección de correo electrónico del destinatario

# Término de búsqueda en Elasticsearch
search_term = 'No encontrado'  # Término de búsqueda para encontrar los logs específicos
start_time = datetime.now() - timedelta(hours=60)  # Hora de inicio (1 hora atrás)
end_time = datetime.now()  # Hora de fin (tiempo actual)
# Consulta Elasticsearch
query={
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "message": search_term
          }
        },
        {
          "range": {
            "@timestamp": {
              "gte": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
              "lte": end_time.strftime("%Y-%m-%dT%H:%M:%S")
            }
          }
        }
      ]
    }
  }
}

# Ejecutar la consulta
response = es.search(index=index_name, body=query)
print(response)
# Verificar si se encontraron logs
if response['hits']['total']['value'] > 0:
    # Preparar el mensaje de correo electrónico
    hits = response['hits']['hits']
    # Preparar el contenido del mensaje de correo
    subject = f"Notificación de log encontrado: {search_term}"
    body = f"Se encontraron logs específicos en Elasticsearch dentro del rango de tiempo especificado:\n\n"

    for hit in hits:
        log_message = hit['_source']
        body += f"- {log_message}\n"

    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = from_address
    message['To'] = to_address

    # Enviar el correo electrónico
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)
        print("Correo electrónico enviado con éxito.")
else:
    print("No se encontraron logs específicos en Elasticsearch.")
