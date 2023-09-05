var div_dos_h3 = document.getElementById('div_dos_h3')
var botao_contagem_chamar = document.getElementById('botao_contagem_chamar')
var h3_botao = document.getElementById('h3_botao')
var dados;

function requisicaolistadechamadapacientes() {
    
    fetch('http://192.168.1.70:5000/pegarrankingenomedalistadechamadapacientes').then(response => response.json())
    .then(data => {
        dados = data;
        RederizarDadosComoH3(data)
})
}

requisicaolistadechamadapacientes();


function RederizarDadosComoH3(data) {

    for (var i = 0; i < data.length; i++) {

        var elementonovonome = document.createElement('h3');
        var elementonovoranking = document.createElement('h3');
        var elementonovodiv = document.createElement('div')

        var textonome = dados[i][1]
        var textoranking = dados[i][0]

        elementonovonome.textContent = textonome
        elementonovoranking.textContent = textoranking

        elementonovodiv.appendChild(elementonovonome)
        elementonovodiv.appendChild(elementonovoranking)

        elementonovodiv.style.backgroundColor = 'gray'
        elementonovodiv.style.display = 'flex'
        elementonovodiv.style.flexDirection = 'row'
        elementonovodiv.style.marginBottom = '10px'
    
        elementonovoranking.style.marginLeft = '30px'

        div_dos_h3.appendChild(elementonovodiv)
}

}


var indiceAtual = 0
var listapacientesparadeletar = [];
function mostrarProximoNumero(){
    if (indiceAtual < dados.length){
        h3_botao.textContent =  dados[indiceAtual][1]
        listapacientesparadeletar.push(dados[indiceAtual][1])
        indiceAtual++;
        console.log(h3_botao.textContent)
    }else{

        dados = {
            listaparadeletar: listapacientesparadeletar
        }
        h3_botao.textContent = 'FIM, Deletando'
        fetch('http://192.168.1.70:5000/deletarpacientesjaconsultadospelomedico', {
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

    }}
