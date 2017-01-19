from flask import Flask,render_template,session,redirect,url_for,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import os
from flask_mail import Mail,Message

basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
manager=Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)


app.config['MAIL_SERVER']='smtp.exmail.qq.com'
app.config['MAIL_PORT']=465
#app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX']='[Flasky]'
app.config['FLASKY_MAIL_SENDER']='gyc1412@163.com'
app.config['FLASKY_ADMIN']=os.environ.get('FLASKY_ADMIN')
mail=Mail(app)

app.config['SECRET_KEY']="haha"
app.config['SQLALCHEMY_DATABASE_URI']='mysql://flasky:flasky@654321@192.168.100.100:3306/flasky'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICANTS']=True

db=SQLAlchemy(app)


def sender_mail(to,subject,template,**kwargs):
    msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body=render_template(template+'.txt',**kwargs)
    msg.body=render_template(template +'.html',**kwargs)
    msg.html=render_template(template +'.html',**kwargs)
    mail.send(msg)


@app.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        #old_name=session.get('name')
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            session['known']=False
            if app.config['FLASKY_ADMIN']:
                send_mail(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
    else:
        session['known']=True
        session['name']=form.name.data
        return redirect(url_for('index'))
        #if old_name is not None and old_name !=form.name.data:
        #    flash('Looks like you have changed your name!')
        #session['name']=form.name.data
        #return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))

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


#flask_wtf
class NameForm(Form):

    name=StringField('what is your name?',validators=[Required()])
    submit=SubmitField('Submit')


#databases
class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    users=db.relationship('User',backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))


    def __repr__(self):
        return '<User %r>' % self.username


if __name__=='__main__':
    manager.run()
