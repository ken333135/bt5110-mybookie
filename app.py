from src import app, utils
from src.models import Models

if __name__ == '__main__':
    from os import environ
    models = Models()
    # models.dropTables()
    models.createModels()

    # only do seed if db is empty
    # membersCount = models.getMemberCount()
    # app.logger.info(membersCount)
    # if (membersCount==0):
    #     utils.readDbFile("src/data.sql", models)

    utils.readDbFile("src/data.sql", models)

    app.run(host='0.0.0.0', debug=False, port=environ.get("PORT", 5001))
