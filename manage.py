'''
This file will be excuted by flask run
This will spawn one instance of the app
'''


from application import create_app

app = create_app()
