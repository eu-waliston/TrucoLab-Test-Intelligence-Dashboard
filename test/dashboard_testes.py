import subprocess
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, PageBreak
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas


# -------------------------------------------------------------
# Helpers para caixas estilizadas
# -------------------------------------------------------------
def draw_box(ax, color="#1b2a41"):
    ax.set_facecolor(color)
    for spine in ax.spines.values():
        spine.set_visible(False)


# -------------------------------------------------------------
# RODAR PYTEST
# -------------------------------------------------------------
def run_pytest():
    print("Executando pytest...")
    subprocess.run(
        ["pytest", "--json-report", "--json-report-file=report.json", "-q"],
        capture_output=False,
        text=True
    )
    print("✔️ Testes finalizados. Processando...")


# -------------------------------------------------------------
# CARREGAR RELATÓRIO JSON
# -------------------------------------------------------------
def load_report():
    with open("report.json", "r") as f:
        return json.load(f)


# -------------------------------------------------------------
# PROCESSAMENTO DOS DADOS
# -------------------------------------------------------------
def process_data(data):
    tests = data.get("tests", [])
    summary = data.get("summary", {})
    duration = data.get("duration", 0)

    total = len(tests)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    skipped = summary.get("skipped", 0)
    avg_time = duration / total if total else 0

    tests_by_file = {}
    fails_by_file = {}
    slow_tests = []

    for t in tests:
        file = t.get("nodeid", "").split("::")[0]
        outcome = t.get("outcome")
        call = t.get("call", {})
        sec = call.get("duration", 0)

        tests_by_file[file] = tests_by_file.get(file, 0) + 1
        if outcome == "failed":
            fails_by_file[file] = fails_by_file.get(file, 0) + 1
        slow_tests.append((t["nodeid"], sec))

    slow_tests = sorted(slow_tests, key=lambda x: x[1], reverse=True)[:10]

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "duration": duration,
        "avg_time": avg_time,
        "tests_by_file": tests_by_file,
        "fails_by_file": fails_by_file,
        "slow_tests": slow_tests,
    }


# -------------------------------------------------------------
# GERAR O DASHBOARD PRINCIPAL
# -------------------------------------------------------------
def generate_dashboard_image(info):
    fig = plt.figure(figsize=(15, 11))
    fig.patch.set_facecolor("#0e1726")

    gs = GridSpec(4, 3, figure=fig, wspace=0.6, hspace=1.2)
    font = "white"

    fig.suptitle("✨ Dashboard de Testes — Visão Completa ✨",
                 color="white", fontsize=25, fontweight="bold", y=0.96)

    # Pizza
    ax1 = fig.add_subplot(gs[0, 0])
    draw_box(ax1)
    ax1.pie(
        [info["passed"], info["failed"], info["skipped"]],
        labels=["✔️ Passaram", "❌ Falharam", "➡️ Ignorados"],
        autopct="%1.1f%%",
        textprops={"color": "white"}
    )
    ax1.set_title("Status Geral", color=font, fontsize=14)

    # Testes por arquivo
    ax2 = fig.add_subplot(gs[0, 1])
    draw_box(ax2)
    ax2.barh(list(info["tests_by_file"].keys()),
             list(info["tests_by_file"].values()), color="#4e89ff")
    ax2.set_title("📁 Testes por Arquivo", color=font)
    ax2.tick_params(colors=font)

    # Falhas
    ax3 = fig.add_subplot(gs[0, 2])
    draw_box(ax3)
    if info["fails_by_file"]:
        ax3.bar(info["fails_by_file"].keys(),
                info["fails_by_file"].values(), color="#ff6961")
    ax3.set_title("⚠️ Falhas por Arquivo", color=font)
    ax3.tick_params(colors=font, rotation=45)

    # Indicadores
    ax4 = fig.add_subplot(gs[1, :])
    draw_box(ax4)
    txt = (
        f"📌 Total de testes: {info['total']}\n"
        f"⏱️ Tempo total: {info['duration']:.2f}s\n"
        f"⚡ Média por teste: {info['avg_time']:.4f}s\n"
        f"✔️ Sucessos: {info['passed']} — ❌ Falhas: {info['failed']} — ➡️ Ignorados: {info['skipped']}"
    )
    ax4.text(0.02, 0.5, txt, color=font, fontsize=15, va="center")
    ax4.set_title("📊 Indicadores", color=font)

    # Histórico simbólico
    ax5 = fig.add_subplot(gs[2, :])
    draw_box(ax5)
    fake = [info["passed"], info["passed"] - 1,
            info["passed"] + 2, info["passed"]]
    ax5.plot(fake, marker="o", linewidth=2)
    ax5.set_title("📈 Histórico Simbólico", color=font)
    ax5.tick_params(colors=font)

    # Lentos
    ax6 = fig.add_subplot(gs[3, :])
    draw_box(ax6)
    txt2 = "🐌 Top 10 Testes Mais Lentos\n\n"
    for name, sec in info["slow_tests"]:
        txt2 += f"• {name} — {sec:.4f}s\n"
    ax6.text(0.02, 0.95, txt2, va="top", color=font)
    ax6.set_title("⏳ Testes Lentos", color=font)

    outfile = "dashboard_main.png"
    plt.savefig(outfile, facecolor=fig.get_facecolor(), dpi=170)
    plt.close()
    return outfile


# -------------------------------------------------------------
# CABEÇALHO E RODAPÉ DO PDF
# -------------------------------------------------------------
def header_footer(canvas: Canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 10)
    canvas.drawString(30, 565, "Relatório de Testes Automatizados — Projeto Truco AI")
    canvas.drawRightString(815, 565, datetime.now().strftime("%d/%m/%Y"))
    canvas.drawString(30, 20, f"Página {doc.page}")
    canvas.restoreState()


# -------------------------------------------------------------
# GERAR PDF PREMIUM
# -------------------------------------------------------------
def generate_pdf(info, dashboard_file):
    pdf = SimpleDocTemplate(
        "dashboard_testes_completo.pdf",
        pagesize=landscape(letter)
    )

    styles = getSampleStyleSheet()
    flow = []

    # CAPA
    title = Paragraph(
        "<para align='center'><font size=30>📘 Relatório de Testes Automatizados</font></para>",
        styles["Title"]
    )
    flow.append(Spacer(1, 2 * inch))
    flow.append(title)
    flow.append(Spacer(1, 1 * inch))
    flow.append(Paragraph(
        f"<para align='center'><font size=16>Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</font></para>",
        styles["Normal"]
    ))
    flow.append(PageBreak())

    # INDICADORES
    summary = f"""
    <font size=18><b>📊 Indicadores Gerais</b></font><br/><br/>
    • Total de testes: {info['total']}<br/>
    • Tempo total: {info['duration']:.2f}s<br/>
    • Média por teste: {info['avg_time']:.4f}s<br/>
    • Sucessos: {info['passed']}<br/>
    • Falhas: {info['failed']}<br/>
    • Ignorados: {info['skipped']}<br/>
    """

    flow.append(Paragraph(summary, styles["Normal"]))
    flow.append(PageBreak())

    # DASHBOARD PRINCIPAL
    flow.append(Image(dashboard_file, width=10 * inch, height=6 * inch))
    flow.append(PageBreak())

    # Testes por arquivo
    text_files = "<font size=18><b>📁 Testes por Arquivo</b></font><br/><br/>"
    for f, c in info["tests_by_file"].items():
        text_files += f"• {f} — {c} testes<br/>"
    flow.append(Paragraph(text_files, styles["Normal"]))
    flow.append(PageBreak())

    # Testes lentos
    text_slow = "<font size=18><b>🐌 Testes Mais Lentos</b></font><br/><br/>"
    for name, sec in info["slow_tests"]:
        text_slow += f"• {name} — {sec:.4f}s<br/>"
    flow.append(Paragraph(text_slow, styles["Normal"]))

    pdf.build(flow, onFirstPage=header_footer, onLaterPages=header_footer)

    print("📄 PDF completo salvo como: dashboard_testes_completo.pdf")


# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------
if __name__ == "__main__":
    run_pytest()
    data = load_report()
    info = process_data(data)
    dash = generate_dashboard_image(info)
    generate_pdf(info, dash)
