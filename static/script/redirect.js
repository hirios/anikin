// REDIRECIONA PARA UMA LISTA DE CAPITULOS

$('.select_anime').click(function () {
    var url = $(this).attr('data-href');
    var dados = {'manga_url': url};
    $.ajax({
        type: 'POST',
        url: '/chapters',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(dados),
        success: function(content) {
            $('body').html(content);
            console.log('ok');  
        }
    });
    return false; 
});


// REDIRECIONA PARA A PAGINA REFERENTE A UM CAPITULO

$('.redic-cap').click(
    function () {
        var chapter_string = $(this).text();
        var dados = {'CAP_URL': MANGA_URL + '/' + chapter_string};
        $.ajax({
            type: 'POST',
            url: '/pages',
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(dados),
            cache: false,
            success: function(content) {
                window.location.href = '/pages'
                console.log('yes');
            }
        });
    return false; 
});


// VOLTA PARA A PAGINA DE PESQUISA
$('#link-voltar').click(
    function(){
        window.location.href = '/'
    }
)