import os
import sys
import pyinputplus as pyip
import shutil
from appmanager import AppManager


def get_app_info():
    try:
        print('------------------------------------')
        print('How do you want to name your app?')
        name = pyip.inputStr(limit=2).replace(' ', '_')
        print('------------------------------------')
        print('Do you need a database?')
        input_database = pyip.inputMenu(['yes', 'no'], limit=2, numbered=True)
        models = list()
        if input_database == 'yes':
            database = True
            models_bool = True
            while models_bool:
                print('Do you want to add a database table?')
                input_model = pyip.inputMenu(['yes', 'no'], limit=2, numbered=True)
                if input_model == 'yes':
                    model_name = pyip.inputStr('Tablename: ').replace(' ', '_').capitalize()
                    models.append(model_name)
                else:
                    models_bool = False
        else:
            database = False

        blueprint_names = list()
        blueprints_bool = True
        blueprints = False
        print('------------------------------------')
        while blueprints_bool:
            print('Do you want to add a blueprint?')
            blueprint = pyip.inputMenu(['yes', 'no'], limit=2, numbered=True)
            if blueprint == 'yes':
                blueprint_name = pyip.inputStr('Blueprintname: ').replace(' ', '_').lower()
                blueprint_names.append(blueprint_name)
                blueprints = True
            else:
                blueprints_bool = False

        app = AppManager(name, database, models, blueprints, blueprint_names)

    except pyip.RetryLimitException as e:
        print('ERROR: You exceeded the input limit.')
        return sys.exit()

    return app


if __name__ == '__main__':
    app = get_app_info()
    app.create_app()