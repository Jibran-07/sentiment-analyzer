"""Build submission.pdf with reportlab."""
import datetime
import textwrap
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Image, Paragraph, Preformatted, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

ROOT = Path(__file__).parent
STREAMLIT_URL = "https://sentiment-analyzer0.streamlit.app/"
SPACE_URL = "https://huggingface.co/spaces/Jibran101/sentiment-analyzer"
COMMITS_URL = "https://github.com/Jibran-07/sentiment-analyzer/commits/main"
SPACE_COMMITS_URL = SPACE_URL + "/commits/main"
BUILD_ERROR = (
    "Our Playwright screenshot script worked on localhost but timed out after 180 s on the live "
    "Streamlit Cloud URL (<font face='Courier'>TimeoutError: waiting for get_by_text(\"Sentiment "
    "Analyzer\")</font>). A debug screenshot showed the app was running; Streamlit Cloud serves it "
    "inside a nested iframe (<font face='Courier'>/~/+/</font>), so selectors on the outer page "
    "found nothing. We fixed it by locating that frame (<font face='Courier'>page.frames</font>) "
    "and running all selectors against it."
)
TODAY = datetime.date.today().strftime("%d %B %Y")

ss = getSampleStyleSheet()
body = ParagraphStyle("body", parent=ss["BodyText"], fontSize=9, leading=11.5, spaceAfter=2)
h = ParagraphStyle("h", parent=ss["Heading3"], fontSize=11, spaceBefore=6, spaceAfter=3,
                   textColor=colors.HexColor("#1f3b73"))
title = ParagraphStyle("t", parent=ss["Title"], fontSize=15, spaceAfter=2)
sub = ParagraphStyle("s", parent=body, alignment=TA_CENTER, fontSize=9.5)
cap = ParagraphStyle("c", parent=body, alignment=TA_CENTER, fontSize=8.5)
code = ParagraphStyle("code", fontName="Courier", fontSize=6.6, leading=7.6,
                      backColor=colors.HexColor("#f5f5f5"), borderPadding=3)
cell = ParagraphStyle("cell", parent=body, fontSize=8.5, leading=10.5)


def show_code(path):
    src = (ROOT / path).read_text(encoding="utf-8").strip()
    src = src.encode("ascii", "backslashreplace").decode("ascii")  # emojis -> \U escapes
    lines = []
    for ln in src.splitlines():
        indent = len(ln) - len(ln.lstrip())
        lines += textwrap.wrap(ln, 125, subsequent_indent=" " * (indent + 4)) or [""]
    return Preformatted("\n".join(lines), code)


def link(u):
    return f'<link href="{u}" color="blue"><u>{u}</u></link>'


story = [
    Paragraph("Class Activity — Session 5: Sentiment Analyzer", title),
    Paragraph("<b>Muhammad Jibran Narejo</b> (B04-0923-000020) &amp; "
              "<b>Sheikh Muhammad Abdullah</b> (B04-0923-000044)", sub),
    Paragraph(f"Program: BSCS · Section: A · Foundations of Generative AI (CS4106) · "
              f"Dr. Azhar Dilshad · {TODAY}", sub),
    Spacer(1, 4),
    Paragraph("1. Live App URL", h),
    Paragraph(f"Hugging Face Space: {link(SPACE_URL)} — confirmed working (analyzed text live "
              f"on {TODAY}).", body),
    Paragraph(f"The Space is a free Static Space that embeds the Streamlit Community Cloud app "
              f"{link(STREAMLIT_URL)}, because free HF accounts can no longer create Streamlit/Docker "
              f"Spaces.", body),
    Paragraph("2. Commit-History Link", h),
    Paragraph(f"App code: {link(COMMITS_URL)}<br/>HF Space: {link(SPACE_COMMITS_URL)}", body),
    Paragraph("3. Screenshots (live app)", h),
]

shots = []
for name, label in [("positive", "Positive"), ("negative", "Negative"), ("fooled", "Fools the model")]:
    crop = ROOT / "screenshots" / f"{name}_crop.tmp"
    PILImage.open(ROOT / "screenshots" / f"{name}.png").crop((330, 100, 1070, 900)).save(crop, "PNG")
    img = Image(str(crop))
    w = 58 * mm
    img.drawHeight = img.imageHeight * w / img.imageWidth
    img.drawWidth = w
    shots.append([img, Paragraph(label, cap)])
t = Table([[s[0] for s in shots], [s[1] for s in shots]], colWidths=[61 * mm] * 3)
t.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
story += [t]

story += [
    Paragraph("4. Our Personalization", h),
    Paragraph("Beyond the starter code we added: a header with both our names and roll numbers; a "
              "sidebar <i>Try an example</i> button that cycles through campus-themed sample sentences; "
              "a session history table (via <font face='Courier'>st.session_state</font>) of the last 5 "
              "analyses; a low-confidence note below 75%; and a footer listing the model's limits "
              "(binary only, sarcasm, 512-token truncation). We also pinned the model, cached it with "
              "<font face='Courier'>@st.cache_resource</font>, and added truncation and error handling.",
              body),
    Paragraph("5. Final Code", h),
    Paragraph("<b>app.py</b>", body),
    show_code("app.py"),
    Spacer(1, 4),
    Paragraph("<b>requirements.txt</b>", body),
    show_code("requirements.txt"),
    Spacer(1, 4),
    Paragraph("<b>index.html</b> (HF Static Space wrapper)", body),
    show_code("hf-space/index.html"),
    Paragraph("6. Three Test Cases", h),
]

rows = [
    ["Input", "Output", "Correct?"],
    ["Our group presentation went smoother than any rehearsal we did.", "POSITIVE (97.43%)", "Yes"],
    ["My laptop froze twice during the online quiz.", "NEGATIVE (99.85%)", "Yes"],
    ["Great, another group project where I do all the work.", "POSITIVE (99.98%)",
     "<b>No, fooled.</b> This is sarcasm: \"Great\" is a strong positive token and the complaint "
     "(\"I do all the work\") has no explicitly negative word, so the SST-2 model scores it as "
     "praise with near-total confidence."],
]
tt = Table([[Paragraph(c, cell) for c in r] for r in rows], colWidths=[72 * mm, 32 * mm, 76 * mm])
tt.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf7")),
    ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#fdecea")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
]))
story += [tt, Spacer(1, 2),
          Paragraph("All scores come from real runs (see test_results.txt in the repo). Other finding: "
                    "\"The new library timings made exam week so much easier.\" was labelled NEGATIVE "
                    "(98.18%), likely because \"exam week\" dominates.", body)]

story += [
    Paragraph("7. Reflection", h),
    Paragraph(f"<b>Error we hit:</b> {BUILD_ERROR}",
              body),
    Paragraph("<b>Industry fit:</b> Triaging customer reviews and support tickets, e.g. an e-commerce or "
              "telecom team auto-flagging clearly negative feedback so agents respond to it first.", body),
    Paragraph("<b>Biggest risk:</b> Confidently wrong labels. The model gave 99.98% to a sarcastic "
              "complaint, so decisions made on its score alone (without a neutral class or human review) "
              "would silently misread unhappy users.", body),
]

doc = SimpleDocTemplate(str(ROOT / "submission.pdf"), pagesize=A4, leftMargin=14 * mm,
                        rightMargin=14 * mm, topMargin=12 * mm, bottomMargin=12 * mm,
                        title="Session 5 Sentiment Analyzer", author="Muhammad Jibran Narejo")
doc.build(story)
print("wrote submission.pdf")
