var botao_enviar = document.getElementById('botao_enviar')
var linkapi = 'http://192.168.1.70:5000/cadastrarpaciente'

//ENVIANDO OS DADOS DO CADASTRO DO PACIENTE PARA A API
botao_enviar.addEventListener('click', function(){

    var input_nome = document.getElementById('input_nome').value
    var input_cpf = document.getElementById('input_cpf').value
    var input_rg = document.getElementById('input_rg').value
    var input_endereco = document.getElementById('input_endereco').value

    var data = {
        nome: input_nome,
        cpf: input_cpf,
        rg: input_rg,
        endereco: input_endereco
    }
    
    var requestoptions = {
        method: 'POST',
        headers: {
            'content-type': 'application/json'
        },
        body: JSON.stringify(data)
    };
    
    fetch(linkapi, requestoptions)
    .then(response => response.json())
    .then(response => {
        console.log(response)
    })

})

//simnaodsd