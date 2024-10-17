from . import db

class Invoices(db.Model):
    __tablename__ = 'facturas'

    id = db.Column(db.Integer, primary_key=True)
    nom_empresa = db.Column(db.String(20))
    cod_gen = db.Column(db.String(36))
    tipo_dte = db.Column(db.String(2))
    estado_doc = db.Column(db.String(30), nullable=True)
    estado_doc_inc = db.Column(db.String(10), nullable=True)
    sello_recepcion = db.Column(db.String(40), nullable=True)
    num_iden_recep = db.Column(db.String(20), nullable=True)
    accion = db.Column(db.String(10), nullable=True)
    observaciones = db.Column(db.String(300), nullable=True)
    num_control = db.Column(db.String(31))
    nit_emisor = db.Column(db.String(14))
    nrc_emisor = db.Column(db.String(14))
    nom_emisor = db.Column(db.String(300))
    nom_receptor = db.Column(db.String(300))
    nrc_receptor = db.Column(db.String(14))
    nit_receptor = db.Column(db.String(14))
    dte = db.Column(db.Text)
    fecha_emision = db.Column(db.Date)
    procesada = db.Column(db.String(1), default='0')
    estado = db.Column(db.String(1), default='A')
    monto = db.Column(db.Numeric(10, 2), nullable=True)

    # Nuevos campos agregados
    subtotal = db.Column(db.Numeric(10, 2), nullable=True)
    iva = db.Column(db.Numeric(10, 2), nullable=True)

    def __repr__(self):
        return f'<RecepcionFacturas {self.cod_gen}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nom_empresa': self.nom_empresa,
            'cod_gen': self.cod_gen,
            'tipo_dte': self.tipo_dte,
            'estado_doc': self.estado_doc,
            'estado_doc_inc': self.estado_doc_inc,
            'sello_recepcion': self.sello_recepcion,
            'num_iden_recep': self.num_iden_recep,
            'accion': self.accion,
            'observaciones': self.observaciones,
            'num_control': self.num_control,
            'nit_emisor': self.nit_emisor,
            'nrc_emisor': self.nrc_emisor,
            'nom_emisor': self.nom_emisor,
            'nom_receptor': self.nom_receptor,
            'nrc_receptor': self.nrc_receptor,
            'nit_receptor': self.nit_receptor,
            'dte': self.dte,
            'fecha_emision': self.fecha_emision.strftime('%Y-%m-%d') if self.fecha_emision else None,
            'procesada': self.procesada,
            'estado': self.estado,
            'monto': str(self.monto) if self.monto else None,
            'subtotal': str(self.subtotal) if self.subtotal else None,  
            'iva': str(self.iva) if self.iva else None 
        }
