
from flask import Flask, jsonify, render_template, request
import re

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")
    


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "projeto": "Seguranca Digital nas Comunidades"
    })



@app.route("/chat", methods=["POST"])
def chat():
    dados = request.get_json(silent = True) or {}
    pergunta = dados.get("mensagem", "")

    if not isinstance(pergunta, str) or not pergunta.strip():
        return jsonify({
            "resposta":    "Digite uma pergunta para começar."
        }),400

    pergunta = pergunta.strip()


 # Proteção inicial contra alguns dados sensíveis.
    padroes_sensiveis = [
        r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
        r"\b(?:senha|password|token)\s*[:=]\s*\S+",
        r"\b\d{11}\b"
    ]

    if any(
        re.search(padrao, pergunta, re.IGNORECASE)
        for padrao in padroes_sensiveis
    ):
        return jsonify({
            "resposta": (
                "⚠️ Sua mensagem pode conter dados sensíveis. "
                "Não envie CPF, senhas ou códigos de verificação. "
                "Reformule sua pergunta sem informações pessoais."
            )
        })

    texto = pergunta.lower()

    if any(p in texto for p in ["pix", "transferência", "transferi dinheiro"]):
        resposta = (
            "Se você suspeita de um golpe envolvendo Pix, "
            "entre em contato imediatamente com seu banco "
            "pelo aplicativo ou canal oficial. Guarde os comprovantes "
            "e pergunte sobre o Mecanismo Especial de Devolução (MED). "
            "A devolução não é garantida."
        )

    elif any(p in texto for p in ["whatsapp", "whats"]):
        resposta = (
            "Para proteger seu WhatsApp, ative a confirmação em "
            "duas etapas, nunca compartilhe códigos de verificação "
            "e confira os dispositivos conectados. Se perdeu o acesso, "
            "siga o procedimento de recuperação oficial do WhatsApp."
        )

    elif any(p in texto for p in ["senha", "senhas", "password"]):
        resposta = (
            "Use senhas longas e exclusivas para cada serviço. "
            "Um gerenciador de senhas e a verificação em duas etapas "
            "podem ajudar a proteger suas contas. Nunca compartilhe "
            "suas senhas ou códigos de acesso."
        )

    elif any(p in texto for p in ["link", "phishing", "mensagem suspeita", "golpe"]):
        resposta = (
            "Desconfie de mensagens urgentes, ofertas boas demais "
            "e links inesperados. Não clique nem informe códigos. "
            "Verifique a mensagem por um canal oficial, acessado "
            "diretamente, sem usar o link recebido."
        )

    elif any(p in texto for p in ["privacidade", "dados pessoais", "cpf"]):
        resposta = (
            "Compartilhe apenas os dados estritamente necessários. "
            "Confira a legitimidade do site antes de preencher formulários "
            "e nunca publique documentos, senhas ou códigos em chats."
        )

    elif any(p in texto for p in ["wifi", "wi-fi", "rede pública"]):
        resposta = (
            "Em redes Wi-Fi públicas, evite operações sensíveis "
            "quando não puder verificar a segurança da conexão. "
            "Confira o endereço dos sites e prefira aplicativos "
            "e páginas oficiais."
        )

    else:
        resposta = (
            "Ainda não tenho uma orientação revisada para essa dúvida. "
            "Tente perguntar sobre golpes, Pix, WhatsApp, senhas, "
            "privacidade ou Wi-Fi. Em caso de fraude, procure "
            "imediatamente a instituição envolvida pelo canal oficial."
        )

    return jsonify({"resposta": resposta})


if __name__ == "__main__":
    app.run(debug=True)

