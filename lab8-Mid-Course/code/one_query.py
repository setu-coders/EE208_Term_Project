import SearchFiles_zhCN
directory, searcher, analyzer = SearchFiles_zhCN.init_search()
command = input("command: ")
docs = SearchFiles_zhCN.get_search_res(command,searcher,analyzer)
print(docs)