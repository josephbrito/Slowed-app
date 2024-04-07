from flask import Flask, render_template, request, send_file, abort
from main import main
from youtube import DownloadVideo

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/load', methods=['POST'])
def loadsong():
    if request.method == 'POST':
        file = request.files['file_song']
        dst = f"./songs/{file.filename}"
        file.save(dst)
        song_path_slowed = main(dst)

        if(song_path_slowed):
            return send_file(song_path_slowed, as_attachment=True, mimetype='audio/mpeg')
        else:
            abort(500)
    return abort(400)

@app.route('/load/youtube', methods=['POST'])
def loadUrl():
    try:
        if request.method == 'POST':
            url = request.form['yt_url']
            path_song_youtube = DownloadVideo(url)
            if path_song_youtube:
                song_path_slowed = main(path_song_youtube)

                if song_path_slowed:
                    return send_file(song_path_slowed, as_attachment=True, mimetype='audio/mpeg', download_name=song_path_slowed.split('/')[-1])
    except Exception as e:
        print('An error ocurred')
        print(e)
        abort(500)

if __name__ == '__main__':
   app.run(debug=True)