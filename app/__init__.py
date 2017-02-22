from flask import Flask,render_template

app = Flask(__name__)




from app.mod_options.controllers import mod_opt as opt_module
from app.mod_volume_indicator.controllers import mod_vi as vi_module

app.register_blueprint(opt_module)
app.register_blueprint(vi_module)