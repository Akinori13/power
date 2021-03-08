SERVER = {
    'host': 'localhost',
    'port': 8080,
    'servername': 'power',
    'listen_backlog': 5, # 接続要求を保持するキューの最大値
    'bufsize': 4096, # 一度に受信するデータの最大値
    'document_root': "www",
    'is_dynamic': True, # 動的サーバか。
    'entry_point': 'index', # 動的サーバの時のすべての入り口
}