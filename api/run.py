import config


def create_app():
    connex_app = config.connex_app
    connex_app.add_api(f'swagger.yml')  # get endpoint config
    flask_app = connex_app.app

    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
