import streamlit as st
from fpdf import FPDF

# Classe para configurar a estrutura e estética do PDF
class ResumePDF(FPDF):
    def header(self):
        # Espaço em branco no topo
        self.ln(10)

    def footer(self):
        # Rodapé com número de página
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

    def add_section_title(self, title):
        # Estilização dos títulos das seções
        self.set_font("helvetica", "B", 12)
        self.set_text_color(40, 70, 140)  # Tom de azul profissional
        self.cell(0, 10, title.upper(), ln=True)
        # Linha horizontal decorativa
        self.set_draw_color(40, 70, 140)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(4)

    def add_body_text(self, text):
        # Configuração do corpo de texto
        self.set_font("helvetica", "", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 6, text)
        self.ln(3)

def generate_pdf(data):
    # Inicializa o PDF (fpdf2 usa helvetica como padrão seguro para acentos)
    pdf = ResumePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # --- CABEÇALHO ---
    pdf.set_font("helvetica", "B", 24)
    pdf.cell(0, 12, data['nome'].upper(), ln=True, align="C")
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    contato = f"{data['email']}  |  {data['telefone']}  |  {data['linkedin']}"
    pdf.cell(0, 8, contato, ln=True, align="C")
    pdf.ln(10)

    # --- SEÇÕES ---
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

    # Retorna o PDF como uma sequência de bytes
    return pdf.output()

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Gerador de Currículo", page_icon="📄")

# CSS customizado para melhorar o visual da interface
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; background-color: #28468c; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 Gerador de Currículo Premium")
st.write("Preencha os campos abaixo para gerar um PDF profissional e formatado.")

with st.form("form_curriculo"):
    st.subheader("Informações Pessoais")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome Completo", placeholder="Ex: Victor Ricardo")
        email = st.text_input("E-mail", placeholder="seuemail@exemplo.com")
    with col2:
        telefone = st.text_input("Telefone", placeholder="(21) 99999-9999")
        linkedin = st.text_input("LinkedIn/Portfólio", placeholder="linkedin.com/in/seuusuario")
    
    st.divider()
    
    st.subheader("Conteúdo Profissional")
    resumo = st.text_area("Resumo Profissional", help="Uma breve apresentação sobre sua carreira.")
    experiencia = st.text_area("Experiência Profissional", help="Liste cargo, empresa e principais conquistas.")
    formacao = st.text_area("Formação Acadêmica", help="Curso, Instituição e ano de conclusão.")
    habilidades = st.text_area("Habilidades Técnicas", placeholder="Ex: Python, Excel Avançado, Gestão de Projetos...")
    
    submit_button = st.form_submit_button("GERAR MEU CURRÍCULO")

# --- LÓGICA DE GERAÇÃO ---
if submit_button:
    if not nome or not email:
        st.warning("Por favor, preencha o Nome e o E-mail para continuar.")
    else:
        try:
            dados_usuario = {
                "nome": nome, "email": email, "telefone": telefone,
                "linkedin": linkedin, "resumo": resumo,
                "experiencia": experiencia, "formacao": formacao,
                "habilidades": habilidades
            }
            
            # Gera os bytes do PDF
            pdf_output = generate_pdf(dados_usuario)
            
            st.success("✨ Seu currículo foi formatado com perfeição!")
            
            st.download_button(
                label="⬇️ Baixar Currículo em PDF",
                data=pdf_output,
                file_name=f"Curriculo_{nome.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Ocorreu um erro ao gerar o PDF: {e}")
