import config

app = config.connex_app
# get endpoint config
app.add_api(f'swagger.yml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
