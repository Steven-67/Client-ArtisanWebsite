from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from .models import Note, Artisan, Client, User, SampleWork
from . import db
import json
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

def save_picture(file):
    if file:
        # Generate a secure filename
        filename = secure_filename(file.filename)
        # Save the file to a specific directory
        file.save(os.path.join(current_app.root_path, 'static', 'profile_pictures', filename))
        # Return the saved file path
        return f"profile_pictures/{filename}"

@views.route('/', methods=['GET', 'POST'])
def artisan_register():
    from .auth import auth  # Import inside the function
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        services = request.form.get('services')
        profile_picture = request.files.get('profile_picture')
        description = request.form.get('description')
        sample_work_files = request.files.getlist('sample_work')

        # Save the artisan details and files to the database
        user_id = current_user.id
        artisan = Artisan(user_id=user_id, name=name, location=location, services=services, description=description)

        if profile_picture:
            # Save the profile picture file and set the path in the artisan model
            profile_picture_path = save_picture(profile_picture)
            artisan.profile_picture = profile_picture_path

        # Save the sample work files and create SampleWork models
        for file in sample_work_files:
            file_path = save_picture(file)
            sample_work = SampleWork(artisan_id=artisan.id, file_path=file_path)
            db.session.add(sample_work)

        db.session.add(artisan)
        db.session.commit()

        return redirect(url_for('views.client_page'))

    return render_template('artisan_register.html')

@views.route('/', methods=['GET', 'POST'])
@login_required
def client_page():
    if request.method == 'POST':
        note = request.form.get('note')  # Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)  # Providing the schema for the note
            db.session.add(new_note)  # Adding the note to the database
            db.session.commit()
            flash('Note added!', category='success')

    artisans = Artisan.query.all()  # Retrieve all artisans

    return render_template("client_page.html", user=current_user, artisans=artisans)

@views.route('/', methods=['GET', 'POST'])
@login_required
def artisan_page():
    if request.method == 'POST':
        note = request.form.get('note')  # Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)  # Providing the schema for the note
            db.session.add(new_note)  # Adding the note to the database
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("artisan_page.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # This function expects a JSON from the INDEX.js file
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
