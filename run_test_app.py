from app import WebcomponentApp, db
if __name__ == "__main__":
    webapp = WebcomponentApp(db, "test_app.db")
    webapp.config['WEBCOMPONENT_LIGHT_DOM'] = True
    webapp.runApp()