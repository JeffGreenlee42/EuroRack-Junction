from flask_app import app
from flask_app.controllers import controller_users
from flask_app.controllers import controller_modules

app.config['UPLOAD_DIRECTORY'] = "flask_app/static/images/uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif']

app.secret_key = "py is life"

if __name__ == "__main__":
    app.run(port=5001, debug=True)