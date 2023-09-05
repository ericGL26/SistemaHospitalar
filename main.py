import cmath
import threading
import time
import mysql.connector
import sqlite3
# Conecte-se ao banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123123",
    port="3606",
    database="sistemahospitalar"
)
print(mydb)
con = mydb
c = mydb.cursor(buffered=True)
parar_event = threading.Event()

import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS



#CODIGO PARA ATUALIZAR O RANKING A CADA 20 MIN
def atualizar(sets, tables, where=None):
    c = mydb.cursor()
    query = "UPDATE " + tables
    query = query + " SET " + ",".join([field + " = '" + str(value) + "'" for field, value in sets.items()])
    if (where):
        query = query + " WHERE " + where
    c.execute(query)
    mydb.commit()

def atualizar_ranking():
    while True:
        cursor = mydb.cursor()
        listadeidseranking = []
        cursor.execute("SELECT * FROM triagem")
        valorestriagem = cursor.fetchall()

        # ADICIONANDO VALORES RANKING E ID DE CADA PESSOA EM SUBSLISTA
        for i in valorestriagem:
            ranking = i[6]
            id = int(i[0])
            sublista = []
            sublista.append(id)
            sublista.append(ranking)
            listadeidseranking.append(sublista)

        # VERIFICAÇÃO DE VALOR DE RANKING
        for i in listadeidseranking:
            idi = i[0]
            rankingi = int(i[1])
            if rankingi < 100:
                atualizar({"ranking": rankingi + 1}, "triagem", "idtriagem = " + str(idi))

        time.sleep(2)  # Espera por 2 segundos antes da próxima execução

# Inicie a função atualizar_ranking() em uma thread separada
thread_ranking = threading.Thread(target=atualizar_ranking)
thread_ranking.daemon = True  # Encerrará a thread quando o programa principal for encerrado
thread_ranking.start()







app = Flask(__name__)
CORS(app)
#COMECANDO CODIGO PARA CADASTRAR PACIENTE
@app.route('/cadastrarpaciente', methods=['POST'])
def cadastrar():
    try:
        c = mydb.cursor()
        dadosfront = request.get_json()
        nome = dadosfront['nome']
        cpf = dadosfront['cpf']
        rg = dadosfront['rg']
        endereco = dadosfront['endereco']
        # Use prepared statements para evitar SQL Injection
        query = "INSERT INTO pacientes (nomepaciente, cpfpaciente, rgpaciente, enderecopaciente) VALUES (%s, %s, %s, %s)"
        values = (nome, cpf, rg, endereco)

        c.execute(query, values)
        mydb.commit()

        return jsonify({"message": "Paciente cadastrado com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)})

#AQUI ACABA O CODIGO DE CADASTRAR O PACIENTE

#AQUI COMECA O CODIGO DE CADASTRAR NA TRIAGEM
@app.route('/triagem', methods=["POST"])
def insert():
    try:
        c = mydb.cursor()
        dadosfront = request.get_json()
        sentimento = dadosfront['sintomasSelecionados']
        peso = dadosfront['peso']
        altura = dadosfront['altura']
        sexo = dadosfront['sexo']
        alergias = dadosfront['alergias']
        nome = dadosfront['nome']
        idade = dadosfront['idade']
        # TRANSFORMANDO O SENTIMENTOS EM NUMERO PARA FACILITAR
        sintomas = json.loads(sentimento)
        mapeamento = {
    'Dor no peito': {'codigo': 1, 'gravidade': 15},
    'Falta de ar': {'codigo': 2, 'gravidade': 10},
    'Dor abdominal': {'codigo': 3, 'gravidade': 20},
    'Tosse persistente': {'codigo': 4, 'gravidade': 15},
    'Febre alta': {'codigo': 5, 'gravidade': 25},
    'Fadiga': {'codigo': 6, 'gravidade': 10},
    'Dores musculares': {'codigo': 7, 'gravidade': 15},
    'Dor de cabeca intensa': {'codigo': 8, 'gravidade': 20},
    'Tontura': {'codigo': 9, 'gravidade': 15},
    'Vomitos frequentes': {'codigo': 10, 'gravidade': 20},
    'Diarreia persistente': {'codigo': 11, 'gravidade': 15},
    'Hemorragia nasal': {'codigo': 12, 'gravidade': 10},
    'Sensacao de desmaio': {'codigo': 13, 'gravidade': 20},
    'Dificuldade para engolir': {'codigo': 14, 'gravidade': 15},
    'Inchaco nas pernas': {'codigo': 15, 'gravidade': 10},
    'Dor na garganta': {'codigo': 16, 'gravidade': 15},
    'Perda de peso inexplicada': {'codigo': 17, 'gravidade': 20},
    'Sangramento nas gengivas': {'codigo': 18, 'gravidade': 10},
    'Visao turva': {'codigo': 19, 'gravidade': 15},
    'Falta de apetite': {'codigo': 20, 'gravidade': 10},
    'Dor nas costas': {'codigo': 21, 'gravidade': 15},
    'Sensacao de queimacao ao urinar': {'codigo': 22, 'gravidade': 15},
    'Febre baixa': {'codigo': 23, 'gravidade': 10},
    'Coceira intensa na pele': {'codigo': 24, 'gravidade': 15},
    'Feridas que nao cicatrizam': {'codigo': 25, 'gravidade': 20},
    'Frequencia urinaria aumentada': {'codigo': 26, 'gravidade': 15},
    'Desorientacao': {'codigo': 27, 'gravidade': 20},
    'Dor no ouvido': {'codigo': 28, 'gravidade': 15},
    'Fraqueza muscular': {'codigo': 29, 'gravidade': 15},
    'Sensacao de formigamento': {'codigo': 30, 'gravidade': 15},
    'Rigidez no pescoco': {'codigo': 31, 'gravidade': 15},
    'Inchaco abdominal': {'codigo': 32, 'gravidade': 10},
    'Sangramento retal': {'codigo': 33, 'gravidade': 15},
    'Ansiedade intensa': {'codigo': 34, 'gravidade': 20},
    'Dor nos olhos': {'codigo': 35, 'gravidade': 15},
    'Visao dupla': {'codigo': 36, 'gravidade': 15},
    'Dor no peito ao respirar': {'codigo': 37, 'gravidade': 25},
    'Sintomas neurologicos': {'codigo': 38, 'gravidade': 20},
    'Nausea persistente': {'codigo': 39, 'gravidade': 15},
    'Ronco frequente': {'codigo': 40, 'gravidade': 10},
    'Dor na panturrilha': {'codigo': 41, 'gravidade': 15},
    'Hematomas inexplicados': {'codigo': 42, 'gravidade': 15},
    'Pele amarelada': {'codigo': 43, 'gravidade': 15},
    'Suores noturnos': {'codigo': 44, 'gravidade': 10},
    'Sangramento nas articulacoes': {'codigo': 45, 'gravidade': 15},
    'Feridas nos labios ou boca': {'codigo': 46, 'gravidade': 15},
    'Perda de audicao': {'codigo': 47, 'gravidade': 15},
    'Tremores': {'codigo': 48, 'gravidade': 15},
    'Queda de cabelo excessiva': {'codigo': 49, 'gravidade': 10},
    'Sangramento no ouvido': {'codigo': 50, 'gravidade': 15},
    'Sangramento nos olhos': {'codigo': 51, 'gravidade': 15},
    'Dor durante a relacao sexual': {'codigo': 52, 'gravidade': 20},
    'Tontura ao levantar': {'codigo': 53, 'gravidade': 15},
    'Sangramento apos a menopausa': {'codigo': 54, 'gravidade': 20},
    'Dor na regiao lombar': {'codigo': 55, 'gravidade': 15},
    'Sangramento nas unhas': {'codigo': 56, 'gravidade': 15},
    'Alteracoes de humor extremas': {'codigo': 57, 'gravidade': 20},
    'Dor ao urinar': {'codigo': 58, 'gravidade': 15},
    'Alteracoes na voz': {'codigo': 59, 'gravidade': 15},
    'Dor no flanco': {'codigo': 60, 'gravidade': 15},
    'Pele palida': {'codigo': 61, 'gravidade': 10},
    'Inchaco nos pes': {'codigo': 62, 'gravidade': 10},
    'Sangramento nas nadegas': {'codigo': 63, 'gravidade': 15},
    'Tremores nas maos': {'codigo': 64, 'gravidade': 15},
    'Palidez da pele': {'codigo': 65, 'gravidade': 10},
    'Dificuldade para engolir alimentos solidos': {'codigo': 66, 'gravidade': 15},
    'Sangramento no estomago': {'codigo': 67, 'gravidade': 20},
    'Dor nas articulacoes': {'codigo': 68, 'gravidade': 15},
    'Sensacao de queimacao na pele': {'codigo': 69, 'gravidade': 15},
    'Espasmos musculares': {'codigo': 70, 'gravidade': 15},
    'Visao embacada': {'codigo': 71, 'gravidade': 15},
    'Secrecao nasal persistente': {'codigo': 72, 'gravidade': 10},
    'Aftas frequentes': {'codigo': 73, 'gravidade': 15},
    'Perda de equilibrio': {'codigo': 74, 'gravidade': 15},
    'Sensacao de ouvidos tampados': {'codigo': 75, 'gravidade': 15},
    'Inchaco nas maos': {'codigo': 76, 'gravidade': 10},
    'Sangramento nas axilas': {'codigo': 77, 'gravidade': 15},
    'Hemorragia nas gengivas': {'codigo': 78, 'gravidade': 10},
    'Dor no quadril': {'codigo': 79, 'gravidade': 15},
    'Perda de memoria': {'codigo': 80, 'gravidade': 20},
    'Tremores nas pernas': {'codigo': 81, 'gravidade': 15},
    'Batimento cardiaco irregular': {'codigo': 82, 'gravidade': 25},
    'Feridas nas costas': {'codigo': 83, 'gravidade': 15},
    'Visao de tunel': {'codigo': 84, 'gravidade': 15},
    'Dor nas costelas': {'codigo': 85, 'gravidade': 15},
    'Dificuldade em se concentrar': {'codigo': 86, 'gravidade': 20},
    'Perda de visao periferica': {'codigo': 87, 'gravidade': 20},
    'Hemorragia na pele': {'codigo': 88, 'gravidade': 15},
    'Dor no calcanhar': {'codigo': 89, 'gravidade': 15},
    'Dor na palma da mao': {'codigo': 90, 'gravidade': 15},
    'Pele seca e escamosa': {'codigo': 91, 'gravidade': 10},
    'Inchaco no rosto': {'codigo': 92, 'gravidade': 10},
    'Dor nas nadegas': {'codigo': 93, 'gravidade': 15},
    'Sensacao de queimacao no estomago': {'codigo': 94, 'gravidade': 20},
    'Sangramento no nariz': {'codigo': 95, 'gravidade': 10},
    'Coceira nos olhos': {'codigo': 96, 'gravidade': 15},
    'Feridas nos dedos dos pes': {'codigo': 97, 'gravidade': 15},
    'Dor no pescoco': {'codigo': 98, 'gravidade': 15},
}

        listadesentimentos = []
        listadegravidade = []
        for sintoma in sintomas:
            if sintoma in mapeamento:
                numeros = mapeamento[sintoma]["codigo"]
                gravidade = mapeamento[sintoma]["gravidade"]
                listadegravidade.append(gravidade)
                listadesentimentos.append(numeros)
        json_listadesentimentos = json.dumps(listadesentimentos)
        #DEFININDO O RANKING AUTOMATICAMENTE
        ranking = sum(listadegravidade)

        #ENVIANDO OS DADOS PARA O BANCO
        query = "INSERT INTO triagem (sentimento, peso, altura, sexo, alergias, ranking, nome, idade) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (json_listadesentimentos, peso, altura, sexo, alergias, ranking, nome, idade)

        c.execute(query, values)
        mydb.commit()


        return jsonify({"message": "Paciente cadastrado com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)})
#AQUI ACABA O CODIGO DE CADASTRAR NA TRIAGEM



@app.route('/pegarlistadepacientescadastrados')
def select():
    comando = f'SELECT * FROM listadechamadatriagem'
    c.execute(comando)
    mydb.commit()
    resultado = c.fetchall()
    return jsonify(resultado)


@app.route('/deletarpacientesjaconsultadospelomedico', methods=['DELETE'])
def deletarpacientesjaconsultadospelomedico():
    dadosfront = request.get_json()
    listaparadeletar = dadosfront["listaparadeletar"]
    nomes_formatados = ', '.join(map(str, listaparadeletar))
    try:
        table = ('listadeatendimentos')  # Nome da tabela
        print(table)
        # Construir a query DELETE
        query = f"DELETE FROM listadeatendimentos WHERE nome IN ({', '.join(['%s'] * len(listaparadeletar))})"
        querydois = f"DELETE FROM triagem WHERE nome IN ({', '.join(['%s'] * len(listaparadeletar))})"
        querytres = f"DELETE FROM listadechamadatriagem WHERE nome IN ({', '.join(['%s'] * len(listaparadeletar))})"
        values = tuple(listaparadeletar)
        # Executar a query
        c.execute(query, values)
        c.execute(querydois, values)
        c.execute(querytres, values)
        con.commit()
        return jsonify({'mensagem': 'Registro deletado com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)})


@app.route('/pegarrankingenomedalistadechamadapacientes')
def selecionar():
    comando = f'SELECT ranking, nome FROM listadeatendimentos order by ranking desc'
    c.execute(comando)
    mydb.commit()
    resultado = c.fetchall()
    return jsonify(resultado)

#APAGANDO USUARIO JA CHAMADO
@app.route('/deletarpacientesatendidos', methods=['DELETE'])
def deletarpacientes():
    dadosfront = request.get_json()
    listaidparadeletar = dadosfront["listaidparadeletar"]
    ids_formatados = ', '.join(map(str, listaidparadeletar))
    try:
        table = ('listadechamadatriagem')  # Nome da tabela
        print(table)
        # Construir a query DELETE
        query = f'DELETE FROM listadechamadatriagem WHERE id IN ({ids_formatados})'
        # Executar a query
        c.execute(query)
        con.commit()
        return jsonify({'mensagem': 'Registro deletado com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)})


app.run(host="0.0.0.0")
#ENCERRAMENTO DA API

