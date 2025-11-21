import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="OB Master Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PARA ESTILO "TRADER/DARK" ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stButton>button {
        background-color: #00ff7f;
        color: #000000;
        border: none;
        font-weight: bold;
    }
    .stHeader {
        color: #00ff7f;
    }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA API DO GOOGLE ---
# O Streamlit vai buscar a chave nos "Secrets" (segredos) do app
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Erro: Chave API não encontrada. Configure nos Secrets do Streamlit.")
    st.stop()

# --- O CÉREBRO (SYSTEM PROMPT) ---
system_instruction = """
Você é o "OB Master Agent", especialista em Marketing para Opções Binárias.
Seu tom é: Profissional, Trader de Elite, Persuasivo e focado em Conversão.
Sempre use formatação Markdown rica (negrito, listas, tabelas).
Não use introduções longas, vá direto ao ponto.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# --- FUNÇÃO PARA GERAR RESPOSTA ---
def ask_gemini(prompt):
    with st.spinner('Analisando mercado e gerando estratégia...'):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erro ao conectar com a IA: {e}"

# --- BARRA LATERAL (MENU) ---
st.sidebar.title("📈 OB MASTER")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Escolha a Ferramenta:",
    ["🏠 Dashboard", 
     "📝 Gerador de Conteúdo", 
     "🌪️ Criador de Funis", 
     "📊 Analisador de Performance", 
     "🎨 Gerador de Criativos",
     "💎 Gerador de Ofertas"]
)
st.sidebar.markdown("---")
st.sidebar.info("Status: **Online** 🟢")

# --- TELAS DO APP ---

if menu == "🏠 Dashboard":
    st.title("Bem-vindo ao QG do Trader")
    st.markdown("""
    Selecione uma ferramenta no menu lateral para começar a operar seu marketing.
    
    ### Resumo do Dia:
    * **Foco:** Alta conversão.
    * **Meta:** Captura de Leads e FTDs.
    """)

elif menu == "📝 Gerador de Conteúdo":
    st.header("📝 Gerador de Posts e Copy")
    tema = st.text_input("Qual o tema do post? (Ex: Estratégia M5, Mindset, Resultado do dia)")
    estilo = st.selectbox("Estilo:", ["Agressivo/Ostentação", "Educativo/Técnico", "Motivacional", "Misterioso"])
    plataforma = st.selectbox("Onde vai postar?", ["Instagram Feed", "Instagram Stories", "Telegram", "E-mail"])
    
    if st.button("Gerar Conteúdo"):
        if tema:
            prompt = f"Crie um conteúdo para {plataforma} sobre '{tema}'. Estilo: {estilo}. Inclua Headline, Texto persuasivo e CTA."
            resultado = ask_gemini(prompt)
            st.markdown("---")
            st.markdown(resultado)
        else:
            st.warning("Preencha o tema primeiro.")

elif menu == "🌪️ Criador de Funis":
    st.header("🌪️ Arquiteto de Funis")
    objetivo = st.text_input("Qual o objetivo final? (Ex: Venda de Mentoria, Cadastro na Corretora)")
    
    if st.button("Construir Funil"):
        prompt = f"Crie um funil de vendas completo para: {objetivo}. Inclua: 1. Script de Vídeo, 2. Headline da Landing Page, 3. Sequência de 3 e-mails."
        resultado = ask_gemini(prompt)
        st.markdown("---")
        st.markdown(resultado)

elif menu == "📊 Analisador de Performance":
    st.header("📊 Diagnóstico de Métricas")
    col1, col2, col3 = st.columns(3)
    cliques = col1.number_input("Cliques no Link", min_value=0)
    cadastros = col2.number_input("Cadastros (Leads)", min_value=0)
    vendas = col3.number_input("Depósitos/Vendas", min_value=0)
    
    if st.button("Analisar Dados"):
        prompt = f"Analise estes dados de tráfego para Opções Binárias: {cliques} cliques, {cadastros} cadastros, {vendas} vendas. Calcule as taxas de conversão, diagnostique o problema (Criativo, LP ou Oferta) e me diga o que fazer."
        resultado = ask_gemini(prompt)
        st.markdown("---")
        st.success("Diagnóstico Realizado:")
        st.markdown(resultado)

elif menu == "🎨 Gerador de Criativos":
    st.header("🎨 Prompt para Imagens (Midjourney/DALL-E)")
    ideia = st.text_input("Descreva a cena básica (Ex: Trader operando no celular em Dubai)")
    
    if st.button("Criar Prompt"):
        prompt = f"Crie um prompt detalhado e profissional em INGLÊS para gerar uma imagem realista de IA. Base: {ideia}. Estilo: Trader profissional, dark mode, luzes neon, luxo, alta definição."
        resultado = ask_gemini(prompt)
        st.markdown("---")
        st.code(resultado, language="text")

elif menu == "💎 Gerador de Ofertas":
    st.header("💎 Criador de Ofertas Irresistíveis")
    produto = st.text_input("O que você está vendendo/indicando?")
    
    if st.button("Gerar 3 Versões"):
        prompt = f"Crie 3 níveis de oferta (Leve, Moderada, Agressiva) para o produto: {produto}. Use gatilhos mentais de escassez e urgência."
        resultado = ask_gemini(prompt)
        st.markdown("---")
        st.markdown(resultado)
