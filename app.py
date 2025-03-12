from flask import Flask, render_template, request, session, redirect, url_for
import requests
#import supabase

app = Flask(__name__)
app.secret_key = "segredo_super_secreto"  # Necessário para usar session

# Configuração do Supabase
#SUPABASE_URL = "https://aonlgzucweiamkvhopnk.supabase.co"
#SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFvbmxnenVjd2VpYW1rdmhvcG5rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk1NTQ1NjAsImV4cCI6MjA1NTEzMDU2MH0.7ZMUNKvLeE6fMTDDMG71SCwCPqikkbyAlVDZB-qJTYs"
#supa = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# URL do webhook no n8n
WEBHOOK_URL = "https://n8n.gustavotadeu.com.br/webhook/analise_maturidade"

# Lista de perguntas do assessment
QUESTOES_ASSESSMENT = [
    "Existe uma estrutura formalizada de governança de segurança cibernética?",
    "Existem políticas e procedimentos documentados e atualizados?",
    "São realizadas auditorias regulares para verificar a conformidade?",
    "As funções e responsabilidades foram definidas em termos de segurança cibernética?",
    "A organização está alinhada com normas como ISO 27001, NIST, etc.?",
    "As revisões de conformidade são realizadas regularmente?",
    "Existe um processo formal para o gerenciamento de riscos de segurança cibernética?",
    "São realizadas avaliações regulares de risco de segurança?",
    "As medidas de mitigação baseadas na análise de risco estão em vigor?",
    "Os fornecedores terceirizados são avaliados em termos de segurança?",
    "Os ativos críticos de TI são identificados e documentados?",
    "Você tem uma estratégia de continuidade de negócios e recuperação de desastres em vigor?",
    "Os mecanismos de criptografia são aplicados a dados confidenciais?",
    "Você tem uma política segura de retenção e exclusão de dados?",
    "As ferramentas de prevenção de vazamento de dados (DLP) são usadas?",
    "Eles são regularmente copiados e testados regularmente?",
    "O acesso a dados confidenciais é restrito por permissões apropriadas?",
    "Existem controles em vigor para impedir o acesso não autorizado a dados críticos?",
    "A infraestrutura de rede é segmentada para minimizar o risco?",
    "São usados firewalls e sistemas de detecção de intrusão (IDS/IPS)?",
    "Os patches e atualizações de segurança são aplicados regularmente?",
    "A autenticação multifator (MFA) é usada para acesso crítico?",
    "As configurações de segurança em servidores e estações de trabalho são reforçadas?",
    "Existe monitoramento contínuo de tráfego e eventos de segurança?",
    "Existe um plano formal de resposta a incidentes?",
    "São realizados exercícios de resposta a incidentes?",
    "Você tem uma equipe ou gerente designado para gerenciar incidentes?",
    "Os incidentes ocorridos são documentados e analisados para melhorar a segurança?",
    "Existem mecanismos para notificar as partes interessadas sobre incidentes?",
    "A resposta a incidentes foi integrada com outras áreas do negócio?",
    "O treinamento em segurança cibernética é fornecido aos funcionários?",
    "As campanhas de conscientização estão sendo executadas em ameaças como phishing?",
    "Os funcionários conhecem as políticas de segurança da organização?",
    "Existe um programa de treinamento de segurança em andamento?",
    "A eficácia do treinamento é medida por meio de testes ou simulações?",
    "As novas contratações são induzidas em segurança cibernética?",
    "O princípio do menor privilégio de acesso é implementado?",
    "São usadas ferramentas para gerenciamento de acesso e autenticação?",
    "Os acessos são revogados em tempo hábil quando os funcionários são demitidos?",
    "Você aplica políticas de senha forte e autenticação multifator?",
    "Os acessos a recursos confidenciais são monitorados e registrados?",
    "Existem processos em vigor para revisar e auditar o acesso regularmente?",
    "Sua organização usa o Active Directory (AD) para gerenciamento de acesso centralizado?",
    "As Diretivas de Grupo (GPOs) são impostas para impor a segurança?",
    "Você tem uma ferramenta de gerenciamento de endpoint (MDM, EDR, etc.)?",
    "Foi implementado um sistema de Gerenciamento e Monitoramento de Logs (SIEM)?",
    "As soluções de controle de acesso à rede (NAC) são usadas?",
    "A infraestrutura tem segmentação de rede para limitar o acesso a recursos confidenciais?",
    "As ferramentas de automação de segurança (SOARs) foram implementadas?",
]

@app.route("/", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        # Salvando os dados do formulário na sessão
        session["cadastro"] = {
            "nome": request.form["nome"],
            "telefone": request.form["telefone"],
            "email": request.form["email"],
            "cargo": request.form["cargo"],
            "empresa": request.form["empresa"],
            "quantidade_funcionarios": request.form["quantidade_funcionarios"],
        }
        return redirect(url_for("assessment"))

    return render_template("cadastro.html")

@app.route("/assessment", methods=["GET", "POST"])
def assessment():
    if "cadastro" not in session:
        return redirect(url_for("cadastro"))  # Se não tiver cadastro, redireciona

    if request.method == "POST":
        respostas_assessment = {}

        for i, pergunta in enumerate(QUESTOES_ASSESSMENT):
            resposta = request.form.get(f"resposta_{i+1}", "").strip()
            respostas_assessment[f"q{i+1}"] = resposta

        # Montando JSON final no formato correto
        dados_finais = {
            **session["cadastro"],  # Dados do cadastro
            "respostas_assessment": respostas_assessment  # Respostas do assessment
        }

        # Enviando os dados para o n8n via Webhook
        try:
            response = requests.post(WEBHOOK_URL, json=dados_finais)
            if response.status_code == 200:
                return "✅ Dados enviados com sucesso!"
            else:
                return f"❌ Erro ao enviar os dados. Código {response.status_code}", 400
        except Exception as e:
            return f"❌ Falha na conexão com o webhook: {e}", 500

    return render_template("assessment.html", questoes=QUESTOES_ASSESSMENT)
'''
@app.route('/consulta', methods=['GET', 'POST'])
def index():
    resultados = None
    erro = None

    if request.method == 'POST':
        email_busca = request.form.get('email_busca')

        try:
            response = supa.rpc("custom_query", {"email_param": email_busca}).execute()
            resultados = response.data
        except Exception as e:
            erro = f"Erro ao buscar dados: {str(e)}"

    return render_template('consulta.html', resultados=resultados, erro=erro)
    
    '''
if __name__ == "__main__":
    app.run(debug=True)
