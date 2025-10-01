#!/usr/bin/env python3
"""
GlobalExam AI - Global Server
=============================
Server global pour contrôler l'accès à l'application depuis n'importe où
"""

from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime, timedelta
import hashlib
import uuid

app = Flask(__name__)

# Base de données simple (fichiers JSON)
USERS_DB = "users.json"
REQUESTS_DB = "requests.json"
LOGS_DB = "logs.json"

def load_data(filename):
    """Charger les données depuis un fichier JSON"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except:
        return {}

def save_data(filename, data):
    """Sauvegarder les données dans un fichier JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Erreur sauvegarde {filename}: {e}")

def log_activity(activity_type, user_id, details=""):
    """Enregistrer une activité"""
    logs = load_data(LOGS_DB)
    log_id = str(uuid.uuid4())
    logs[log_id] = {
        'timestamp': datetime.now().isoformat(),
        'type': activity_type,
        'user_id': user_id,
        'details': details
    }
    save_data(LOGS_DB, logs)

@app.route('/')
def home():
    """Page d'accueil"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GlobalExam AI - Server Status</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            .logo { text-align: center; color: #2c3e50; margin-bottom: 30px; }
            .status { background: #27ae60; color: white; padding: 15px; border-radius: 5px; text-align: center; }
            .info { background: #3498db; color: white; padding: 10px; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">
                <h1>🤖 GlobalExam AI Server 🤖</h1>
                <h2>🌐 Global Access Control System</h2>
            </div>
            <div class="status">
                ✅ Server Online and Ready
            </div>
            <div class="info">
                🔒 Security: Server-controlled access management
            </div>
            <div class="info">
                🎯 Features: Real-time user approval system
            </div>
            <div class="info">
                📊 Status: {{ requests_count }} pending requests
            </div>
            <p><a href="/admin/dashboard">🎛️ Admin Dashboard</a></p>
        </div>
    </body>
    </html>
    """, requests_count=len(load_data(REQUESTS_DB)))

@app.route('/api/auth', methods=['POST'])
def handle_auth():
    """Gérer les demandes d'authentification"""
    try:
        data = request.json
        user_info = data.get('user_info', {})
        user_id = user_info.get('user_id', 'unknown')
        
        # Enregistrer la demande
        requests_db = load_data(REQUESTS_DB)
        request_id = str(uuid.uuid4())
        requests_db[request_id] = {
            'user_info': user_info,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending',
            'user_id': user_id
        }
        save_data(REQUESTS_DB, requests_db)
        
        # Logger l'activité
        log_activity('auth_request', user_id, f"New access request from {user_info.get('system_info', {}).get('computer_name', 'unknown')}")
        
        # Vérifier si déjà approuvé
        users_db = load_data(USERS_DB)
        if user_id in users_db and users_db[user_id].get('approved'):
            user_data = users_db[user_id]
            if datetime.now() < datetime.fromisoformat(user_data.get('expires_at')):
                log_activity('auth_success', user_id, "Existing session valid")
                return jsonify({
                    'access_granted': True,
                    'session_token': user_data['session_token'],
                    'expires_at': user_data['expires_at'],
                    'message': 'Access granted - existing session'
                })
        
        return jsonify({
            'access_granted': False,
            'reason': 'Demande en attente d\'approbation du propriétaire',
            'request_id': request_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/check', methods=['POST'])
def check_session():
    """Vérifier la validité d'une session"""
    try:
        data = request.json
        user_id = data.get('user_id')
        session_token = data.get('session_token')
        
        users_db = load_data(USERS_DB)
        if user_id in users_db:
            user_data = users_db[user_id]
            if (user_data.get('session_token') == session_token and
                user_data.get('approved') and
                datetime.now() < datetime.fromisoformat(user_data.get('expires_at'))):
                
                log_activity('session_check', user_id, "Session valid")
                return jsonify({'session_valid': True})
        
        log_activity('session_check', user_id, "Session invalid")
        return jsonify({'session_valid': False})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/dashboard')
def admin_dashboard():
    """Tableau de bord administrateur"""
    requests_db = load_data(REQUESTS_DB)
    users_db = load_data(USERS_DB)
    logs = load_data(LOGS_DB)
    
    # Trier les demandes par date (plus récentes en premier)
    sorted_requests = sorted(requests_db.items(), 
                           key=lambda x: x[1]['timestamp'], reverse=True)
    
    # Derniers logs
    recent_logs = sorted(logs.items(), 
                        key=lambda x: x[1]['timestamp'], reverse=True)[:10]
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GlobalExam AI - Admin Dashboard</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: #2c3e50; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
            .section { background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
            .request { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .pending { border-left: 5px solid #f39c12; }
            .approved { border-left: 5px solid #27ae60; }
            .denied { border-left: 5px solid #e74c3c; }
            .btn { padding: 10px 15px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }
            .btn-approve { background: #27ae60; color: white; }
            .btn-deny { background: #e74c3c; color: white; }
            .btn-revoke { background: #f39c12; color: white; }
            .stats { display: flex; justify-content: space-around; margin-bottom: 20px; }
            .stat { background: #3498db; color: white; padding: 15px; border-radius: 5px; text-align: center; flex: 1; margin: 0 10px; }
            .log { font-size: 12px; color: #666; margin: 5px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎛️ GlobalExam AI - Admin Dashboard</h1>
                <p>Contrôlez l'accès à votre application depuis n'importe où dans le monde</p>
            </div>
            
            <div class="stats">
                <div class="stat">
                    <h3>{{ pending_count }}</h3>
                    <p>Demandes en attente</p>
                </div>
                <div class="stat">
                    <h3>{{ approved_count }}</h3>
                    <p>Utilisateurs approuvés</p>
                </div>
                <div class="stat">
                    <h3>{{ total_requests }}</h3>
                    <p>Total des demandes</p>
                </div>
            </div>
            
            <div class="section">
                <h2>📋 Demandes d'Accès</h2>
                {% if requests %}
                    {% for request_id, request_data in requests %}
                    <div class="request {{ request_data.status }}">
                        <h3>👤 {{ request_data.user_id }}</h3>
                        <p><strong>Ordinateur:</strong> {{ request_data.user_info.system_info.computer_name if request_data.user_info.system_info else 'Inconnu' }}</p>
                        <p><strong>Système:</strong> {{ request_data.user_info.system_info.system if request_data.user_info.system_info else 'Inconnu' }}</p>
                        <p><strong>Heure:</strong> {{ request_data.timestamp }}</p>
                        <p><strong>Statut:</strong> {{ request_data.status }}</p>
                        
                        {% if request_data.status == 'pending' %}
                        <a href="/admin/approve/{{ request_data.user_id }}" class="btn btn-approve">✅ Approuver</a>
                        <a href="/admin/deny/{{ request_data.user_id }}" class="btn btn-deny">❌ Refuser</a>
                        {% elif request_data.status == 'approved' %}
                        <a href="/admin/revoke/{{ request_data.user_id }}" class="btn btn-revoke">🔒 Révoquer</a>
                        {% endif %}
                    </div>
                    {% endfor %}
                {% else %}
                    <p>Aucune demande d'accès pour le moment.</p>
                {% endif %}
            </div>
            
            <div class="section">
                <h2>📊 Logs Récents</h2>
                {% for log_id, log_data in recent_logs %}
                <div class="log">
                    <strong>{{ log_data.timestamp }}</strong> - {{ log_data.type }} - {{ log_data.user_id }} - {{ log_data.details }}
                </div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    """, 
    requests=sorted_requests,
    recent_logs=recent_logs,
    pending_count=len([r for r in requests_db.values() if r['status'] == 'pending']),
    approved_count=len([u for u in users_db.values() if u.get('approved')]),
    total_requests=len(requests_db)
    )

@app.route('/admin/approve/<user_id>')
def approve_user(user_id):
    """Approuver un utilisateur"""
    users_db = load_data(USERS_DB)
    requests_db = load_data(REQUESTS_DB)
    
    # Créer ou mettre à jour l'utilisateur
    session_token = hashlib.sha256(f"{user_id}{datetime.now().isoformat()}".encode()).hexdigest()
    users_db[user_id] = {
        'approved': True,
        'session_token': session_token,
        'expires_at': (datetime.now() + timedelta(hours=8)).isoformat(),
        'approved_at': datetime.now().isoformat()
    }
    save_data(USERS_DB, users_db)
    
    # Mettre à jour le statut de la demande
    for req_id, req_data in requests_db.items():
        if req_data.get('user_id') == user_id:
            req_data['status'] = 'approved'
    save_data(REQUESTS_DB, requests_db)
    
    log_activity('user_approved', user_id, "Access granted by admin")
    
    return f"""
    <html><body style="font-family: Arial; text-align: center; margin-top: 100px;">
    <h1>✅ Utilisateur Approuvé</h1>
    <p>L'utilisateur <strong>{user_id}</strong> a été approuvé avec succès.</p>
    <p>Session valide pendant 8 heures.</p>
    <a href="/admin/dashboard">← Retour au tableau de bord</a>
    </body></html>
    """

@app.route('/admin/deny/<user_id>')
def deny_user(user_id):
    """Refuser un utilisateur"""
    requests_db = load_data(REQUESTS_DB)
    
    # Mettre à jour le statut de la demande
    for req_id, req_data in requests_db.items():
        if req_data.get('user_id') == user_id:
            req_data['status'] = 'denied'
    save_data(REQUESTS_DB, requests_db)
    
    log_activity('user_denied', user_id, "Access denied by admin")
    
    return f"""
    <html><body style="font-family: Arial; text-align: center; margin-top: 100px;">
    <h1>❌ Utilisateur Refusé</h1>
    <p>L'accès a été refusé pour <strong>{user_id}</strong>.</p>
    <a href="/admin/dashboard">← Retour au tableau de bord</a>
    </body></html>
    """

@app.route('/admin/revoke/<user_id>')
def revoke_user(user_id):
    """Révoquer l'accès d'un utilisateur"""
    users_db = load_data(USERS_DB)
    
    if user_id in users_db:
        users_db[user_id]['approved'] = False
        users_db[user_id]['revoked_at'] = datetime.now().isoformat()
        save_data(USERS_DB, users_db)
    
    log_activity('user_revoked', user_id, "Access revoked by admin")
    
    return f"""
    <html><body style="font-family: Arial; text-align: center; margin-top: 100px;">
    <h1>🔒 Accès Révoqué</h1>
    <p>L'accès a été révoqué pour <strong>{user_id}</strong>.</p>
    <a href="/admin/dashboard">← Retour au tableau de bord</a>
    </body></html>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🌐 GlobalExam AI Server starting on port {port}")
    print(f"🎛️ Admin Dashboard: http://localhost:{port}/admin/dashboard")
    app.run(host='0.0.0.0', port=port, debug=False)
