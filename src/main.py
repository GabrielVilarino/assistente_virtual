import speech_recognition as sr
import re
import pyttsx3
import random
from datetime import datetime
from fpdf import FPDF

nome_usuario = ''
ASSISTENTE = 'Neiva'
PIADAS = ['Por que os químicos são ótimos em resolver problemas? Porque eles têm todas as soluções!',
          'Por que o desenvolvedor faliu? Porque ele usou todo o seu cache.',
          'Você já ouviu falar do cara que roubou o calendário? Ele pegou 12 meses!',
          'O que ganha o melhor dentista do mundo? Uma pequena placa.',
          'Meus professores me disseram que eu nunca seria muito porque procrastino muito. Eu disse a eles: “Esperem para ver!”',
          'Minha memória ficou tão ruim que realmente me fez perder o emprego. Ainda estou empregado. Só não consigo lembrar onde.',
          'Quando em uma candidatura a emprego perguntam quem deve ser notificado em caso de emergência, sempre escrevo: “Um médico muito bom”.',
          'Por que o médico está sempre calmo? Porque ele tem muitos pacientes.',
          'Por que o livro de matemática parece tão triste? Por causa de todos os seus problemas.',
          'Qual é a comida favorita de um lobisomem? Lobisomens não são reais.',
          'Como chamar um cão mágico? Um Labracadabrador.',
          'Por que os pássaros voam para climas mais quentes no inverno? É muito mais fácil do que caminhar!',
          'Seja como um próton. Sempre seja positivo.',
          'Que tipo de carro o Yoda dirige? Toyoda.',
          'O que o zero diz a um oito? Cinto legal.'
          ]
MESES = ['Janeiro',
         'Fevereiro',
         'Março',
         'Abril',
         'Maio',
         'Junho',
         'Julho',
         'Agosto',
         'Setembro',
         'Outubro',
         'Novembro',
         'Dezembro'
         ]

print("Iniciando Assistente Virtual")

def criar_pdf(lista_itens):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    for item in lista_itens:
        # Se o item for uma string única com itens separados por espaço
        if ' ' in item:
            itens_individual = item.split()
            for subitem in itens_individual:
                pdf.cell(200, 10, txt=subitem, ln=True, align='L')
        else:
            pdf.cell(200, 10, txt=item, ln=True, align='L')

    pdf.output('lista.pdf')

while(True):
    mic = sr.Recognizer()

    with sr.Microphone() as source:
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-20)

        mic.adjust_for_ambient_noise(source)

        try:
            audio = mic.listen(source, timeout=10)
        except sr.WaitTimeoutError:
            engine.say("Já que não quer falar comigo, vou sair")
            engine.runAndWait()
            break

        try:
            frase = mic.recognize_google(audio, language='pt-BR')

            # print(f"Você falou: {frase}")
            if (re.search(r'\b' + 'ajuda' + r'\b', format(frase), re.IGNORECASE)):
                engine.say("Do que você precisa?")
                engine.runAndWait()

            elif (re.search(r'\b' + '(meu\s*nome\s*é|me\s*chamo\s*) ' + r'\b', format(frase), re.IGNORECASE)):
                nome = re.search('meu\s*nome\s*é\s*(.*)',format(frase), re.IGNORECASE)
                if nome is None:
                    nome = re.search('me\s*chamo (.*)',format(frase), re.IGNORECASE)
                nome_usuario = nome.group(1)
                engine.say(f"Olá {nome_usuario}")
                engine.runAndWait()

            elif (re.search(r'\b' + '(seu|teu)\s*nome' + r'\b', format(frase), re.IGNORECASE)):
                engine.say(f"Meu nome é {ASSISTENTE}")
                engine.runAndWait()

            elif (re.search(r'\b' + 'tudo\s*bem\s*(com\s*você|contigo)' + r'\b', format(frase), re.IGNORECASE)):
                engine.say(f"Tudo ótimo, e com você?")
                engine.runAndWait()

            elif (re.search(r'\b' + 'piada' + r'\b', format(frase), re.IGNORECASE)):
                quantidade = len(PIADAS)
                numeracao = random.randint(0, quantidade)
                engine.say(PIADAS[numeracao])
                engine.runAndWait()

            elif (re.search(r'\b' + 'lista' + r'\b', format(frase), re.IGNORECASE)):
                engine.say("Me diga os itens que você quer por na lista")
                engine.runAndWait()
                escrever = True
                itens = []
                while escrever is True:
                    try:
                        audio_itens = mic.listen(source, timeout=10)
                    except sr.WaitTimeoutError:
                        print("Tempo esgotado. Você não está falando.")
                        break
                    item = mic.recognize_google(audio_itens, language='pt-BR')
                    itens.append(item)
                    print(f"Itens: {itens}")
                    engine.say("Itens adicionados. Quer adicionar mais algum?")
                    engine.runAndWait()
                    try:
                        audio_resposta = mic.listen(source, timeout=3)
                        resposta = mic.recognize_google(audio_resposta, language='pt-BR')
                        if re.search(r'\b' + 'sim' + r'\b', resposta, re.IGNORECASE):
                            engine.say("Pode dizer")
                            engine.runAndWait()
                        elif re.search(r'\b' + 'quero' + r'\b', resposta, re.IGNORECASE):
                            engine.say("Pode dizer")
                            engine.runAndWait()
                        elif re.search(r'\b' + 'não' + r'\b', resposta, re.IGNORECASE):
                            break
                        elif re.search(r'\b' + 'terminei' + r'\b', resposta, re.IGNORECASE):
                            break

                    except sr.WaitTimeoutError:
                        print("Lista Finalizada.")
                        break

                criar_pdf(lista_itens=itens)
                engine.say("Lista criada com sucesso")
                engine.runAndWait()

            elif (re.search(r'\b' + '(que|qual)\s*(dia|a\s*data|data)\s*(é|de)\s*hoje' + r'\b', format(frase), re.IGNORECASE)):
                hoje = datetime.now()
                dia = hoje.day
                mes = hoje.month
                ano = hoje.year
                mes_str = MESES[mes-1]
                engine.say(f"Hoje é {dia} de {mes_str} de {ano}")
                engine.runAndWait()

            elif (re.search(r'\b' + 'como\s*eu\s*me\s*chamo' + r'\b', format(frase), re.IGNORECASE)):
                if nome_usuario == '':
                    engine.say(f"Eu não sei, qual o seu nome?")
                    engine.runAndWait()
                else:
                    engine.say(f"Como eu iria me esquecer? Você se chama {nome_usuario}")
                    engine.runAndWait()
        except sr.UnknownValueError:
            print("Algo deu errado!")