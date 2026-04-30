import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from io import BytesIO

def generate_psychology_pdf(data):
    buffer = BytesIO()
    # Criar o documento com margens generosas para um visual limpo e calmo
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    elements = []

    # --- PALETA DE CORES PSICOLOGIA (Sóbria e Acolhedora) ---
    color_primary = colors.HexColor("#1A3A5F") # Azul Petróleo Profundo (Profissionalismo, calma)
    color_secondary = colors.HexColor("#4F4F4F") # Cinza Escuro (Sobriedade, leitura fácil)
    color_accent = colors.HexColor("#A9A9A9") # Cinza Claro (Divisores sutis)

    # --- ESTILOS CUSTOMIZADOS ---
    # Título do Nome: Fonte elegante, cor sóbria, centralizado
    style_name = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=color_primary,
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    # Informações de Contato: Fonte menor, cor neutra, centralizado, espaçamento sutil
    style_contact = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=color_secondary,
        alignment=TA_CENTER,
        spaceAfter=24,
        fontName='Helvetica'
    )

    # Títulos das Seções: Fonte média, cor primária, alinhado à esquerda, sem linhas intrusivas
    style_section_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=color_primary,
        spaceBefore=16,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )

    # Corpo do Texto: Fonte legível, cor neutra, justificado, espaçamento generoso entre linhas
    style_body = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14, # Espaçamento entre linhas (muito importante para psicologia)
        textColor=color_secondary,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName='Helvetica'
    )

    # --- MONTAGEM DO CONTEÚDO (Cabeçalho Perfeito) ---
    
    # Nome (Correção da imagem: sem sobreposição)
    elements.append(Paragraph(data['nome'].upper(), style_name))
    
    # Contatos (Formatados elegantemente abaixo do nome)
    contatos = f"{data['email']}  •  {data['telefone']}<br/>{data['linkedin']}"
    elements.append(Paragraph(contatos, style_contact))

    # --- DIVISOR SUTIL (Substituindo a linha grossa) ---
    elements.append(HRFlowable(width="100%", thickness=0.5, color=color_accent, spaceAfter=20))

    # Função para adicionar seções com formatação de psicologia
    def add_section(title, content):
        if content:
            elements.append(Paragraph(title.upper(), style_section_title))
            # Substituir quebras de linha por tags <br/> do HTML (necessário no ReportLab)
            formatted_content = content.replace('\n', '<br/>')
            elements.append(Paragraph(formatted_content, style_body))

    add_section("Resumo Profissional", data['resumo'])
    add_section("Experiência Clínica", data['experiencia'])
    add_section("Formação Acadêmica", data['formacao'])
    add_section("Áreas de Atuação e Especialidades", data['habilidades'])
    add_section("Cursos e Certificações", data['certificacoes'])

    # Gerar o PDF
    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

# --- INTERFACE STREAMLIT (Limpa e Funcional) ---
st.set_page_config(page_title="Gerador de Currículo - Psicologia", layout="centered")

# CSS para esconder o menu do Streamlit para um visual mais profissional na ferramenta
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("🌱 Curriculum Vitae - Psicologia")
st.markdown("---")

with st.form("resume_form"):
    st.subheader("Informações Pessoais")
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome Completo", placeholder="Débora de Carvalho Moreira")
        email = st.text_input("E-mail", placeholder="seu.email@exemplo.com")
    with col2:
        telefone = st.text_input("Telefone (com DDD)", placeholder="(11) 9XXXX-XXXX")
        linkedin = st.text_input("LinkedIn (opcional)", placeholder="linkedin.com/in/seuusuario")
    
    st.divider()
    
    st.subheader("Conteúdo Profissional")
    resumo = st.text_area("Resumo Profissional (Breve introdução sobre sua abordagem e foco)")
    experiencia = st.text_area("Experiência Clínica (Instituições, Clínicas, Tempo, Principais demandas)")
    formacao = st.text_area("Formação Acadêmica (Graduação, Pós-graduação, Instituição, Ano)")
    habilidades = st.text_area("Áreas de Atuação e Especialidades (Terapia Cognitivo-Comportamental, etc.)")
    certificacoes = st.text_area("Cursos e Certificações (Cursos relevantes, Congressos)")
    
    st.divider()
    submit = st.form_submit_button("GERAR CURRÍCULO PROFISSIONAL EM PDF")

if submit:
    if nome and email and resumo and experiencia and formacao:
        try:
            data = {
                "nome": nome, "email": email, "telefone": telefone,
                "linkedin": linkedin, "resumo": resumo,
                "experiencia": experiencia, "formacao": formacao,
                "habilidades": habilidades,
                "certificacoes": certificacoes
            }
            
            pdf_result = generate_psychology_pdf(data)
            
            st.success("✨ Currículo gerado com sucesso!")
            st.download_button(
                label="⬇️ BAIXAR PDF",
                data=pdf_result,
                file_name=f"Curriculo_{nome.replace(' ', '_')}_Psicologia.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Erro ao processar a geração do PDF: {e}")
    else:
        st.warning("Por favor, preencha pelo menos os campos obrigatórios: Nome, E-mail, Resumo, Experiência e Formação.")
