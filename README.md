# 📄 Gerador de Currículo Profissional (Python + LaTeX)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gerador-curriculo.streamlit.app)

Um aplicativo web interativo que gera currículos profissionais em **PDF** usando a precisão tipográfica e aparência sofisticada do **LaTeX**. O modelo foi otimizado para ser **ATS-Friendly** (Applicant Tracking Systems), garantindo que robôs de recrutamento consigam ler os dados corretamente, além de manter um design limpo e elegante para recrutadores humanos.

## Funcionalidades

*   **100% Otimizado para ATS:** Layout linear, sem colunas complexas, ícones ou tabelas que confundem robôs de leitura.
*   **Formulário Dinâmico:** Adicione ou remova quantas experiências profissionais e formações acadêmicas desejar.
*   **Personalizável:** Escolha a cor de destaque do currículo através de um seletor visual.
*   **Links Inteligentes:** Formatação automática para LinkedIn e E-mail clicáveis.
*   **Alta Qualidade Tipográfica:** Uso da fonte *Times New Roman* e espaçamentos milimetricamente calculados pelo motor do LaTeX.
*   **Design Responsivo:** Funciona perfeitamente em Computadores e Celulares.

## Privacidade e Segurança

Este projeto foi construído com **Privacy by Design**:
1.  **Sem Banco de Dados:** Nenhuma informação preenchida é salva permanentemente.
2.  **Processamento em Memória:** Os dados são processados apenas no momento da geração.
3.  **Isolamento de Sessão:** O sistema utiliza `UUID` para gerar nomes de arquivos únicos para cada clique, evitando colisão de dados entre usuários simultâneos.
4.  **Auto-Limpeza:** Os arquivos `.tex` e `.pdf` gerados são deletados do servidor imediatamente após o download.

##  Tecnologias Utilizadas

*   **[Python](https://www.python.org/):** Linguagem principal.
*   **[Streamlit](https://streamlit.io/):** Framework para a interface web interativa.
*   **[Jinja2](https://jinja.palletsprojects.com/):** Motor de template para injetar os dados do Python no código LaTeX.
*   **[LaTeX](https://www.latex-project.org/):** Sistema de preparação de documentos para gerar o PDF final.

##  Como Rodar Localmente

Para rodar este projeto na sua máquina, você precisará do Python e de uma distribuição LaTeX instalada.

### 1. Pré-requisitos
*   **Python 3.8+**
*   **Distribuição LaTeX:**
    *   *Windows:* Instale o [MiKTeX](https://miktex.org/) ou TeX Live.
    *   *Linux:* `sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-latex-extra`
    *   *Mac:* Instale o MacTeX.

### 2. Instalação

Clone o repositório:
```bash
git clone https://github.com/PHOdaSilva/gerador-curriculo.git
cd gerador-curriculo
```
Instale as dependências do Python:
```bash
pip install -r requirements.txt
```

### 3. Execução
Rode o aplicativo Streamlit:
```bash
streamlit run app.py
```

O navegador abrirá automaticamente no endereço http://localhost:8501.

## Deploy (Streamlit Cloud)

Este projeto está configurado para deploy fácil no Streamlit Community Cloud.
O arquivo packages.txt é crucial para o deploy, pois instrui o servidor Linux a instalar os pacotes LaTeX necessários sem precisar de acesso root:
```bash
texlive-latex-base
texlive-latex-recommended
texlive-latex-extra
texlive-fonts-recommended
```

## Estrutura do Projeto:
```bash
/
├── app.py              # Código principal (Frontend Streamlit + Lógica)
├── template.tex        # O modelo do currículo em LaTeX (Jinjificado)
├── requirements.txt    # Dependências Python (streamlit, jinja2)
├── packages.txt        # Dependências Linux (Compilador LaTeX)
└── README.md           # Documentação
```

## Contribuição
Sinta-se à vontade para fazer um Fork deste projeto, abrir Issues ou enviar Pull Requests. Sugestões de novos templates LaTeX são bem-vindas!

----

Desenvolvido por P.H. Silva.
