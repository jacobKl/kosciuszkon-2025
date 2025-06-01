import weasyprint
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime


def generate_stats_pdf(filename: str, data: dict):
    cards = [
        {
            "title": "Koszt instalacji",
            "value": f"{data.get('panel_installation_cost', 0):,.2f} PLN"
        },
        {
            "title": "Produkcja na rok",
            "value": f"{data.get('produced_energy_per_year', 0):,.2f} kWh"
        },
        {
            "title": "Energia wysłana do sieci",
            "value": f"{data.get('energy_into_grid', 0):,.2f} kWh"
        },
        {
            "title": "Własna konsumpcja",
            "value": f"{data.get('self_consumption', 0):,.2f}%"
        }
    ]

    years = [stat["year"] for stat in data["statistics"]]
    states = [stat["state"] for stat in data["statistics"]]

    plt.figure(figsize=(6.2, 2.5), dpi=140)
    plt.plot(years, states, marker="o", color="#4c9f70", linewidth=3, label="Stan końcowy")
    plt.fill_between(years, states, color="#f3fcf7", alpha=0.22)
    plt.grid(alpha=0.22)
    plt.xlabel("Rok")
    plt.ylabel("Stan [PLN]")
    plt.title("Stan końcowy w kolejnych latach", color="#49516f", fontsize=11, fontweight="bold", pad=12)
    plt.tick_params(colors="#496f5d")
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.legend()
    plt.tight_layout(pad=1)
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", transparent=False, facecolor="white")
    plt.close()
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    img_tag = f'<img src="data:image/png;base64,{image_base64}" style="max-width: 100%; border-radius: 10px; border:1.5px solid #4c9f70; margin: 18px auto 24px; display: block; background: white;">'

    rows_html = ""
    for stat in data["statistics"]:
        rows_html += f"""
            <tr>
                <td>{stat['year']}</td>
                <td>{stat['cost_without_installation']:.2f} PLN</td>
                <td>{stat['profit']:.2f} PLN</td>
                <td>{stat['cost']:.2f} PLN</td>
                <td>{stat['savings']:.2f} PLN</td>
            </tr>
        """

    html = f"""
        <html lang="pl">
        <head>
          <meta charset="UTF-8">
          <title>Rezultat</title>
          <style>
            :root {{
              --color-primary: #4c9f70;
              --color-secondary: #496f5d;
              --color-dark: #49516f;
              --color-accent: #6279b8;
              --color-accent-2: #8ea4d2;
            }}
            body {{
              font-family: 'Segoe UI', Arial, sans-serif;
              margin: 0;
              padding: 0;
            }}
            .container {{
              max-width: 900px;
              margin: 28px auto;
              background: #fff;
              border-radius: 18px;
              box-shadow: 0 6px 30px rgba(76,159,112,0.07);
              overflow: hidden;
              border: 2px solid var(--color-primary);
              padding-bottom: 30px;
            }}
            .header {{
              background: linear-gradient(90deg, var(--color-primary) 70%, var(--color-primary));
              color: #fff;
              padding: 32px 40px 26px 40px;
              border-bottom: 3px solid white;
            }}
            .header h1 {{
              font-size: 2.2rem;
              margin: 0 0 8px 0;
              letter-spacing: 1px;
              font-weight: 700;
            }}
            .header p {{
              margin: 0;
              font-size: 1.15rem;
              opacity: 0.92;
              font-weight: 400;
            }}
            .card-grid {{
              display: flex;
              gap: 24px;
              padding: 32px 40px 16px 40px;
              flex-wrap: wrap;
            }}
            .card {{
              flex: 0 1 calc(50% - 12px);
              background: var(--color-primary);
              border-radius: 12px;
              padding: 22px 18px 14px 22px;
              display: flex;
              flex-direction: column;
              align-items: flex-start;
              border-left: 6px solid var(--color-secondary);
              box-shadow: 0 2px 8px rgba(76,159,112,0.06);
              min-width: 0;
            }}
            .card-title {{
              font-size: 1.02rem;
              color: #fff;
              margin-bottom: 6px;
              font-weight: 600;
              letter-spacing: 0.2px;
            }}
            .card-value {{
              font-size: 1.4rem;
              color: #fff;
              font-weight: bold;
              letter-spacing: 0.5px;
            }}
            .dashboard-section {{
              margin: 0 40px 20px 40px;
              background: #f3fcf7;
              border-radius: 14px;
              padding: 20px 18px 14px 18px;
              border: 1px solid var(--color-primary);
            }}
            .dashboard-section h2 {{
              text-align: center;
              font-size: 1.3rem;
              font-weight: 400;
              margin: 0 0 16px 0;
              color: var(--color-secondary);
              letter-spacing: 0.4px;
            }}
            table {{
              width: 100%;
              border-collapse: collapse;
              font-size: 1.01rem;
              background: #fff;
              border-radius: 12px;
              overflow: hidden;
            }}
            thead {{
              background: var(--color-primary);
              color: #fff;
              font-weight: bold;
            }}
            th, td {{
              padding: 10px 8px;
              text-align: center;
              border-bottom: 1px solid #e6e6e6;
            }}
            th {{
              text-transform: uppercase;
              font-size: 0.97rem;
              letter-spacing: 0.3px;
              border-bottom: 2px solid var(--color-primary);
            }}
            tr:last-child td {{
              border-bottom: none;
            }} 
            .footer {{
              text-align: right;
              padding: 18px 40px 24px 40px;
              color: var(--color-secondary);
              font-size: 0.98rem;
              background: #f3fcf7;
              border-top: 2px solid var(--color-primary);
              margin-top: 30px;
            }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <h1>Rezultat</h1>
              <p>Raport na podstawie danych z dnia {datetime.now().strftime("%d.%m.%Y")}</p>
            </div>
        
            <div class="card-grid">
              {''.join([f'''
                <div class="card">
                  <div class="card-title">{card["title"]}</div>
                  <div class="card-value">{card["value"]}</div>
                </div>
              ''' for card in cards])}
            </div>
        
            <div class="dashboard-section">
              <h2>Statystyki (tabela)</h2>
              <table>
                <thead>
                  <tr>
                    <th>Rok</th>
                    <th>Koszt bez instalacji</th>
                    <th>Zysk</th>
                    <th>Koszt</th>
                    <th>Oszczędności</th>
                  </tr>
                </thead>
                <tbody>
                  {rows_html}
                </tbody>
              </table>
            </div>
        
            <div class="dashboard-section">
              <h2>Zwrot kosztów inwestycji</h2>
              {img_tag}
            </div>
        
            <div class="footer">
              &copy; {data.get('footer', 'GreenHouse')}
            </div>
          </div>
        </body>
        </html>
    """

    weasyprint.HTML(string=html).write_pdf("storage/" + filename)
