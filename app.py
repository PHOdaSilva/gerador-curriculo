import streamlit as st
import os
import subprocess
import uuid
from jinja2 import Environment, FileSystemLoader

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Gerador de Currículo Profissional", 
    page_icon="📄", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PERSONALIZADO (Visual Pro) ---
st.markdown("""
<style>
    /* Ajuste de espaçamento do título */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Destaque para os botões de adicionar */
    button[kind="secondary"] {
        border-color: #e0e0e0;
    }
    /* Estilo do botão Principal (Gerar PDF) */
    div.stButton > button:first-child {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    /* Cards de inputs com borda suave */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        background-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO ---
if 'num_experiencias' not in st.session_state:
    st.session_state.num_experiencias = 1
if 'num_formacoes' not in st.session_state:
    st.session_state.num_formacoes = 1

# --- SIDEBAR (Barra Lateral) ---
with st.sidebar:
    st.title("⚙️ Configurações")
    st.markdown("Personalize a aparência do seu documento.")
    
    cor_escolhida = st.color_picker("Cor de Destaque (Títulos):", "#093967")
    
    st.divider()
    
    st.info("""
    ℹ️ **Como funciona?**
    
    Este gerador cria um currículo profissional e otimizado para **ATS** (robôs de recrutamento).
    
    1. Preencha seus dados.
    2. Adicione suas experiências.
    3. Baixe o PDF pronto.
    
    🔒 **Privacidade:**
    Seus dados são processados na memória e deletados imediatamente após o download.
    """)

# --- CABEÇALHO PRINCIPAL ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.markdown("# 📄")
with col_title:
    st.title("Gerador de Currículo Profissional")
    st.markdown("Crie um currículo limpo, organizado e legível por humanos e robôs.")

st.divider()

# --- 1. DADOS PESSOAIS ---
st.subheader("1. 👤 Dados Pessoais")

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome Completo", placeholder="Ex: MARIA DA SILVA")
        email = st.text_input("Email", placeholder="Ex: maria@email.com")
        telefone = st.text_input("Telefone", placeholder="Ex: (11) 99999-9999")
    with col2:
        titulo = st.text_input("Título Profissional", placeholder="Ex: Engenheira Civil")
        localizacao = st.text_input("Cidade, UF", placeholder="Ex: São Paulo, SP")
        linkedin = st.text_input("LinkedIn", placeholder="Ex: linkedin.com/in/maria")

    resumo = st.text_area("Resumo Profissional", placeholder="Ex: Profissional com 5 anos de experiência em gestão de projetos, focado em metodologias ágeis...", height=100)

st.write("") # Espaço

# --- 2. EXPERIÊNCIA ---
st.subheader("2. 💼 Experiência Profissional")
st.caption("Liste suas experiências da mais recente para a mais antiga.")

for i in range(st.session_state.num_experiencias):
    # Container com borda para agrupar cada experiência visualmente
    with st.container(border=True):
        col_header, col_delete = st.columns([8, 1])
        with col_header:
            st.markdown(f"**Experiência #{i+1}**")
        
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1:
            st.text_input("Cargo", key=f"cargo_{i}", placeholder="Ex: Analista Sênior")
        with c2:
            st.text_input("Empresa", key=f"empresa_{i}", placeholder="Ex: Google")
        with c3:
            st.text_input("Período", key=f"periodo_exp_{i}", placeholder="Ex: Jan/2023 - Atual")
        
        col_local, col_desc = st.columns([2, 4])
        with col_local:
            st.text_input("Local", key=f"local_exp_{i}", placeholder="Ex: São Paulo, SP")
        with col_desc:
            st.text_area("Descrição das atividades", key=f"desc_exp_{i}", height=100, placeholder="Descreva suas principais responsabilidades e conquistas...")

# Botões de controle (Adicionar/Remover)
col_btn_1, col_btn_2, col_vazia = st.columns([2, 2, 4])
with col_btn_1:
    if st.button("➕ Adicionar Experiência", use_container_width=True):
        st.session_state.num_experiencias += 1
        st.rerun()
with col_btn_2:
    if st.session_state.num_experiencias > 1:
        if st.button("🗑️ Remover Última", type="secondary", use_container_width=True):
            st.session_state.num_experiencias -= 1
            st.rerun()

st.divider()

# --- 3. FORMAÇÃO ---
st.subheader("3. 🎓 Formação Acadêmica")

for i in range(st.session_state.num_formacoes):
    with st.container(border=True):
        st.markdown(f"**Formação #{i+1}**")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Curso", key=f"curso_{i}", placeholder= "Ex: Ciência da Computação")
            st.text_input("Instituição", key=f"inst_{i}",placeholder="Ex: USP")
        with c2:
            st.text_input("Período", key=f"periodo_form_{i}",placeholder="Ex: 2019 - 2023")
            st.text_input("Local", key=f"local_form_{i}", placeholder="Ex: São Paulo, SP")

col_btn_f1, col_btn_f2, col_vazia_f = st.columns([2, 2, 4])
with col_btn_f1:
    if st.button("➕ Adicionar Formação", use_container_width=True):
        st.session_state.num_formacoes += 1
        st.rerun()
with col_btn_f2:
    if st.session_state.num_formacoes > 1:
        if st.button("🗑️ Remover Última", type="secondary", use_container_width=True):
            st.session_state.num_formacoes -= 1
            st.rerun()

st.divider()

# --- 4. HABILIDADES ---
st.subheader("4. 🚀 Habilidades e Idiomas")

with st.container(border=True):
    col_skills_1, col_skills_2 = st.columns(2)
    with col_skills_1:
        st.markdown("**Idiomas**")
        idiomas_txt = st.text_area("Liste os idiomas", placeholder="Inglês Fluente\nEspanhol Intermediário", height=150, help="Pule uma linha para cada idioma.")
    with col_skills_2:
        st.markdown("**Proficiências**")
        skills_txt = st.text_area("Liste softwares e soft skills", placeholder="Python, Excel Avançado, Gestão de Projetos, Comunicação, Liderança", height=150, help="Separe por vírgulas ou pule linhas.")

st.write("")
st.write("")

# --- BOTÃO FINAL ---
# Centralizar o botão de ação
_, col_main_btn, _ = st.columns([1, 2, 1])

with col_main_btn:
    if st.button("GERAR CURRÍCULO EM PDF", type="primary"):
        
        with st.spinner("Compilando seu currículo... (Isso leva uns segundinhos)"):
            
            # --- COLETA DE DADOS ---
            lista_experiencias = []
            for i in range(st.session_state.num_experiencias):
                cargo = st.session_state.get(f"cargo_{i}", "")
                if cargo:
                    lista_experiencias.append({
                        "cargo": cargo,
                        "empresa": st.session_state.get(f"empresa_{i}", ""),
                        "periodo": st.session_state.get(f"periodo_exp_{i}", ""),
                        "local": st.session_state.get(f"local_exp_{i}", ""),
                        "descricao": st.session_state.get(f"desc_exp_{i}", "")
                    })

            lista_formacoes = []
            for i in range(st.session_state.num_formacoes):
                curso = st.session_state.get(f"curso_{i}", "")
                if curso:
                    lista_formacoes.append({
                        "curso": curso,
                        "instituicao": st.session_state.get(f"inst_{i}", ""),
                        "periodo": st.session_state.get(f"periodo_form_{i}", ""),
                        "local": st.session_state.get(f"local_form_{i}", "")
                    })

            def processar_lista(texto):
                if "\n" in texto:
                    return [x.strip() for x in texto.split("\n") if x.strip()]
                return [x.strip() for x in texto.split(",") if x.strip()]

            idiomas_list = processar_lista(idiomas_txt)
            skills_list = processar_lista(skills_txt)
            
            cor_latex = cor_escolhida.lstrip('#').upper()

            # Tratamento LinkedIn e Email
            linkedin_texto = linkedin.strip().replace("https://", "").replace("http://", "").replace("www.", "")
            linkedin_link = linkedin.strip()
            if linkedin_link and not linkedin_link.startswith("http"):
                linkedin_link = f"https://{linkedin_link}"

            dados = {
                "cor": cor_latex,
                "nome": nome,
                "titulo": titulo,
                "email": email, 
                "telefone": telefone,
                "localizacao": localizacao,
                "linkedin_texto": linkedin_texto,
                "linkedin_link": linkedin_link,
                "resumo": resumo,
                "experiencias": lista_experiencias,
                "formacoes": lista_formacoes,
                "idiomas": idiomas_list,
                "skills": skills_list
            }

            # --- GERAÇÃO DO PDF ---
            env = Environment(
                loader=FileSystemLoader('.'),
                block_start_string='\BLOCK{',
                block_end_string='}',
                variable_start_string='\VAR{',
                variable_end_string='}',
                comment_start_string='\#{',
                comment_end_string='}',
            )

            session_id = str(uuid.uuid4())
            arquivo_tex = f"cv_{session_id}.tex"
            arquivo_pdf = f"cv_{session_id}.pdf"

            try:
                template = env.get_template('template.tex')
                latex_renderizado = template.render(dados=dados)

                with open(arquivo_tex, 'w', encoding='utf-8') as f:
                    f.write(latex_renderizado)

                subprocess.run(["pdflatex", "-interaction=nonstopmode", arquivo_tex], capture_output=True)
                
           
                process = subprocess.run(
                    ["pdflatex", "-interaction=nonstopmode", arquivo_tex], 
                    capture_output=True
                )

                if os.path.exists(arquivo_pdf):
                    st.success("✅ Currículo gerado com sucesso!")
                    with open(arquivo_pdf, "rb") as pdf_file:
                        st.download_button(
                            label="⬇️ BAIXAR MEU CURRÍCULO (PDF)",
                            data=pdf_file,
                            file_name=f"Curriculo_{nome.replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True
                        )
                else:
                 
                    st.error("Ops! Ocorreu um erro na criação do PDF.")
                    with st.expander("Ver detalhes do erro (Logs)"):
                        st.code(process.stdout.decode('latin-1')[-1500:])
                
                # Limpeza
                arquivos_para_apagar = [arquivo_tex, arquivo_pdf, f"cv_{session_id}.log", f"cv_{session_id}.aux", f"cv_{session_id}.out"]
                for arq in arquivos_para_apagar:
                    if os.path.exists(arq):
                        os.remove(arq)

            except Exception as e:
                st.error(f"Erro interno: {e}")



