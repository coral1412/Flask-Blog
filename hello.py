from flask import Flask,render_template,session,redirect,url_for,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required


app=Flask(__name__)
manager=Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)
app.config['SECRET_KEY']="haha"

#@app.route('/')
#def index():
##    return '<h1>Hello World</h1>'
#    return render_template('index.html',current_time=datetime.utcnow())

#@app.route('/',methods=['GET','POST'])
#def index():
#    name=None
#    form=NameForm()
#    if form.validate_on_submit():
##        name=form.name.data
##        form.name.data=''
##        session['name']=form.name.data
#        old_name=session.get('name')
#        if old_name is not None and old_name !=form.name.data:
#            flash('Looks like you have changed your name!')
#        session['name']=form.name.data
#        return redirect(url_for('index'))
#    return render_template('index.html',form=form,name=session.get('name'))
@app.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        old_name=session.get('name')
        if old_name is not None and old_name !=form.name.data:
            flash('Looks like you have changed your name!')
        session['name']=form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'))

@app.route('/user/<name>')
def  user(name):
#    return '<h1>Hello,%s!</h1>' % name
    return render_template('user.html',name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"),500


class NameForm(Form):

    name=StringField('what is your name?',validators=[Required()])
    submit=SubmitField('Submit')


if __name__=='__main__':
    manager.run()
