from flask import Flask, request, render_template
import query
from query.query import search_query

app = Flask(__name__)


@app.route("/")
def main():
    return "<p>Hello World! To search chat histories, go to /search</p>"


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET' and request.args:
        query = request.args.get('query')
        advanced_search_mode = request.args.get('advanced_search_mode')
        naive_data = search_query(query)
        advanced_data = None
        if advanced_search_mode == 'term_at_a_time':
            advanced_data = search_query(query, matched_mode='term_at_a_time')
        elif advanced_search_mode == 'BM25':
            advanced_data = search_query(query, matched_mode='BM25')
        data = {'query_string': query,
                'naive_results': naive_data,
                'advanced_results': advanced_data}
        return render_template('search.html', data=data)
    return render_template('search.html')


if __name__ == '__main__':
    app.run()
