# -*- coding: utf-8 -*-
"""Generate PDF from the codebook Markdown (delivery artifact)."""
from __future__ import annotations

import re
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "docs" / "03_Libro_de_Codigos.md"
OUT_PATH = ROOT / "docs" / "03_Libro_de_Codigos.pdf"
FONT_REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
MARGIN = 18.0


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_x(MARGIN)
        self.set_font("Body", size=8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Libro de Codigos v1.0  |  Pagina {self.page_no()}/{{nb}}", align="C")


def strip_md(raw: str) -> str:
    raw = re.sub(r"\*\*(.+?)\*\*", r"\1", raw)
    raw = re.sub(r"`([^`]+)`", r"\1", raw)
    raw = re.sub(r"\*(.+?)\*", r"\1", raw)
    raw = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw)
    # Replace characters that can break layout in narrow cells
    raw = raw.replace("\u00a0", " ").replace("\t", " ")
    return raw


def usable_width(pdf: PDF) -> float:
    return pdf.w - pdf.l_margin - pdf.r_margin


def write_block(pdf: PDF, text: str, size: float = 10, bold: bool = False, lh: float = 5.5) -> None:
    pdf.set_x(pdf.l_margin)
    style = "B" if bold else ""
    pdf.set_font("Body", style, size)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(usable_width(pdf), lh, text)


def write_line(pdf: PDF, line: str) -> None:
    line = line.rstrip("\n")
    if not line.strip():
        pdf.ln(3)
        return

    if line.startswith("# "):
        write_block(pdf, strip_md(line[2:].strip()), size=16, bold=True, lh=8)
        pdf.ln(2)
        return
    if line.startswith("## "):
        pdf.ln(2)
        write_block(pdf, strip_md(line[3:].strip()), size=13, bold=True, lh=7)
        pdf.ln(1)
        return
    if line.startswith("### "):
        pdf.ln(1)
        write_block(pdf, strip_md(line[4:].strip()), size=11, bold=True, lh=6)
        return
    if line.strip() == "---":
        pdf.ln(1)
        y = pdf.get_y()
        pdf.set_draw_color(180, 180, 180)
        pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
        pdf.ln(3)
        return
    if line.strip().startswith("|"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c.replace(" ", "")) for c in cells if c):
            return
        row = " | ".join(cells)
        write_block(pdf, strip_md(row), size=9, lh=5)
        return

    raw = line.strip()
    if raw.startswith("- ") or raw.startswith("* "):
        raw = "- " + raw[2:]
    write_block(pdf, strip_md(raw), size=10, lh=5.5)


def main() -> None:
    text = MD_PATH.read_text(encoding="utf-8")
    pdf = PDF(format="Letter")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_font("Body", "", str(FONT_REGULAR))
    pdf.add_font("Body", "B", str(FONT_BOLD))
    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.add_page()
    for line in text.splitlines():
        write_line(pdf, line)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT_PATH))
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size} bytes, pages={pdf.pages_count})")


if __name__ == "__main__":
    main()
