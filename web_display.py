from flask import Flask, Response, render_template, request
from app.search_engine import SearchEngine
from app.search_engine2 import SearchEngine2

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home_page.html')


@app.route('/page-query', methods=['POST'])
def results():
    search_engine = SearchEngine()
    search_engine2 = SearchEngine2()
    search_query = request.form.get('search_query')
    if search_query.find(" ") != -1: #search engine của Duy, search cụm từ
        results_list = search_engine2(search_query)
        total_results = 0
        for result in results_list:
            total_results += result[1]

        msg = f'{total_results} results total'

        if len(results_list) == 0:
            msg = 'There is no page with this content'

        return render_template('page-query2.html', search_query=search_query, content=results_list, msg=msg)

    else: #search engine của Triết, search 1 từ hoặc nhiều từ ngăn cách dấu phẩy
        results_list = search_engine(search_query)
        count = 0  # đếm tổng result vì mỗi text có result của riêng nó
        for b in results_list:
            for c in iter(b.splitlines()):
                if str(c).startswith("found "):  # có format là "found x results:....."
                    c = c.split()
                    count += int(c[1])
        msg = str(count) + " results total"
        if len(results_list) == 0:
            msg = 'There is no page with this content'

        content = []
        for b in results_list:
            content2 = []
            b = b.splitlines()
            for c in b:
                content2.append(c)
            content.append(
                content2)  # tạo tensor kiểu [[a,b,c],[d,e,f]...] vì chèn <br> vào string html display ko xuống dòng

        return render_template('page-query.html', search_query=search_query, content=content, msg=msg)




if __name__ == '__main__':
    app.run(debug=True)