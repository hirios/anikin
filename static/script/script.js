//  

var imagem_html = document.getElementsByClassName('img-pag');
var imagens = [];
var total_de_imagens = imagem_html.length - 1;
var cont = 0;

for (var i = 0; i < imagem_html.length; i++) {
    imagens.push(imagem_html[i].getAttribute('data-img-pag'))
    }

function fpassar(){
    if (cont < total_de_imagens){
        cont += 1;
        document.getElementById('img-infocus').setAttribute('src', imagens[cont]);
    }
}

function fvoltar(){
    if (cont > 0) {
        cont -= 1;
        document.getElementById('img-infocus').setAttribute('src', imagens[cont]);
    }
}
