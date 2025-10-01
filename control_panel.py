#!/usr/bin/env python3
"""
Panneau de Contrôle pour GlobalExam AI - Sécurité v4
===================================================

Ce panneau vous permet de contrôler qui peut utiliser votre application :

1. Voir toutes les demandes d'accès
2. Approuver ou refuser des utilisateurs
3. Révoquer l'accès à distance
4. Voir les logs d'utilisation
5. Mode serveur local pour tests

Vous gardez le contrôle total sur votre application !

Auteur : Projet Étudiant
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import threading
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import hashlib

class ControlPanel:
    """
    Panneau de contrôle pour gérer l'accès à l'application
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GlobalExam AI - Panneau de Contrôle")
        self.root.geometry("800x600")
        
        # Données de contrôle
        self.authorized_users = {}  # user_id -> session_info
        self.pending_requests = []  # Demandes en attente
        self.usage_logs = []       # Logs d'utilisation
        
        # Configuration
        self.config = {
            'server_port': 8080,
            'session_duration_hours': 8,
            'auto_approve_known_users': False
        }
        
        # Serveur local pour tests
        self.server = None
        self.server_thread = None
        
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """Créer l'interface utilisateur"""
        
        # Notebook pour les onglets
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Onglet 1: Demandes d'accès
        self.requests_frame = ttk.Frame(notebook)
        notebook.add(self.requests_frame, text="Demandes d'Accès")
        self.setup_requests_tab()
        
        # Onglet 2: Utilisateurs autorisés
        self.users_frame = ttk.Frame(notebook)
        notebook.add(self.users_frame, text="Utilisateurs Autorisés")
        self.setup_users_tab()
        
        # Onglet 3: Logs d'utilisation
        self.logs_frame = ttk.Frame(notebook)
        notebook.add(self.logs_frame, text="Logs d'Utilisation")
        self.setup_logs_tab()
        
        # Onglet 4: Configuration
        self.config_frame = ttk.Frame(notebook)
        notebook.add(self.config_frame, text="Configuration")
        self.setup_config_tab()
        
        # Barre de statut
        self.status_bar = tk.Label(self.root, text="Prêt", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_requests_tab(self):
        """Configuration de l'onglet demandes d'accès"""
        
        # Titre
        title = tk.Label(self.requests_frame, text="Demandes d'Accès en Attente", font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Liste des demandes
        columns = ('Utilisateur', 'Ordinateur', 'Raison', 'Heure', 'Actions')
        self.requests_tree = ttk.Treeview(self.requests_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.requests_tree.heading(col, text=col)
            self.requests_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.requests_frame, orient='vertical', command=self.requests_tree.yview)
        self.requests_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        tree_frame = tk.Frame(self.requests_frame)
        tree_frame.pack(fill='both', expand=True, padx=10)
        
        self.requests_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Boutons
        buttons_frame = tk.Frame(self.requests_frame)
        buttons_frame.pack(pady=10)
        
        tk.Button(buttons_frame, text="✓ Approuver", command=self.approve_request, bg='green', fg='white').pack(side='left', padx=5)
        tk.Button(buttons_frame, text="✗ Refuser", command=self.deny_request, bg='red', fg='white').pack(side='left', padx=5)
        tk.Button(buttons_frame, text="🔄 Actualiser", command=self.refresh_requests).pack(side='left', padx=5)
        
        # Simulation de demandes pour test
        tk.Button(buttons_frame, text="🧪 Simuler Demande", command=self.simulate_request).pack(side='left', padx=5)
        
    def setup_users_tab(self):
        """Configuration de l'onglet utilisateurs autorisés"""
        
        title = tk.Label(self.users_frame, text="Utilisateurs Autorisés", font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Liste des utilisateurs
        columns = ('Utilisateur', 'Ordinateur', 'Autorisé le', 'Expire le', 'Statut')
        self.users_tree = ttk.Treeview(self.users_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=140)
        
        # Scrollbar
        scrollbar2 = ttk.Scrollbar(self.users_frame, orient='vertical', command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar2.set)
        
        # Pack
        tree_frame2 = tk.Frame(self.users_frame)
        tree_frame2.pack(fill='both', expand=True, padx=10)
        
        self.users_tree.pack(side='left', fill='both', expand=True)
        scrollbar2.pack(side='right', fill='y')
        
        # Boutons
        buttons_frame2 = tk.Frame(self.users_frame)
        buttons_frame2.pack(pady=10)
        
        tk.Button(buttons_frame2, text="🚫 Révoquer Accès", command=self.revoke_access, bg='orange', fg='white').pack(side='left', padx=5)
        tk.Button(buttons_frame2, text="⏰ Étendre Session", command=self.extend_session, bg='blue', fg='white').pack(side='left', padx=5)
        tk.Button(buttons_frame2, text="🔄 Actualiser", command=self.refresh_users).pack(side='left', padx=5)
        
    def setup_logs_tab(self):
        """Configuration de l'onglet logs"""
        
        title = tk.Label(self.logs_frame, text="Logs d'Utilisation", font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Zone de texte pour les logs
        self.logs_text = scrolledtext.ScrolledText(self.logs_frame, height=20, width=80)
        self.logs_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Boutons
        logs_buttons = tk.Frame(self.logs_frame)
        logs_buttons.pack(pady=5)
        
        tk.Button(logs_buttons, text="🔄 Actualiser Logs", command=self.refresh_logs).pack(side='left', padx=5)
        tk.Button(logs_buttons, text="🗑️ Effacer Logs", command=self.clear_logs).pack(side='left', padx=5)
        tk.Button(logs_buttons, text="💾 Exporter Logs", command=self.export_logs).pack(side='left', padx=5)
        
    def setup_config_tab(self):
        """Configuration de l'onglet configuration"""
        
        title = tk.Label(self.config_frame, text="Configuration du Système", font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Configuration serveur
        server_frame = tk.LabelFrame(self.config_frame, text="Serveur Local (pour tests)")
        server_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(server_frame, text="Port:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.port_var = tk.StringVar(value=str(self.config['server_port']))
        tk.Entry(server_frame, textvariable=self.port_var, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        self.server_status = tk.Label(server_frame, text="Arrêté", fg='red')
        self.server_status.grid(row=0, column=2, padx=10, pady=2)
        
        tk.Button(server_frame, text="▶️ Démarrer Serveur", command=self.start_server).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(server_frame, text="⏹️ Arrêter Serveur", command=self.stop_server).grid(row=1, column=1, padx=5, pady=5)
        
        # Configuration sessions
        session_frame = tk.LabelFrame(self.config_frame, text="Sessions")
        session_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(session_frame, text="Durée session (heures):").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.duration_var = tk.StringVar(value=str(self.config['session_duration_hours']))
        tk.Entry(session_frame, textvariable=self.duration_var, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        # Auto-approbation
        self.auto_approve_var = tk.BooleanVar(value=self.config['auto_approve_known_users'])
        tk.Checkbutton(session_frame, text="Auto-approuver les utilisateurs connus", 
                      variable=self.auto_approve_var).grid(row=1, column=0, columnspan=2, sticky='w', padx=5, pady=2)
        
        # Bouton sauvegarder
        tk.Button(session_frame, text="💾 Sauvegarder Configuration", command=self.save_config).grid(row=2, column=0, columnspan=2, pady=10)
        
    def simulate_request(self):
        """Simuler une demande d'accès pour test"""
        request = {
            'user_id': f'test_user_{int(time.time())}',
            'reason': 'Test de l\'application',
            'request_time': datetime.now().isoformat(),
            'system_info': {
                'username': 'TestUser',
                'computer_name': 'TEST-PC',
                'system': 'Windows'
            }
        }
        
        self.pending_requests.append(request)
        self.refresh_requests()
        self.log_message(f"Demande simulée pour {request['user_id']}")
        
    def approve_request(self):
        """Approuver une demande sélectionnée"""
        selection = self.requests_tree.selection()
        if not selection:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une demande à approuver")
            return
        
        item = self.requests_tree.item(selection[0])
        user_id = item['values'][0]
        
        # Trouver la demande
        request = None
        for req in self.pending_requests:
            if req['user_id'] == user_id:
                request = req
                break
        
        if request:
            # Créer une session autorisée
            session_info = {
                'user_id': user_id,
                'session_token': hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest(),
                'granted_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(hours=self.config['session_duration_hours'])).isoformat(),
                'system_info': request['system_info'],
                'status': 'active'
            }
            
            self.authorized_users[user_id] = session_info
            self.pending_requests.remove(request)
            
            self.refresh_requests()
            self.refresh_users()
            self.log_message(f"✓ Accès approuvé pour {user_id}")
            
            messagebox.showinfo("Succès", f"Accès approuvé pour {user_id}")
    
    def deny_request(self):
        """Refuser une demande sélectionnée"""
        selection = self.requests_tree.selection()
        if not selection:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une demande à refuser")
            return
        
        item = self.requests_tree.item(selection[0])
        user_id = item['values'][0]
        
        # Supprimer la demande
        self.pending_requests = [req for req in self.pending_requests if req['user_id'] != user_id]
        
        self.refresh_requests()
        self.log_message(f"✗ Accès refusé pour {user_id}")
        
        messagebox.showinfo("Refusé", f"Accès refusé pour {user_id}")
    
    def revoke_access(self):
        """Révoquer l'accès d'un utilisateur"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un utilisateur")
            return
        
        item = self.users_tree.item(selection[0])
        user_id = item['values'][0]
        
        if user_id in self.authorized_users:
            del self.authorized_users[user_id]
            self.refresh_users()
            self.log_message(f"🚫 Accès révoqué pour {user_id}")
            messagebox.showinfo("Révoqué", f"Accès révoqué pour {user_id}")
    
    def extend_session(self):
        """Étendre la session d'un utilisateur"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Sélection", "Veuillez sélectionner un utilisateur")
            return
        
        item = self.users_tree.item(selection[0])
        user_id = item['values'][0]
        
        if user_id in self.authorized_users:
            # Étendre de X heures
            new_expiry = datetime.now() + timedelta(hours=self.config['session_duration_hours'])
            self.authorized_users[user_id]['expires_at'] = new_expiry.isoformat()
            
            self.refresh_users()
            self.log_message(f"⏰ Session étendue pour {user_id}")
            messagebox.showinfo("Étendu", f"Session étendue pour {user_id}")
    
    def refresh_requests(self):
        """Actualiser la liste des demandes"""
        # Vider la liste
        for item in self.requests_tree.get_children():
            self.requests_tree.delete(item)
        
        # Ajouter les demandes
        for request in self.pending_requests:
            self.requests_tree.insert('', 'end', values=(
                request['user_id'],
                request['system_info'].get('computer_name', 'Inconnu'),
                request.get('reason', 'Non spécifiée'),
                request['request_time'][:19],  # Sans microsecondes
                'En attente'
            ))
    
    def refresh_users(self):
        """Actualiser la liste des utilisateurs"""
        # Vider la liste
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Ajouter les utilisateurs
        for user_id, session in self.authorized_users.items():
            # Vérifier si expiré
            try:
                expires_at = datetime.fromisoformat(session['expires_at'])
                status = 'Actif' if datetime.now() < expires_at else 'Expiré'
            except:
                status = 'Erreur'
            
            self.users_tree.insert('', 'end', values=(
                user_id,
                session['system_info'].get('computer_name', 'Inconnu'),
                session['granted_at'][:19],
                session['expires_at'][:19],
                status
            ))
    
    def refresh_logs(self):
        """Actualiser les logs"""
        self.logs_text.delete(1.0, tk.END)
        
        for log in self.usage_logs:
            self.logs_text.insert(tk.END, f"{log}\n")
        
        self.logs_text.see(tk.END)
    
    def clear_logs(self):
        """Effacer les logs"""
        if messagebox.askyesno("Confirmation", "Effacer tous les logs ?"):
            self.usage_logs.clear()
            self.refresh_logs()
    
    def export_logs(self):
        """Exporter les logs"""
        filename = f"globalexam_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for log in self.usage_logs:
                    f.write(f"{log}\n")
            messagebox.showinfo("Exporté", f"Logs exportés vers {filename}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur d'export : {e}")
    
    def log_message(self, message: str):
        """Ajouter un message aux logs"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.usage_logs.append(log_entry)
        
        # Garder seulement les 1000 derniers logs
        if len(self.usage_logs) > 1000:
            self.usage_logs = self.usage_logs[-1000:]
        
        self.status_bar.config(text=message)
    
    def start_server(self):
        """Démarrer le serveur local pour tests"""
        if self.server_thread and self.server_thread.is_alive():
            messagebox.showwarning("Serveur", "Le serveur est déjà en cours d'exécution")
            return
        
        try:
            port = int(self.port_var.get())
            self.config['server_port'] = port
            
            # Créer le serveur dans un thread séparé
            self.server_thread = threading.Thread(target=self._run_server, args=(port,))
            self.server_thread.daemon = True
            self.server_thread.start()
            
            self.server_status.config(text=f"En cours (port {port})", fg='green')
            self.log_message(f"Serveur démarré sur le port {port}")
            
        except ValueError:
            messagebox.showerror("Erreur", "Port invalide")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur serveur : {e}")
    
    def stop_server(self):
        """Arrêter le serveur local"""
        if self.server:
            self.server.shutdown()
            self.server = None
        
        self.server_status.config(text="Arrêté", fg='red')
        self.log_message("Serveur arrêté")
    
    def _run_server(self, port: int):
        """Exécuter le serveur HTTP simple"""
        try:
            handler = self._create_request_handler()
            self.server = socketserver.TCPServer(("", port), handler)
            self.server.serve_forever()
        except Exception as e:
            self.log_message(f"Erreur serveur : {e}")
    
    def _create_request_handler(self):
        """Créer le gestionnaire de requêtes HTTP"""
        control_panel = self
        
        class RequestHandler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                # Traiter les requêtes POST de l'application
                if self.path == '/api/auth':
                    self._handle_auth_request()
                elif self.path == '/api/check':
                    self._handle_check_request()
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def _handle_auth_request(self):
                # Traiter demande d'authentification
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    request_data = json.loads(post_data.decode('utf-8'))
                    
                    user_info = request_data.get('user_info', {})
                    user_id = user_info.get('user_id')
                    
                    # Vérifier si déjà autorisé
                    if user_id in control_panel.authorized_users:
                        session = control_panel.authorized_users[user_id]
                        expires_at = datetime.fromisoformat(session['expires_at'])
                        
                        if datetime.now() < expires_at:
                            # Session encore valide
                            response = {
                                'access_granted': True,
                                'session_token': session['session_token'],
                                'expires_at': session['expires_at']
                            }
                        else:
                            # Session expirée
                            response = {
                                'access_granted': False,
                                'reason': 'Session expirée'
                            }
                    else:
                        # Ajouter à la liste des demandes
                        control_panel.pending_requests.append(user_info)
                        control_panel.log_message(f"Nouvelle demande de {user_id}")
                        
                        response = {
                            'access_granted': False,
                            'reason': 'Demande en attente d\'approbation'
                        }
                    
                    # Envoyer la réponse
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                    
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    control_panel.log_message(f"Erreur auth : {e}")
            
            def _handle_check_request(self):
                # Vérifier session existante
                try:
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    check_data = json.loads(post_data.decode('utf-8'))
                    
                    user_id = check_data.get('user_id')
                    session_token = check_data.get('session_token')
                    
                    # Vérifier la session
                    valid = False
                    if user_id in control_panel.authorized_users:
                        session = control_panel.authorized_users[user_id]
                        if (session['session_token'] == session_token and
                            datetime.now() < datetime.fromisoformat(session['expires_at'])):
                            valid = True
                    
                    response = {'session_valid': valid}
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                    
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    control_panel.log_message(f"Erreur check : {e}")
            
            def log_message(self, format, *args):
                # Supprimer les logs HTTP verbeux
                pass
        
        return RequestHandler
    
    def save_config(self):
        """Sauvegarder la configuration"""
        try:
            self.config['server_port'] = int(self.port_var.get())
            self.config['session_duration_hours'] = int(self.duration_var.get())
            self.config['auto_approve_known_users'] = self.auto_approve_var.get()
            
            messagebox.showinfo("Sauvegardé", "Configuration sauvegardée")
            self.log_message("Configuration sauvegardée")
            
        except ValueError:
            messagebox.showerror("Erreur", "Valeurs de configuration invalides")
    
    def load_data(self):
        """Charger les données sauvegardées"""
        # Pour cette démo, on commence avec des données vides
        # Dans une vraie application, on chargerait depuis des fichiers
        pass
    
    def run(self):
        """Lancer le panneau de contrôle"""
        self.log_message("Panneau de contrôle démarré")
        self.root.mainloop()

def main():
    """Fonction principale"""
    print("GlobalExam AI - Panneau de Contrôle v4")
    print("="*50)
    
    app = ControlPanel()
    app.run()

if __name__ == "__main__":
    main()
