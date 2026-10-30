import datetime
import random
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from db import buscar_tickets
from db import listar_tickets
from db import crear_ticket
from db import init_db
from db import crear_prestadores_iniciales
from db import obtener_prestadores

init_db()
crear_prestadores_iniciales()
prestadores = obtener_prestadores()

# Show app title and description.
st.set_page_config(page_title="CND ", page_icon="🎫")
st.title("🎫 CMC Gestión de Traslados")
st.write(
    """
    This app shows how you can build an internal tool in Streamlit. Here, we are 
    implementing a support ticket workflow. The user can create a ticket, edit 
    existing tickets, and view some statistics.
    """
)

# Create a random Pandas dataframe with existing tickets.
if "df" not in st.session_state:

    # Set seed for reproducibility.
    np.random.seed(42)

    # Make up some fake issue descriptions.
    issue_descriptions = [
        "Network connectivity issues in the office",
        "Software application crashing on startup",
        "Printer not responding to print commands",
        "Email server downtime",
        "Data backup failure",
        "Login authentication problems",
        "Website performance degradation",
        "Security vulnerability identified",
        "Hardware malfunction in the server room",
        "Employee unable to access shared files",
        "Database connection failure",
        "Mobile application not syncing data",
        "VoIP phone system issues",
        "VPN connection problems for remote employees",
        "System updates causing compatibility issues",
        "File server running out of storage space",
        "Intrusion detection system alerts",
        "Inventory management system errors",
        "Customer data not loading in CRM",
        "Collaboration tool not sending notifications",
    ]

    # Generate the dataframe with 100 rows/tickets.
    data = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "Issue": np.random.choice(issue_descriptions, size=100),
        "Status": np.random.choice(["Open", "In Progress", "Closed"], size=100),
        "Priority": np.random.choice(["High", "Medium", "Low"], size=100),
        "Date Submitted": [
            datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
    }
    df = pd.DataFrame(data)



# Show a section to add a new ticket.
st.header("Crear Caso")

# We're adding tickets via an `st.form` and some input widgets. If widgets are used
# in a form, the app will only rerun once the submit button is pressed.
with st.form("add_ticket_form"):

    beneficio = st.text_input("Beneficio")

    nombre = st.text_input("Nombre")

    apellido = st.text_input("Apellido")

    telefono = st.text_input("Telefono")

    prestador = st.selectbox(
        "Prestador",
        [p["nombre"] for p in prestadores]
    )

    tipo = st.selectbox(
        "Tipo de gestion",
        [
            "Demora",
            "Consulta",
            "Reclamo",
            "Movil no asignado",
            "Ausencia de movil"
        ]
    )

    observacion = st.text_area("Observaciones")

    prioridad = st.selectbox(
        "Prioridad",
        ["Alta", "Media", "Baja"]
    )

    submitted = st.form_submit_button("Crear Caso")
if submitted:

    numero_ticket = crear_ticket(
        beneficio,
        nombre,
        apellido,
        telefono,
        1,
        tipo,
        prioridad,
        observacion
    )

    st.success(
        f"Ticket {numero_ticket} creado correctamente"
    )

    st.write("### Datos cargados")

    st.write(f"**Beneficio:** {beneficio}")
    st.write(f"**Nombre:** {nombre}")
    st.write(f"**Apellido:** {apellido}")
    st.write(f"**Prestador:** {prestador}")
    st.write(f"**Tipo:** {tipo}")
    st.write(f"**Prioridad:** {prioridad}")
    st.write(f"**Observación:** {observacion}")
    st.divider()

    st.subheader("Gestionar Caso")

buscar = st.text_input(
    "Ingrese Beneficio o Apellido"
)

if buscar:

    tickets = buscar_tickets(buscar)

else:

    tickets = listar_tickets()

st.divider()

st.subheader("Resultados")
st.write("DEBUG")
st.write(f"Total encontrados: {len(tickets)}")

for ticket in tickets:

    st.write(
        f"{ticket['nombre_afiliado']} "
        f"{ticket['apellido_afiliado']} | "
        f"{ticket['beneficio']} | "
        f"{ticket['numero_ticket']}"
    )