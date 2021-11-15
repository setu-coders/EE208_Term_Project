import SearchFiles_img as _imgsearch
directory, searcher, analyzer = _imgsearch.init_search()
command = input("command: ")
docs = _imgsearch.get_search_res(command,50,searcher,analyzer)
print(docs)