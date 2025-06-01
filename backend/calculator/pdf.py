from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def generate_stats_pdf(filename: str, data: dict):
    color_primary = colors.Color(76 / 255, 159 / 255, 112 / 255)
    color_secondary = colors.Color(73 / 255, 111 / 255, 93 / 255)
    color_dark = colors.Color(73 / 255, 81 / 255, 111 / 255)
    color_accent = colors.Color(98 / 255, 121 / 255, 184 / 255)
    color_accent2 = colors.Color(142 / 255, 164 / 255, 210 / 255)

    doc = SimpleDocTemplate("storage/" + filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("Photovoltaic Investment Report", styles["Title"])
    date_str = Paragraph(f"Generated at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}", styles["Normal"])
    elements.append(title)
    elements.append(date_str)
    elements.append(Spacer(1, 16))

    stats = [
        ("Installation cost", f"{data['panel_installation_cost']} zł", color_primary),
        ("Buy price", f"{data['energy_price_buy_kwh']} zł/kWh", color_accent),
        ("Sell price", f"{data['energy_price_sell_kwh']} zł/kWh", color_accent2),
        ("Yearly prod.", f"{data['yearly_production_kw']} kWh", color_secondary),
        ("Self-consumption", f"{data['self_consumption']}%", color_dark),
    ]
    cards_table = Table([[s[0], s[1]] for s in stats], colWidths=[160, 120])
    cards_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), color_primary),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (0, 1), color_accent),
        ("BACKGROUND", (0, 2), (0, 2), color_accent2),
        ("BACKGROUND", (0, 3), (0, 3), color_secondary),
        ("BACKGROUND", (0, 4), (0, 4), color_dark),
        ("TEXTCOLOR", (0, 1), (1, 4), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("BOX", (0, 0), (-1, -1), 1, colors.grey),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(cards_table)
    elements.append(Spacer(1, 24))

    statistics = data["statistics"]
    if statistics:
        table_data = [["Year", "Cost w/o installation", "Profit", "Cost", "Savings", "State"]]
        for stat in statistics:
            table_data.append([
                stat["year"],
                stat["cost_without_installation"],
                stat["profit"],
                stat["cost"],
                stat["savings"],
                stat["state"]
            ])
        stats_table = Table(table_data, colWidths=[50, 85, 70, 60, 70, 60])
        stats_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), color_accent),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOX", (0, 0), (-1, -1), 1, colors.grey),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ]))
        elements.append(stats_table)

    doc.build(elements)
