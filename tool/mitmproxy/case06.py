# 得到上的所有电子书

import json

def response(flow):
    url = 'https://entree.igetget.com/search/v2/document/searchbytype'
    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        # print(data)q
        books = data['c']['list']
        for book in books:
            print(book)
            # title = book.get('title')
            # cover = book.get('detail').get('cover')
            # price = book.get('detail').get('price')
            # ebook = book.get('detail').get('ebook')
            # print(title, cover, price, ebook)