import config

connex_app = config.connex_app

connex_app.add_api("swagger.yml")

connex_app = connex_app.app

if __name__ == '__main__':
    connex_app.run(debug=True)
