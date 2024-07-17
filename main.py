import datetime
import csv
from flask import Flask, request, render_template
from prettytable import PrettyTable
from colorama import init, Fore, Style

app = Flask(__name__)
init(autoreset=True)  # Inicializa colorama para que los colores se reseteen automáticamente

@app.route('/datos_sensor/', methods=['POST'])
def datos_sensor():
    if request.method == 'POST':
        data = request.json
        print(data)

        if 'temperatura_dht22' not in data or 'humedad_dht22' not in data or 'temperatura_dht11' not in data or 'humedad_dht11' not in data:
            return 'Datos incompletos', 400  # Bad Request

        fecha_hora_actual = datetime.datetime.now()
        fecha_hora_formateada = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")

        temperatura_dht22 = data['temperatura_dht22']
        humedad_dht22 = data['humedad_dht22']
        temperatura_dht11 = data['temperatura_dht11']
        humedad_dht11 = data['humedad_dht11']

        # Crear tablas PrettyTable para mostrar los datos
        table = PrettyTable()
        table.field_names = [Fore.BLUE + 'Sensor', Fore.BLUE + 'Temperatura (°C)', Fore.BLUE + 'Humedad (%)' + Style.RESET_ALL]
        table.add_row(['Exterior', f'{Fore.GREEN}{temperatura_dht22:.1f}', f'{Fore.GREEN}{humedad_dht22:.1f}' + Style.RESET_ALL])
        table.add_row(['Interior', f'{Fore.CYAN}{temperatura_dht11:.1f}', f'{Fore.CYAN}{humedad_dht11:.1f}' + Style.RESET_ALL])

        # Mostrar la tabla en la consola
        print(table)

        # Guardar los datos en archivos CSV separados
        with open('data/datos_sensor_dht22.csv', 'a', newline='') as csvfile_dht22:
            fieldnames_dht22 = ['Sensor', 'Temperatura (°C)', 'Humedad (%)', 'Fecha']
            writer_dht22 = csv.DictWriter(csvfile_dht22, fieldnames=fieldnames_dht22)

            if csvfile_dht22.tell() == 0:
                writer_dht22.writeheader()

            writer_dht22.writerow({
                'Sensor': 'Exterior',
                'Temperatura (°C)': temperatura_dht22,
                'Humedad (%)': humedad_dht22,
                'Fecha': fecha_hora_formateada
            })

        with open('data/datos_sensor_dht11.csv', 'a', newline='') as csvfile_dht11:
            fieldnames_dht11 = ['Sensor', 'Temperatura (°C)', 'Humedad (%)', 'Fecha']
            writer_dht11 = csv.DictWriter(csvfile_dht11, fieldnames=fieldnames_dht11)

            if csvfile_dht11.tell() == 0:
                writer_dht11.writeheader()

            writer_dht11.writerow({
                'Sensor': 'Interior',
                'Temperatura (°C)': temperatura_dht11,
                'Humedad (%)': humedad_dht11,
                'Fecha': fecha_hora_formateada
            })

        return 'Datos recibidos y almacenados con éxito.'

@app.route('/')
def index():
    # Leer datos del archivo CSV
    data_dht22 = []
    data_dht11 = []

    try:
        with open('data/datos_sensor_dht22.csv', 'r') as csvfile_dht22:
            reader_dht22 = csv.DictReader(csvfile_dht22)
            for row in reader_dht22:
                data_dht22.append(row)
    except FileNotFoundError:
        pass

    try:
        with open('data/datos_sensor_dht11.csv', 'r') as csvfile_dht11:
            reader_dht11 = csv.DictReader(csvfile_dht11)
            for row in reader_dht11:
                data_dht11.append(row)
    except FileNotFoundError:
        pass

    return render_template('index.html', data_dht22=data_dht22, data_dht11=data_dht11)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
