import functools
from flask import (Blueprint, flash,g,redirect,render_template,request,session,url_for
                   )
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from .templates.kml.randompoints import run as make_kml

bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register',methods=('GET','POST'))
def register():
    if request.method =='POST':
        username =request.form['username']
        password = request.form['password']
        db=get_db()
        error=None
        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?',
                (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute('INSERT INTO user (username,password,ind) VALUES (?,?,0)',
                       (username,generate_password_hash(password))
                       )
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/info',methods=('GET','POST'))
def info():
    db = get_db()
    i=1
    attrs = ['username','id','ind']
    STRING = '<h2>Users</h2>'
    STRING += '<h3>'
    for attr in attrs:
        STRING+= str(attr) + ' | '
    STRING+='</h3>'
    while(i<=30):
        try:
            user = db.execute('SELECT * FROM user WHERE id='+str(i)).fetchone()
            i+=1
            STRING +='<h4>'
            for attr in attrs:
                STRING += str(user[attr]) + '    |     '
            STRING += '</h4>'
        except:
            continue
    attrs = ['author_id','created','response_to','response']
    
    STRING+='<h2>Classifications<h2>'
    i=1
    STRING += '<h3>'
    for attr in attrs:
        STRING+= str(attr) + ' | '
    STRING+='</h3>'


    while(i<=30):
        try:
            user = db.execute('SELECT * FROM classifications WHERE id='+str(i)).fetchone()
            i+=1
            STRING +='<h4>'
            for attr in attrs:
                STRING += str(user[attr]) + '    |     '
            STRING += '</h4>'
        except:
            continue

        
    return(STRING)
    # return render_template('auth/info.html')




@bp.route('/login',methods=('GET','POST'))
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username =?',
            (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'],password):
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('.select'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route("select/next", methods=['GET'])
def change_kml():
    db = get_db()
    error = None
    answer = request.form.get('answer')
    user = db.execute(
        'SELECT * FROM user WHERE username =?',
        (g.user['username'],)).fetchone()
    db.execute('INSERT INTO classifications (author_id,response_to,response) VALUES (?,?,?)',
                        (g.user['username'],g.user['ind'],answer)
                       )
    
    db.execute('UPDATE user SET ind = ind+1 WHERE username =?',
        (g.user['username'],))
    db.commit()
    make_kml(g.user['ind'])
    forward_message = "Next!"
    return render_template('select.html', message=forward_message)


@bp.route('/select')
def select():
    # db = get_db()
    #
    # posts = db.execute(
    #     'SELECT body, created'
    #     ' FROM user  WHERE username =?',
    #     (g.user,)
    # ).fetchone()
    return render_template('select.html')

@bp.route('/')
def index():
    return render_template('index.html')