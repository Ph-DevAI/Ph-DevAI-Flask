# app.py - Flask app style Canva avec gestion admin, projets et formations
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# ----- Config Flask -----

app = Flask(__name__)

# Clé secrète pour les sessions et la sécurité
# En production, SECRET_KEY sera lu depuis la variable d'environnement
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key')

# Base de données
# En production, DATABASE_URL sera fourni par Heroku ou Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///users.db')

# Dossier pour les fichiers uploadés
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialisation de l'ORM
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ----- Modèles -----
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    last_login = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)
    projects = db.relationship('Project', backref='owner', cascade="all, delete-orphan")
    subscriptions = db.relationship('Subscription', backref='user', cascade="all, delete-orphan")

class ProjectImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    filename = db.Column(db.String(150), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

# 🔗 Ajouter la relation dans Project
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(150))
    status = db.Column(db.String(50))  # Exemple : "En cours", "Terminé"
    description = db.Column(db.Text)
    image = db.Column(db.String(150))  # image principale
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relation pour plusieurs images
    images = db.relationship('ProjectImage', backref='project', cascade="all, delete-orphan")

class Formation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    duration = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    subscriptions = db.relationship('Subscription', backref='formation', cascade="all, delete-orphan")

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    formation_id = db.Column(db.Integer, db.ForeignKey('formation.id'))
    email = db.Column(db.String(150))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 👇 Nouveau modèle pour compter les visiteurs
class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ----- Routes publiques -----
@app.route('/')
def home():
    # Enregistrer un nouveau visiteur
    visitor = Visitor()
    db.session.add(visitor)
    db.session.commit()
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Identifiants incorrects.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Nom d\'utilisateur déjà pris.')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Compte créé avec succès !')
            return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# ----- Dashboard utilisateur -----
@app.route('/dashboard')
@login_required
def dashboard():
    projets = Project.query.filter_by(user_id=current_user.id).all()
    formations = Formation.query.all()
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', projets=projets, formations=formations, subscriptions=subscriptions, user=current_user)

# ----- Ajouter un projet -----
@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        title = request.form['title']
        status = request.form['status']
        description = request.form['description']

        # Créer le projet principal
        projet = Project(
            user_id=current_user.id,
            title=title,
            status=status,
            description=description
        )
        db.session.add(projet)
        db.session.commit()  # On commit pour avoir l'id du projet

        # Gestion des images multiples
        files = request.files.getlist('images')  # Note : name="images" dans le formulaire
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # Créer une entrée ProjectImage
                img = ProjectImage(project_id=projet.id, filename=filename)
                db.session.add(img)
        db.session.commit()

        flash('Projet ajouté avec succès avec toutes les images !')
        return redirect(url_for('dashboard'))

    return render_template('add_project.html')


# ----- Souscrire à une formation -----
@app.route('/subscribe_formation/<int:formation_id>', methods=['POST'])
@login_required
def subscribe_formation(formation_id):
    formation = Formation.query.get_or_404(formation_id)
    email = request.form.get('email')
    message = request.form.get('message')
    if not email:
        flash("Email requis pour souscrire.")
        return redirect(url_for('dashboard'))
    subscription = Subscription(
        user_id=current_user.id,
        formation_id=formation.id,
        email=email,
        message=message
    )
    db.session.add(subscription)
    db.session.commit()
    flash(f'Souscription à {formation.title} réussie !')
    return redirect(url_for('dashboard'))

# ----- Admin dashboard -----
@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Accès refusé.')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    formations = Formation.query.all()
    projets = Project.query.all()
    
    # 👇 Stats pour Chart.js
    visitor_count = Visitor.query.count()
    projects_status = {
        "En cours": Project.query.filter_by(status="En cours").count(),
        "Terminé": Project.query.filter_by(status="Terminé").count()
    }
    
    return render_template(
        'admin.html',
        users=users,
        formations=formations,
        projets=projets,
        user=current_user,
        visitors_count=visitor_count,
        projects_status=projects_status
    )

# ----- Gestion formations Admin -----
@app.route('/admin/add_formation', methods=['GET', 'POST'])
@login_required
def add_formation():
    if not current_user.is_admin:
        flash('Accès refusé.')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        duration = request.form['duration']
        formation = Formation(title=title, description=description, price=price, duration=duration)
        db.session.add(formation)
        db.session.commit()
        flash('Formation ajoutée avec succès !')
        return redirect(url_for('admin'))
    return render_template('admin_add_formation.html')

@app.route('/admin/update_formation/<int:formation_id>', methods=['GET', 'POST'])
@login_required
def update_formation(formation_id):
    if not current_user.is_admin:
        flash('Accès refusé.')
        return redirect(url_for('dashboard'))
    formation = Formation.query.get_or_404(formation_id)
    if request.method == 'POST':
        formation.title = request.form['title']
        formation.description = request.form['description']
        formation.price = float(request.form['price'])
        formation.duration = request.form['duration']
        db.session.commit()
        flash('Formation mise à jour avec succès !')
        return redirect(url_for('admin'))
    return render_template('admin_update_formation.html', formation=formation)

@app.route('/admin/delete_formation/<int:formation_id>', methods=['POST'])
@login_required
def delete_formation(formation_id):
    if not current_user.is_admin:
        flash('Accès refusé.')
        return redirect(url_for('dashboard'))
    formation = Formation.query.get_or_404(formation_id)
    db.session.delete(formation)
    db.session.commit()
    flash('Formation supprimée avec succès !')
    return redirect(url_for('admin'))

# ----- Modifier projet admin -----
@app.route('/admin/update_project/<int:projet_id>', methods=['GET', 'POST'])
@login_required
def admin_update_project(projet_id):
    if not current_user.is_admin:
        flash('Accès refusé.')
        return redirect(url_for('dashboard'))
    projet = Project.query.get_or_404(projet_id)
    if request.method == 'POST':
        projet.title = request.form['title']
        projet.status = request.form['status']
        projet.description = request.form['description']
        file = request.files.get('image')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            projet.image = filename
        projet.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Projet mis à jour avec succès !')
        return redirect(url_for('admin'))
    return render_template('admin_update_project.html', projet=projet)

# ----- Supprimer une image d'un projet -----
@app.route('/admin/delete_project_image/<int:image_id>', methods=['POST'])
@login_required
def delete_project_image(image_id):
    if not current_user.is_admin:
        flash('Accès refusé.')
        return redirect(url_for('dashboard'))

    img = ProjectImage.query.get_or_404(image_id)
    # Supprimer le fichier du dossier uploads
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    
    db.session.delete(img)
    db.session.commit()
    flash('Image supprimée avec succès !')
    return redirect(url_for('admin_update_project', projet_id=img.project_id))


# ----- Lancer l'app -----
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Vérifier si l'admin existe déjà
        admin_username = "Prince Hilquia"
        admin_password = "@loveofGod123"

        admin_user = User.query.filter_by(username=admin_username).first()
        if not admin_user:
            hashed_password = generate_password_hash(admin_password)
            admin_user = User(username=admin_username, password=hashed_password, is_admin=True)
            db.session.add(admin_user)
            db.session.commit()
            print("Admin créé : Prince Hilquia")
        else:
            print("Admin déjà présent")

    app.run(debug=True)
