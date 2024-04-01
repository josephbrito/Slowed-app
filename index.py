from flask import Flask, render_template, request, send_file, abort
from main import main

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

if __name__ == '__main__':
   app.run(debug=True)