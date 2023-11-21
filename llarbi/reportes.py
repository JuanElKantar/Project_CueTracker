from flask import Blueprint,send_file
from database import get_data_from_database
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from flask import Blueprint
import os  

reportes_bp = Blueprint('reportes', __name__)

# Función para generar el informe PDF
def generate_pdf(filename, data):
    try:
        # Construir la ruta completa para guardar el archivo PDF
        pdf_path = os.path.join(os.path.expanduser("~"), "Desktop", "15 de septiembre 2023 V14.0","pdf", filename)

        # Crear un objeto PDF
        doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter))

        # Crear una tabla con los datos
        table_data = data
        table = Table(table_data)

        # Estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)

        # Agregar la tabla al objeto PDF
        elements = [table]
        doc.build(elements)

        return pdf_path  # Devuelve la ruta completa al archivo PDF generado
    except Exception as e:
        print("Error al generar el informe PDF:", e)
        return None

# Ruta para descargar el informe de la tabla 'partida' en formato PDF
@reportes_bp.route('/download_report', methods=['GET'])
def download_report():
    # Obtener los datos de la tabla 'partida' (debes implementar esta función)
    data = get_data_from_database('partida')  # Reemplaza 'partida' con el nombre de tu tabla

    # Generar el informe en formato PDF
    report_filename = 'informe_partida.pdf'
    pdf_path = generate_pdf(report_filename, data)
    
    if pdf_path:
        # Enviar el archivo PDF como respuesta para su descarga
        return send_file(pdf_path, as_attachment=True)
    else:
        return "Error al generar el informe PDF."
