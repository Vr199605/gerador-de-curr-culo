import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER
from io import BytesIO

def generate_pdf(data):
    buffer = BytesIO()
    # Criar o documento com margens
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    elements = []

    # --- ESTILOS CUSTOMIZADOS ---
    style_name = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontSize=26,
        textColor=colors.HexColor("#1A3A5F"),
        alignment=TA_CENTER,
        spaceAfter=2
    )
    
    style_contact = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    style_section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor("#1A3A5F"),
        spaceBefore=12,
        spaceAfter=6,
        borderPadding=(0, 0, 2, 0),
    )

    style_body = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14, # Espaçamento entre linhas
        alignment=0, # Justificado à esquerda
        spaceAfter=10
    )

    # --- MONTAGEM DO CONTEÚDO ---
    
    # Nome
    elements.append(Paragraph(data['nome'].upper(), style_name))
    
    # Contatos
    contatos = f"{data['email']}  •  {data['telefone']}<br/>{data['linkedin']}"
    elements.append(Paragraph(contatos, style_contact))

    # Função para adicionar seções com linha divisória
    def add_section(title, content):
        if content:
            elements.append(Paragraph(title.upper(), style_section_title))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1A3A5F"), spaceAfter=10))
            # Substituir quebras de linha por tags <br/> do HTML (necessário no ReportLab)
            formatted_content = content.replace('\n', '<br/>')
            elements.append(Paragraph(formatted_content, style_body))

    add_section("Resumo Profissional", data['resumo'])
    add_section("Experiência Profissional", data['experiencia'])
    add_section("Formação Acadêmica", data['formacao'])
    add_section("Habilidades e Competências", data['habilidades'])

    # Gerar o PDF
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Gerador de Currículo", layout="centered")

st.title("🚀 Curriculum Designer Pro")
st.info("Utilizando a engine ReportLab para máxima precisão visual.")

with st.form("resume_form"):
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome Completo")
        email = st.text_input("E-mail")
    with col2:
        telefone = st.text_input("Telefone")
        linkedin = st.text_input("LinkedIn")
    
    resumo = st.text_area("Resumo Profissional")
    experiencia = st.text_area("Experiência Profissional")
    formacao = st.text_area("Formação Acadêmica")
    habilidades = st.text_area("Habilidades Técnicas")
    
    submit = st.form_submit_button("GERAR PDF PERFEITO")

if submit:
    if nome and email:
        try:
            data = {
                "nome": nome, "email": email, "telefone": telefone,
                "linkedin": linkedin, "resumo": resumo,
                "experiencia": experiencia, "formacao": formacao,
                "habilidades": habilidades
            }
            
            pdf_result = generate_pdf(data)
            
            st.success("Currículo gerado com sucesso!")
            st.download_button(
                label="⬇️ Baixar PDF",
                data=pdf_result,
                file_name=f"Curriculo_{nome.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
    else:
        st.warning("Preencha ao menos Nome e E-mail.")
