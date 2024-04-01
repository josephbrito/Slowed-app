$('#file').on('change', function(event) {
    if(event.target.value) {
        $('#result').css("display", "block").text(event.target.value.slice(12));
    } else {
        $('#result').text('')
    }
});

$('#year').text( new Date().getFullYear() );

$('#btn-submit').on('click', function(e) {
    e.preventDefault();
    const formData = new FormData();

    const file = $('#file').prop('files')[0];
    const url_youtube = $('#yt_url').val();

    if(!file && !url_youtube) {
        return;
    } else if(file && url_youtube) {
        alert('Escolha somente 1 método!');
        return;
    }
    formData.append('file_song', file);
    formData.append('yt_url', url_youtube);

    $.ajax({
        type: 'post',
        data:formData,
        url: window.location.href + 'load',
        processData: false,
        contentType: false,
        enctype: 'multipart/form-data',
        xhrFields: {
            responseType: 'blob'
        },
        beforeSend:function() {
            $('#loading-screen').css('display', 'flex');
            console.log('Carregando...');
        },
        success: function(res) {
            $('#loading-screen').css('display', 'none');
            console.log('deu certo');

            let url = window.URL.createObjectURL(res);

            let a = document.createElement('a');
            let source = document.createElement('source');
        
            a.classList.add('button')
            a.textContent = 'Download'
            a.href = url;
            a.download = $('#result').text().split('.')[0].replaceAll(' ', '_') + '-slowed_app.mp3'
            $('.button-container').append(a)
            a.click();

            source.setAttribute('src', url)
            
            $('#my-audio').css('display', 'block').append(source);
            window.URL.revokeObjectURL(url);
        },
        error: function(err) {
            $('#loading-screen').css('display', 'none');
            console.log('Algo deu errado: ', err)
        }
    });
});