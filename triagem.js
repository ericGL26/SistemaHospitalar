var sintomasSelecionados = []
function AdicionarSintomasSelecionadosEmUmaLista() {

    event.preventDefault()
    var checkboxes = document.getElementsByName('sintoma');
    sintomasSelecionados = [];

    for (var i = 0; i < checkboxes.length; i++) {

        if (checkboxes[i].checked) {
            sintomasSelecionados.push(checkboxes[i].value);
        }

    }
}


function EnviarDados() {
    
    var input_nome = document.getElementById('input_nome').value;
    var input_peso = document.getElementById('input_peso').value;
    var input_altura = document.getElementById('input_altura').value;
    var input_sexo = document.getElementById('input_sexo').value;
    var input_alergia = document.getElementById('input_alergia').value;
    var input_nome = document.getElementById('input_nome').value;
    var botao_enviar = document.getElementById('botao_enviar');
    var input_escolha_problema = document.getElementById('input_escolha_problema')
    var opcoesinput = document.getElementById('opcoes');
    var ranking = "13";
    var input_idade = document.getElementById('input_idade').value;


    AdicionarSintomasSelecionadosEmUmaLista();
    
    var linkapi = 'http://192.168.1.70:5000/triagem'

    var sintomas = sintomasSelecionados
    var DadosParaEnviar = {
        sintomasSelecionados: JSON.stringify(sintomas),
        peso: input_peso,
        altura: input_altura,
        sexo: input_sexo,
        alergias: input_alergia,
        nome: input_nome,
        ranking: ranking,
        idade: input_idade
    };
    console.log(DadosParaEnviar)
    const configuracaoDaSolicitacao = {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json', 
        },
        body: JSON.stringify(DadosParaEnviar) 
    };
    
    fetch(linkapi, configuracaoDaSolicitacao)
        .then(response => {
            if (!response.ok) {
                console.log('Algo de errado na resposta')
            }
            return response.json();
        }).then(data => {
            console.log(data)
        })
        
}