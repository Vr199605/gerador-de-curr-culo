import streamlit as st
from fpdf import FPDF

class ResumePDF(FPDF):
    def header(self):
        # Estética do cabeçalho pode ser personalizada aqui
        pass

    def add_section_title(self, title):
        self.set_font("Arial", 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, title.upper(), ln=True, fill=True)
        self.ln(2)

    def add_body_text(self, text, bold=False):
        style = 'B' if bold else ''
        self.set_font("Arial", style, 10)
        self.multi_cell(0, 6, text)
        self.ln(1)

def generate_pdf(data):
    pdf = ResumePDF()
    pdf.add_page()
    
    # Nome e Contato
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 10, data['nome'].upper(), ln=True, align='C')
    pdf.set_font("Arial", '', 10)
    contact_info = f"{data['email']} | {data['telefone']} | {data['linkedin']}"
    pdf.cell(0, 10, contact_info, ln=True, align='C')
    pdf.ln(5)

    # Resumo Profissional
    pdf.add_section_title("Resumo Profissional")
    pdf.add_body_text(data['resumo'])
    pdf.ln(3)

    # Experiência
    pdf.add_section_title("Experiência Profissional")
    pdf.add_body_text(data['experiencia'])
    pdf.ln(3)

    # Formação
    pdf.add_section_title("Formação Acadêmica")
    pdf.add_body_text(data['formacao'])
    pdf.ln(3)

    # Habilidades
    pdf.add_section_title("Habilidades Técnicas")
    pdf.add_body_text(data['habilidades'])

    return pdf.output(dest='S').encode('latin-1')

# Interface Streamlit
st.set_page_config(page_title="Gerador de Currículo Premium", layout="centered")

st.title("📄 Resume Builder Pro")
st.subheader("Crie um currículo impecável em segundos")

with st.form("resume_form"):
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome Completo")
        email = st.text_input("E-mail")
    with col2:
        telefone = st.text_input("Telefone/WhatsApp")
        linkedin = st.text_input("Link do LinkedIn")
    
    resumo = st.text_area("Resumo Profissional (Destaque seus pontos fortes)")
    experiencia = st.text_area("Experiência (Empresa - Cargo - Período - Atividades)")
    formacao = st.text_area("Formação Acadêmica")
    habilidades = st.text_input("Habilidades (Separe por vírgulas)")
    
    submit = st.form_submit_button("Gerar Currículo Perfeito")

if submit:
    if nome and email:
        data = {
            "nome": nome, "email": email, "telefone": telefone,
            "linkedin": linkedin, "resumo": resumo,
            "experiencia": experiencia, "formacao": formacao, "habilidades": habilidades
        }
        
        pdf_bytes = generate_pdf(data)
        
        st.success("✅ Currículo gerado com sucesso!")
        st.download_button(
            label="⬇️ Baixar PDF",
            data=pdf_bytes,
            file_name=f"Curriculo_{nome.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Por favor, preencha pelo menos o nome e o e-mail.")
