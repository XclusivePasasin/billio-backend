from flask import Blueprint, request, jsonify, send_file
from ..models.invoice_model import Invoices, db
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
import io
import json
from flask_paginate import Pagination, get_page_parameter
from io import BytesIO
import os

facturas_bp = Blueprint('facturas_bp', __name__)

# Ruta para monitor de facturas
@facturas_bp.route('/monitor-facturas', methods=['GET'])
def monitor_facturas():
    try:
        # Procesar los parámetros de la solicitud
        nombreEmpresa = request.args.get('nombreEmpresa', '')
        search_query = request.args.get('query', '')
        fecha_inicio_str = request.args.get('startDate', '')
        fecha_fin_str = request.args.get('endDate', '')
        emisor = request.args.get('nit', '')  # 'emisor' corresponde a 'nit'
        tipo_dte = request.args.get('tipoDte', '')
        estado_facturas = request.args.get('estado', '')

        # Filtros avanzados
        nrcEmisor = request.args.get('nrcEmisor', '')
        nitEmisor = request.args.get('nitEmisor', '')
        numeroControl = request.args.get('numeroControl', '')
        codigoGeneracion = request.args.get('codigoGeneracion', '')
        selloRecepcion = request.args.get('selloRecepcion', '')
        tipoDocumento = request.args.get('tipoDte', '')  # Asumiendo que 'tipoDocumento' se mapea a 'tipoDte'

        # Crear consulta base
        query = Invoices.query

        # Aplicar filtros dinámicamente
        if nombreEmpresa:
            query = query.filter(func.upper(Invoices.nom_emisor).like(f"%{nombreEmpresa.upper()}%"))

        if emisor:
            query = query.filter(Invoices.nit_emisor.like(f"%{emisor}%"))

        if tipo_dte:
            query = query.filter(Invoices.tipo_dte.like(f"%{tipo_dte}%"))

        if estado_facturas:
            query = query.filter(Invoices.procesada == estado_facturas)

        # Aplicar filtros avanzados
        if nrcEmisor:
            query = query.filter(Invoices.nrc_emisor.like(f"%{nrcEmisor}%"))

        if nitEmisor:
            query = query.filter(Invoices.nit_emisor.like(f"%{nitEmisor}%"))

        if numeroControl:
            query = query.filter(Invoices.num_control.like(f"%{numeroControl}%"))

        if codigoGeneracion:
            query = query.filter(Invoices.cod_gen.like(f"%{codigoGeneracion}%"))

        if selloRecepcion:
            query = query.filter(Invoices.sello_recepcion.like(f"%{selloRecepcion}%"))

        if tipoDocumento:
            query = query.filter(Invoices.tipo_dte.like(f"%{tipoDocumento}%"))

        if search_query:
            search_term = f"%{search_query}%"
            query = query.filter(or_(
                Invoices.nom_empresa.like(search_term),
                Invoices.cod_gen.like(search_term),
                Invoices.num_control.like(search_term),
                Invoices.nit_emisor.like(search_term),
                Invoices.nrc_emisor.like(search_term),
                Invoices.nom_emisor.like(search_term),
                Invoices.nom_receptor.like(search_term)
            ))

        # Manejo de fechas
        if fecha_inicio_str:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
        else:
            fecha_inicio = None

        if fecha_fin_str:
            fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
        else:
            fecha_fin = None

        if fecha_inicio and fecha_fin:
            query = query.filter(Invoices.fecha_emision.between(fecha_inicio, fecha_fin))

        # Ordenar por fecha de emisión en orden descendente
        query = query.order_by(Invoices.fecha_emision.desc())

        # Paginación
        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = 15

        invoices_pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        # Obtén los items de la página actual
        invoices = invoices_pagination.items

        return jsonify({
            'invoices': [invoice.to_dict() for invoice in invoices],
            'pagination': {
                'page': invoices_pagination.page,
                'total': invoices_pagination.total,
                'per_page': invoices_pagination.per_page,
                'pages': invoices_pagination.pages
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ver DTE por código generado
@facturas_bp.route("/dte/<cod_gen>", methods=["GET"])
def view_dte(cod_gen):
    invoice = Invoices.query.filter_by(cod_gen=cod_gen).first()
    if invoice:
        return jsonify({"dte": invoice.dte})
    else:
        return jsonify({"error": "DTE not found"}), 404

# Descargar DTES
@facturas_bp.route('/downloads-dtes', methods=["GET"])
def download_dtes():
    fecha_inicio_str = request.args.get('startDate')
    fecha_fin_str = request.args.get('endDate')

    if not fecha_inicio_str or not fecha_fin_str:
        return jsonify({"error": "Por favor, seleccione un rango de fechas válido."}), 400

    # Convertir las fechas de string a objetos datetime.date
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
    fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()

    # Filtrar por fechas
    invoices = Invoices.query.filter(
        Invoices.fecha_emision.between(fecha_inicio, fecha_fin)
    ).all()

    if not invoices:
        return jsonify({"error": "No se encontraron DTEs para el rango de fechas seleccionados."}), 404

    # Crear un BytesIO para almacenar los archivos JSON
    memory_file = BytesIO()
    
    # Añadir los archivos JSON al BytesIO
    for invoice in invoices:
        dte_json = json.dumps(invoice.dte, ensure_ascii=False, indent=2).encode('utf-8')
        memory_file.write(dte_json + b'\n')  # Escribe cada JSON en una nueva línea

    memory_file.seek(0)  # Mover el puntero al inicio del archivo

    # Devolver los archivos JSON como un archivo de texto
    return send_file(memory_file, as_attachment=True, download_name='dtes.json', mimetype='application/json')

# Actualizar facturas (sin autenticación)
@facturas_bp.route('/actualizar-facturas', methods=['POST'])
def update_invoices():
    try:
        # Obtener la lista de IDs de facturas enviados en la solicitud
        data = request.json
        id_list = data.get('id_list', [])

        if not id_list:
            return jsonify({"error": "No se proporcionaron IDs de facturas."}), 400

        # Filtrar y actualizar las facturas no procesadas
        invoices = Invoices.query.filter(
            Invoices.id.in_(id_list),
            Invoices.procesada == '0'
        ).all()

        if not invoices:
            return jsonify({"message": "No se encontraron facturas para actualizar o ya están procesadas."}), 200

        for invoice in invoices:
            invoice.procesada = '1'

        db.session.commit()

        return jsonify({"message": "Facturas actualizadas correctamente."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Resumen de facturas (sin nitReceptor obligatorio)
@facturas_bp.route('/dte/summary', methods=['GET'])
def dte_summary():
    try:
        total_dte = Invoices.query.count()
        processed_dte = Invoices.query.filter(Invoices.procesada == 1).count()
        unprocessed_dte = total_dte - processed_dte

        return jsonify({
            'totalDTE': total_dte,
            'processedDTE': processed_dte,
            'unprocessedDTE': unprocessed_dte
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
