# -*- coding: utf-8 -*-
{
    'name': 'Leave Management',
    'version': '16.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Gestion des demandes de congé avec workflow d\'approbation',
    'description': """
        Module de Gestion des Congés
        ============================
        Fonctionnalités :
        - Soumission de demandes de congé par les employés
        - Workflow d'approbation (Brouillon → En attente → Approuvé/Refusé)
        - Contrôle des chevauchements de dates
        - Calcul automatique du nombre de jours
        - Notifications par email (chatter)
        - Tableau de bord avec statistiques
        - Droits d'accès différenciés (employé / manager)
    """,
    'author': 'Votre Nom',
    'website': 'https://www.votresite.com',
    'depends': ['base', 'mail', 'employee_management'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/leave_type_data.xml',
        'views/leave_type_views.xml',
        'views/leave_request_views.xml',
        'views/leave_dashboard_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
