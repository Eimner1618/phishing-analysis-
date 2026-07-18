# Generador de Reporte Formal de Phishing
# Autor: Diego Armando Álvarez Valero
# Formato: SOC / ISO 27035

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from datetime import datetime

# ========== DATOS DEL INCIDENTE ==========
incidente = {
    "id": "INC-2026-001",
    "fecha_reporte": "2026-06-06",
    "fecha_deteccion": "2026-06-06 10:00:00",
    "clasificacion": "Phishing — Suplantación de identidad bancaria",
    "severidad": "ALTA",
    "estado": "Cerrado",
    "analista": "Diego Armando Álvarez Valero",
    "hash_correo": "a3f5c2d1e4b6789012345678901234567890abcd",
}

hallazgos = {
    "remitente": "seguridad@banamex-alertas.com",
    "dominio_falso": "banamex-alertas.com",
    "dominio_legitimo": "banamex.com",
    "enlace": "http://banamex-verificacion.xyz/seguridad/cuenta",
    "reply_to": "recoleccion@gmail.com",
    "spf": "fail",
    "dkim": "none",
    "dmarc": "fail",
    "ip_origen": "45.33.32.156",
    "mailer": "PHPMailer 6.0",
}

iocs = [
    ("Dominio remitente", "banamex-alertas.com"),
    ("Dominio enlace", "banamex-verificacion.xyz"),
    ("IP origen", "45.33.32.156"),
    ("Reply-To", "recoleccion@gmail.com"),
]

tecnicas = [
    ("Suplantación de dominio", "T1566.002 — MITRE ATT&CK"),
    ("Urgencia artificial", "Ingeniería social — presión temporal"),
    ("Enlace malicioso HTTP", "Sin cifrado, dominio diferente al remitente"),
    ("Reply-To hijacking", "Redirección de respuestas a cuenta no corporativa"),
]

# ========== GENERADOR DE PDF ==========
OUTPUT = "Reporte_Phishing_INC-2026-001.pdf"
doc = SimpleDocTemplate(OUTPUT, pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm)

styles = getSampleStyleSheet()
elements = []

# Colores
AZUL = colors.HexColor("#1A56A0")
ROJO = colors.HexColor("#C0392B")
GRIS = colors.HexColor("#555555")
GRIS_CLARO = colors.HexColor("#F5F5F5")

# Estilos
titulo_style = ParagraphStyle("titulo", fontSize=18, textColor=AZUL, 
    spaceAfter=6, fontName="Helvetica-Bold", alignment=TA_CENTER)
subtitulo_style = ParagraphStyle("subtitulo", fontSize=10, textColor=GRIS,
    spaceAfter=12, alignment=TA_CENTER)
header_style = ParagraphStyle("header", fontSize=12, textColor=AZUL,
    spaceBefore=16, spaceAfter=6, fontName="Helvetica-Bold")
body_style = ParagraphStyle("body", fontSize=9, textColor=colors.black,
    spaceAfter=4, leading=14)
alerta_style = ParagraphStyle("alerta", fontSize=10, textColor=ROJO,
    fontName="Helvetica-Bold", spaceAfter=4)

# ===== ENCABEZADO =====
elements.append(Paragraph("REPORTE DE INCIDENTE DE SEGURIDAD", titulo_style))
elements.append(Paragraph("Análisis de Phishing — Formato SOC", subtitulo_style))
elements.append(HRFlowable(width="100%", thickness=2, color=AZUL))
elements.append(Spacer(1, 0.4*cm))

# ===== DATOS DEL INCIDENTE =====
elements.append(Paragraph("1. DATOS DEL INCIDENTE", header_style))
datos_tabla = [
    ["ID de Incidente", incidente["id"]],
    ["Fecha de Detección", incidente["fecha_deteccion"]],
    ["Fecha de Reporte", incidente["fecha_reporte"]],
    ["Clasificación", incidente["clasificacion"]],
    ["Severidad", incidente["severidad"]],
    ["Estado", incidente["estado"]],
    ["Analista", incidente["analista"]],
    ["Hash del correo (SHA256)", incidente["hash_correo"]],
]
t = Table(datos_tabla, colWidths=[5*cm, 12*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,-1), GRIS_CLARO),
    ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#DDDDDD")),
    ("PADDING", (0,0), (-1,-1), 6),
    ("TEXTCOLOR", (1,3), (1,3), ROJO),
    ("FONTNAME", (1,3), (1,3), "Helvetica-Bold"),
]))
elements.append(t)

# ===== HALLAZGOS TÉCNICOS =====
elements.append(Paragraph("2. HALLAZGOS TÉCNICOS", header_style))
hallazgos_tabla = [
    ["Campo", "Valor", "Estado"],
    ["Remitente", hallazgos["remitente"], "❌ Falso"],
    ["Dominio legítimo", hallazgos["dominio_legitimo"], "✓ Referencia"],
    ["Enlace malicioso", hallazgos["enlace"], "❌ HTTP / Dominio falso"],
    ["Reply-To", hallazgos["reply_to"], "❌ No corporativo"],
    ["SPF", hallazgos["spf"], "❌ Fail"],
    ["DKIM", hallazgos["dkim"], "❌ None"],
    ["DMARC", hallazgos["dmarc"], "❌ Fail"],
    ["IP Origen", hallazgos["ip_origen"], "⚠ Verificar en threat intel"],
    ["Mailer", hallazgos["mailer"], "⚠ No corporativo"],
]
t2 = Table(hallazgos_tabla, colWidths=[4*cm, 8*cm, 5*cm])
t2.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), AZUL),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#DDDDDD")),
    ("PADDING", (0,0), (-1,-1), 6),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, GRIS_CLARO]),
]))
elements.append(t2)

# ===== TÉCNICAS DE ATAQUE =====
elements.append(Paragraph("3. TÉCNICAS DE ATAQUE IDENTIFICADAS", header_style))
tecnicas_tabla = [["Técnica", "Referencia / Descripción"]] + tecnicas
t3 = Table(tecnicas_tabla, colWidths=[6*cm, 11*cm])
t3.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), AZUL),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#DDDDDD")),
    ("PADDING", (0,0), (-1,-1), 6),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, GRIS_CLARO]),
]))
elements.append(t3)

# ===== IOCs =====
elements.append(Paragraph("4. INDICADORES DE COMPROMISO (IOCs)", header_style))
iocs_tabla = [["Tipo", "Indicador"]] + iocs
t4 = Table(iocs_tabla, colWidths=[5*cm, 12*cm])
t4.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), AZUL),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#DDDDDD")),
    ("PADDING", (0,0), (-1,-1), 6),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, GRIS_CLARO]),
]))
elements.append(t4)

# ===== CONCLUSIÓN =====
elements.append(Paragraph("5. CONCLUSIÓN Y RECOMENDACIONES", header_style))
elements.append(Paragraph(
    "Correo de phishing confirmado. Se identificó suplantación de identidad bancaria "
    "con múltiples indicadores de compromiso. Los protocolos de autenticación SPF, DKIM "
    "y DMARC fallaron, confirmando que el correo no fue enviado por la entidad legítima.",
    body_style))
elements.append(Spacer(1, 0.3*cm))
elements.append(Paragraph("Acciones recomendadas:", ParagraphStyle("bold", fontSize=9, fontName="Helvetica-Bold")))
recomendaciones = [
    "1. Bloquear los dominios banamex-alertas.com y banamex-verificacion.xyz en el gateway de correo.",
    "2. Agregar la IP 45.33.32.156 a la lista de bloqueo del firewall.",
    "3. Reportar los IOCs a plataformas de threat intelligence (VirusTotal, AbuseIPDB).",
    "4. Notificar a usuarios finales sobre esta campaña de phishing.",
    "5. Verificar si algún usuario interactuó con el enlace malicioso.",
]
for r in recomendaciones:
    elements.append(Paragraph(r, body_style))

# ===== FIRMA =====
elements.append(Spacer(1, 0.8*cm))
elements.append(HRFlowable(width="100%", thickness=1, color=GRIS))
elements.append(Spacer(1, 0.3*cm))
elements.append(Paragraph(f"Analista: {incidente['analista']}", body_style))
elements.append(Paragraph(f"Fecha: {incidente['fecha_reporte']}", body_style))
elements.append(Paragraph("Referencia normativa: ISO/IEC 27035:2023 — Gestión de Incidentes de Seguridad", 
    ParagraphStyle("ref", fontSize=8, textColor=GRIS)))

# ===== GENERAR PDF =====
doc.build(elements)
print(f"Reporte generado: {OUTPUT}")
EOF
