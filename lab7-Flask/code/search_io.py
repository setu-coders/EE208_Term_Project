# SJTU EE208

from flask import Flask, redirect, render_template, request, url_for
import SearchFiles_zhCN

app = Flask(__name__)
directory = ""
searcher = 0
analyzer = 0

@app.route('/form', methods=['POST', 'GET'])
def bio_data_form():
    if request.method == "POST":
        command = request.form['command']
        return redirect(url_for('search_results', command=command))
    return render_template("search_bar.html")


@app.route('/search_results', methods=['GET'])
def search_results():
    global searcher,analyzer
    command = request.args.get('command')
    docs = SearchFiles_zhCN.get_search_res(command,searcher,analyzer)
    return render_template("search_results.html", command = command,docs = docs)



if __name__ == '__main__':
    directory, searcher, analyzer = SearchFiles_zhCN.init_search()
    app.run(debug=True, port=8080)
    
