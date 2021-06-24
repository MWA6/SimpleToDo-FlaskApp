from flask import render_template, request, url_for, redirect, flash
from todoApp import app, db
from todoApp.models import User, NotesDB
from todoApp.forms import signUpForm, loginForm, noteForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods=["GET", "POST"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('notes'))
    return render_template("home1.html")


@app.route('/notes', methods=["GET", "POST"])
@login_required
def notes():
    nform = noteForm()
    dnotes = NotesDB.query.filter_by(user_id=current_user.get_id())
    if nform.validate_on_submit():
        text = NotesDB(notes=nform.note.data, creator=current_user)
        db.session.add(text)
        db.session.commit()
        dnotes = NotesDB.query.filter_by(user_id=current_user.get_id())
    
    return render_template("notes.html", title='Notes/Tasks', form=nform, dnotes=dnotes)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('notes'))
    sform = signUpForm()
    if sform.validate_on_submit():
        user = User(username=sform.username.data, password=sform.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! , Login to continue.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=sform)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('notes'))
    lform = loginForm()
    if lform.validate_on_submit():
        user = User.query.filter_by(username=lform.username.data).first()
        if user and (user.password == lform.password.data):
            login_user(user, remember=lform.remember.data)            
            return redirect(url_for('notes'))
        else:
            flash('Login Failed. Check Username and Password!', 'danger')
    return render_template('login.html', title='Log In', form=lform)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/delete/<int:note_id>', methods=['GET', 'POST'])
@login_required
def delete(note_id):
    note = NotesDB.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes'))

@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    newnote = request.form.get("newnote")
    note_id = request.form.get("note_id")
    note = NotesDB.query.get(note_id)
    note.notes = newnote
    note.done = 0
    db.session.commit()
    return redirect(url_for('notes'))

@app.route('/done/<int:note_id>', methods=['GET', 'POST'])
@login_required
def done(note_id):
    note = NotesDB.query.get(note_id)
    note.done = 1
    db.session.commit()
    return redirect(url_for('notes'))
