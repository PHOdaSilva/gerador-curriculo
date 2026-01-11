import streamlit as st
import os
import subprocess
import uuid
from jinja2 import Environment, FileSystemLoader

# Configuração da página
st.set_page_config(page_title="Gerador de Currículos", page_icon="📄", layout="wide")

st.title("📄 Gerador de Currículo")
st.markdown("""
Preencha os campos abaixo para gerar um currículo profissional.

Atenção: Seus dados são processados apenas na memória temporária para gerar o PDF e são descartados imediatamente. Nenhuma informação é salva em banco de dados.
""")

# --- INICIALIZAÇÃO DO ESTADO ---
if 'num_experiencias' not in st.session_state:
    st.session_state.num_experiencias = 1
if 'num_formacoes' not in st.session_state:
    st.session_state.num_formacoes = 1

# --- DADOS PESSOAIS ---
st.header("1. Dados Pessoais")
cor_escolhida = st.color_picker("Selecione uma cor de destaque (opcional):", "#000000")

col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Nome Completo", placeholder="Ex: MARIA DA SILVA")
    email = st.text_input("Email", placeholder="Ex: maria@email.com")
    telefone = st.text_input("Telefone", placeholder="Ex: (11) 99999-9999")
with col2:
    titulo = st.text_input("Título Profissional", placeholder="Ex: Engenheira Civil")
    localizacao = st.text_input("Cidade, UF", placeholder="Ex: São Paulo, SP")
    linkedin = st.text_input("LinkedIn", placeholder="Ex: linkedin.com/in/maria")

resumo = st.text_area("Resumo Profissional", placeholder="Ex: Profissional com sólida experiência em...")

st.markdown("---")

# --- EXPERIÊNCIA ---
st.header("2. Experiência Profissional")

for i in range(st.session_state.num_experiencias):
    st.subheader(f"Experiência {i+1}")
    
    c1, c2, c3 = st.columns([3, 2, 2])
    with c1:
        st.text_input("Cargo", key=f"cargo_{i}", placeholder="Ex: Analista Sênior")
    with c2:
        st.text_input("Período", key=f"periodo_exp_{i}", placeholder="Ex: Jan/2023 - Dez/2025")
    with c3:
        st.text_input("Empresa", key=f"empresa_{i}", placeholder="Ex: Google")
    
    col_local, col_desc = st.columns([2, 4])
    with col_local:
        st.text_input("Local", key=f"local_exp_{i}", placeholder="Ex: São Paulo, SP")
    with col_desc:
        st.text_area("Descrição das atividades", key=f"desc_exp_{i}", height=100)
    
    st.markdown("")

col_btn_1, col_btn_2 = st.columns([1, 5])
with col_btn_1:
    if st.button("➕ Adicionar Experiência"):
        st.session_state.num_experiencias += 1
        st.rerun()
with col_btn_2:
    if st.session_state.num_experiencias > 1:
        if st.button("➖ Remover Última Exp."):
            st.session_state.num_experiencias -= 1
            st.rerun()

st.markdown("---")

# --- FORMAÇÃO ---
st.header("3. Formação Acadêmica")

for i in range(st.session_state.num_formacoes):
    st.subheader(f"Formação {i+1}")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Curso", key=f"curso_{i}", placeholder= "Ex: Ciência da Computação")
        st.text_input("Instituição", key=f"inst_{i}",placeholder="Ex: Universidade de São Paulo")
    with c2:
        st.text_input("Período", key=f"periodo_form_{i}",placeholder="Ex: Jan/2023 - Dez/2025")
        st.text_input("Local", key=f"local_form_{i}", placeholder="Ex: São Paulo, SP")
    st.markdown("")

col_btn_f1, col_btn_f2 = st.columns([1, 5])
with col_btn_f1:
    if st.button("➕ Adicionar Formação"):
        st.session_state.num_formacoes += 1
        st.rerun()
with col_btn_f2:
    if st.session_state.num_formacoes > 1:
        if st.button("➖ Remover Última Form."):
            st.session_state.num_formacoes -= 1
            st.rerun()

st.markdown("---")

# --- PROFICIÊNCIAS ---
st.header("4. Habilidades e Idiomas")

col_skills_1, col_skills_2 = st.columns(2)

with col_skills_1:
    st.subheader("Idiomas")
    idiomas_txt = st.text_area("Liste os idiomas (um por linha ou separado por vírgula)", placeholder="Inglês Fluente\nEspanhol Intermediário")

with col_skills_2:
    st.subheader("Proficiências")
    st.caption("Softwares, Ferramentas e Soft Skills")
    skills_txt = st.text_area("Liste as proficiências (uma por linha ou separada por vírgula)", placeholder="Python, Excel Avançado, Gestão de Projetos, Comunicação")

st.markdown("---")

# --- BOTÃO FINAL ---
if st.button("GERAR CURRÍCULO EM PDF", type="primary"):
    
    with st.spinner("Compilando seu currículo..."):
        
        # 1. COLETAR EXPERIÊNCIAS
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

        # 2. COLETAR FORMAÇÕES
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

        # 3. TRATAR LISTAS 
        def processar_lista(texto):
            if "\n" in texto:
                return [x.strip() for x in texto.split("\n") if x.strip()]
            return [x.strip() for x in texto.split(",") if x.strip()]

        idiomas_list = processar_lista(idiomas_txt)
        skills_list = processar_lista(skills_txt)
        
        cor_latex = cor_escolhida.lstrip('#').upper()

        # Tratamento do LinkedIn
        linkedin_texto = linkedin.strip().replace("https://", "").replace("http://", "").replace("www.", "")
        
        linkedin_link = linkedin.strip()
        if not linkedin_link.startswith("http"):
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

        # 4. GERAÇÃO DO PDF
        env = Environment(
            loader=FileSystemLoader('.'),
            block_start_string='\BLOCK{',
            block_end_string='}',
            variable_start_string='\VAR{',
            variable_end_string='}',
            comment_start_string='\#{',
            comment_end_string='}',
        )

        # Gera ID único para os arquivos desta execução
        session_id = str(uuid.uuid4())
        arquivo_tex = f"cv_{session_id}.tex"
        arquivo_pdf = f"cv_{session_id}.pdf"

        try:
            template = env.get_template('template.tex')
            latex_renderizado = template.render(dados=dados)

            # Salva com nome único
            with open(arquivo_tex, 'w', encoding='utf-8') as f:
                f.write(latex_renderizado)

            # Compila o arquivo único
            process = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", arquivo_tex], 
                capture_output=True
            )

            if process.returncode != 0:
                st.error("Erro na compilação do LaTeX!")
                st.code(process.stdout.decode('latin-1')[-1500:])
            else:
                st.success("Sucesso! Baixe seu currículo abaixo:")
                # Lê o PDF gerado
                with open(arquivo_pdf, "rb") as pdf_file:
                    st.download_button(
                        label="⬇️ Baixar PDF",
                        data=pdf_file,
                        file_name=f"Curriculo_{nome.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
            
            # Limpeza
            arquivos_para_apagar = [arquivo_tex, arquivo_pdf, f"cv_{session_id}.log", f"cv_{session_id}.aux", f"cv_{session_id}.out"]
            for arq in arquivos_para_apagar:
                if os.path.exists(arq):
                    os.remove(arq)

        except Exception as e:
            st.error(f"Erro: {e}")
