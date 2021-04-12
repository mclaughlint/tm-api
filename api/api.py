import os
import connexion

CONF_DIR = os.getcwd() + '/conf'
print(CONF_DIR)

# initialize app
app = connexion.App(__name__, specification_dir='./')

# get endpoint config
app.add_api(f'{CONF_DIR}/swagger.yml')


if __name__ == '__main__':
    app.run(debug=True)
