"""
Entrypoint file to start API
"""
import config


def create_app():
    """
    Initialize flask app
    :return:
    """
    connex_app = config.connex_app
    connex_app.add_api('swagger.yml')  # get endpoint config

    return connex_app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
