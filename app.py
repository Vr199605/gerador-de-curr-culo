import streamlit as st
from fpdf import FPDF

class ResumePDF(FPDF):
    def add_section_title(self, title):
        # Usando 'helvetica' mas garantindo que o título esteja limpo
        self.set_font("helvetica", "B", 12)
        self.set_text_color(40, 70, 140)
        self.cell(0, 10, title.upper(), ln=True)
        self.set_draw_color(40, 70, 140)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(4)

    def add_body_text(self, text):
        # Limpeza de caracteres Unicode que a fonte básica não entende
        text = text.replace("’", "'").replace("–", "-").replace("“", '"').replace("”", '"')
        self.set_font("helvetica", "", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, text)
        self.ln(3)

def generate_pdf(data):
    pdf = ResumePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Limpando o nome também
    nome_limpo = data['nome'].replace("’", "'")
    
    # --- CABEÇALHO ---
    pdf.set_font("helvetica", "B", 24)
    pdf.cell(0, 12, nome_limpo.upper(), ln=True, align="C")
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    contato = f"{data['email']}  |  {data['telefone']}  |  {data['linkedin']}"
    pdf.cell(0, 8, contato, ln=True, align="C")
    pdf.ln(10)

    # --- SEÇÕES (A limpeza agora ocorre dentro de add_body_text) ---
    if data['resumo']:
        pdf.add_section_title("Resumo Profissional")
        pdf.add_body_text(data['resumo'])

    if data['experiencia']:
        pdf.add_section_title("Experiência Profissional")
        pdf.add_body_text(data['experiencia'])

    if data['formacao']:
        pdf.add_section_title("Formação Acadêmica")
        pdf.add_body_text(data['formacao'])

    if data['habilidades']:
        pdf.add_section_title("Habilidades e Competências")
        pdf.add_body_text(data['habilidades'])

    return pdf.output()
