def get_hostandport(
    app_config: dict = None,
    host='localhost',
    port=8080
) -> [str, int]:
    if app_config:
        host = app_config.get('host')
        port = app_config.get('port')
    return host, port
