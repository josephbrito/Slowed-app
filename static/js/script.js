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

    if(file) {
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
    
                let a_html = `
                <i class="fa-solid fa-download"></i>
                Download
                `;
    
                let a = document.createElement('a');
            
                a.classList.add('button')
                a.insertAdjacentHTML('beforeend', a_html);
                a.href = url;
                a.download = $('#result').text().split('.')[0].replaceAll(' ', '_') + '-slowed_app.mp3'
                $('.button-container').after(a)
                a.click();
            
                window.URL.revokeObjectURL(url);
            },
            error: function(err) {
                console.log(err);
                $('#loading-screen').css('display', 'none');
                $('#error-screen').css('display', 'flex');
    
                setTimeout(() => {
                    $('#error-screen').css('display', 'none');
                }, 3000);
            }
        });
    } else if(url_youtube) {
        console.log('foi pela url');
        $.ajax({
            type: 'post',
            data:formData,
            url: window.location.href + 'load/youtube',
            processData: false,
            contentType: false,
            xhrFields: {
                responseType: 'blob'
            },
            beforeSend:function() {
                $('#loading-screen').css('display', 'flex');
                console.log('Carregando...');
            },
            success: function(res, txt, request) {
                $('#loading-screen').css('display', 'none');
                console.log('deu certo');

                const download_name = request.getResponseHeader('Content-Disposition').split('filename=')[1].replaceAll('"', '');
    
                let url = window.URL.createObjectURL(res);
    
                let a_html = `
                <i class="fa-solid fa-download"></i>
                Download
                `;
    
                if(document.getElementById('btn-download')) {
                    $('#btn-download').remove();
                }

                let a = document.createElement('a');
            
                a.classList.add('button')
                a.id = 'btn-download'
                a.insertAdjacentHTML('beforeend', a_html);
                a.href = url;
                a.download = download_name;
                $('.button-container').after(a)
                a.click();
            
                window.URL.revokeObjectURL(url);
            },
            error: function(err) {
                console.log(err);
                $('#loading-screen').css('display', 'none');
                $('#error-screen').css('display', 'flex');
    
                setTimeout(() => {
                    $('#error-screen').css('display', 'none');
                }, 3000);
            }
        });
    }
    
});