from flask import Blueprint,request,render_template, \
				  flash, session, redirect, url_for
import requests

mod_vi = Blueprint('volume_indicator',__name__,'/volumes_meta')

@mod_vi.route('/<interval>/<symbol>/')
def volumes(interval,symbol):
