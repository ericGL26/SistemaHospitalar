var h3_nome = document.getElementById('h3_nome')
var h3_idade = document.getElementById('h3_idade')
var h3_sexo = document.getElementById('h3_sexo')
var h3_ranking = document.getElementById('h3_ranking')
var h3_sentimento = document.getElementById('h3_sentimento')
var botao_teste = document.getElementById('botao_teste')
var div_dos_inputsid = document.getElementById('div_dos_inputsid')
var numeroaserexibido = document.getElementById('numeroexibido')
var listanomepacientes = [];
var listaidpacientes = []

function pegardadospacientes() {

    fetch('http://192.168.1.70:5000/pegarlistadepacientescadastrados')
    .then(response => {
      if (!response.ok) {
        throw new Error('Não foi possível obter os dados da API');
      }
      return response.json(); // Converte a resposta para JSON
    })
    .then(data => {

      RenderizarDadosDosPacientesComoH3(data)
      
      //ADICIONANDO OS IDS DOS PACIENTES EM UMA LISTA
      listaidpacientes = []
      for (criar = 0; criar < listanomepacientes.length; criar++) {
        listaidpacientes.push(listanomepacientes[criar][0])
}

})}

pegardadospacientes()


function RenderizarDadosDosPacientesComoH3(data) {
  listanomepacientes = data
      for (criarElemento = 0; criarElemento < listanomepacientes.length; criarElemento++) {
        var textoh3 = document.createTextNode(listanomepacientes[criarElemento]);
        var paragrafo = document.createElement('h3');
        paragrafo.style.color = 'white'
        paragrafo.appendChild(textoh3);
        div_dos_inputsid.appendChild(paragrafo)
      }

}


//Mostrar no botao o numero do proximo paciente a ser chamado
var indiceAtual = 0
var listapacientesparadeletar = [];

function MostrarNumeroProximoPacienteNoBotao(){

  //CODIGO PARA MOSTAR O PROXIMO NUMERO A SER EXIBIDO NO BOTAO
  if (indiceAtual < listaidpacientes.length){
    numeroaserexibido.textContent =  listaidpacientes[indiceAtual]
    listapacientesparadeletar.push(listaidpacientes[indiceAtual])
    indiceAtual++;

  }else{

    //DELETANDO OS DADOS DOS PACIENTRES JÁ ATENDIDOS NA TRIAGEM
    dados = {
      listaidparadeletar: listapacientesparadeletar
    }

    fetch('http://192.168.1.70:5000/deletarpacientesatendidos', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dados),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Não foi possível deletar o recurso');
        }
        return response.json();
      })
      .then(data => {
        console.log('Recurso deletado com sucesso', data);
      })
      .catch(error => {
        console.error('Ocorreu um erro:', error);
      });

  }

}