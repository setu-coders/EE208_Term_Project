# SJTU EE208

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route('/form', methods=['POST', 'GET'])
def bio_data_form():
    if request.method == "POST":
        command = request.form['command']
        return redirect(url_for('search_results', command=command))
    return render_template("search_bar.html")


@app.route('/search_results', methods=['GET'])
def search_results():
    
    command = request.args.get('command')

    return render_template("search_results.html", command = command)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
