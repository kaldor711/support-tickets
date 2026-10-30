import sqlite3
from datetime import datetime

DB_NAME = "crm.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS prestadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT,
        activo INTEGER DEFAULT 1
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_ticket TEXT UNIQUE NOT NULL,
        beneficio TEXT NOT NULL,
        nombre_afiliado TEXT NOT NULL,
        apellido_afiliado TEXT NOT NULL,
        telefono TEXT,
        prestador_id INTEGER,
        tipo_consulta TEXT,
        estado TEXT DEFAULT 'Pendiente',
        prioridad TEXT,
        reiteraciones INTEGER DEFAULT 0,
        fecha_creacion DATETIME,
        fecha_primera_respuesta DATETIME,
        fecha_cierre DATETIME
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS mensajes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER NOT NULL,
        fecha_hora DATETIME NOT NULL,
        usuario TEXT NOT NULL,
        tipo_usuario TEXT NOT NULL,
        mensaje TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def crear_prestadores_iniciales():

    conn = get_connection()
    cur = conn.cursor()

    prestadores = [
        ("AMB Salud",),
        ("Traslados Norte",),
        ("Emerger",)
    ]

    cur.executemany(
        "INSERT OR IGNORE INTO prestadores(nombre) VALUES (?)",
        prestadores
    )

    conn.commit()
    conn.close()


def obtener_prestadores():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, nombre
        FROM prestadores
        ORDER BY nombre
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


def crear_ticket(
    beneficio,
    nombre,
    apellido,
    telefono,
    prestador_id,
    tipo_consulta,
    prioridad,
    observacion
):

    conn = get_connection()
    cur = conn.cursor()

    numero_ticket = "TR-" + datetime.now().strftime("%Y%m%d%H%M%S")

    cur.execute("""
        INSERT INTO tickets (
            numero_ticket,
            beneficio,
            nombre_afiliado,
            apellido_afiliado,
            telefono,
            prestador_id,
            tipo_consulta,
            prioridad,
            fecha_creacion
        )
        VALUES (?,?,?,?,?,?,?,?,?)
    """,
    (
        numero_ticket,
        beneficio,
        nombre,
        apellido,
        telefono,
        prestador_id,
        tipo_consulta,
        prioridad,
        datetime.now()
    ))

    ticket_id = cur.lastrowid

    cur.execute("""
        INSERT INTO mensajes (
            ticket_id,
            fecha_hora,
            usuario,
            tipo_usuario,
            mensaje
        )
        VALUES (?,?,?,?,?)
    """,
    (
        ticket_id,
        datetime.now(),
        "OPERADOR",
        "OPERADOR",
        observacion
    ))

    conn.commit()
    conn.close()

    return numero_ticket


def listar_tickets():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            numero_ticket,
            beneficio,
            nombre_afiliado,
            apellido_afiliado,
            prioridad,
            fecha_creacion
        FROM tickets
        ORDER BY id DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


def buscar_tickets(texto):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            numero_ticket,
            beneficio,
            nombre_afiliado,
            apellido_afiliado,
            prioridad,
            fecha_creacion
        FROM tickets
        WHERE
            beneficio LIKE ?
            OR apellido_afiliado LIKE ?
            OR nombre_afiliado LIKE ?
        ORDER BY id DESC
    """,
    (
        f"%{texto}%",
        f"%{texto}%",
        f"%{texto}%"
    ))

    rows = cur.fetchall()

    conn.close()

    return rows


def agregar_mensaje(
    ticket_id,
    usuario,
    tipo_usuario,
    mensaje
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO mensajes (
            ticket_id,
            fecha_hora,
            usuario,
            tipo_usuario,
            mensaje
        )
        VALUES (?,?,?,?,?)
    """,
    (
        ticket_id,
        datetime.now(),
        usuario,
        tipo_usuario,
        mensaje
    ))

    conn.commit()
    conn.close()


def obtener_mensajes(ticket_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM mensajes
        WHERE ticket_id = ?
        ORDER BY fecha_hora
    """,
    (ticket_id,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows