from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
from . import db
import json, jsonify



views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user = current_user)

@views.route('/products')
@login_required
def products():
    return render_template("products.html", user = current_user)

@views.post('/notes')
@views.get('/notes')
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')
    
        if len(note) < 1:
            flash("The note cannot be empty", category = "error")
        else:
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("New Note added", category = "success")
    
    return render_template("notes.html", user = current_user)

@views.post('/delete-note')
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})

