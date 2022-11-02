from src import app, utils
from src.models import Models

if __name__ == '__main__':
    from os import environ
    models = Models()
    models.createModels()
    utils.readDbFile("src/data_test.sql", models)
    app.run(host='0.0.0.0', debug=True, port=environ.get("PORT", 5001))
