# -*- coding: utf-8 -*-
{
    'name': 'Employee Management',
    'version': '16.0.2.0.0',
    'category': 'Human Resources',
    'summary': 'Gestion complète des employés, départements, postes et contrats',
    'description': """
        Module de Gestion des Employés — v2
        =====================================
        ✅ Employés avec photo, matricule auto, workflow de statut
        ✅ Départements avec compteurs et responsables
        ✅ Postes avec grille salariale
        ✅ Groupes de sécurité (Employé / Manager RH / Admin)
        ✅ Dashboard avec statistiques en temps réel
        ✅ Rapport PDF fiche employé
        ✅ Wizard de changement de département
        ✅ Design custom avec CSS
        ✅ Contraintes et validations métier complètes
    """,
    'author': 'Votre Nom',
    'website': 'https://www.votresite.com',
    'depends': ['base', 'mail', 'web'],
    'data': [
        # 1. Sécurité en premier
        'security/security.xml',
        'security/ir.model.access.csv',
        # 2. Données
        'data/department_data.xml',
        # 3. Vues
        'views/assets.xml',
        'views/department_views.xml',
        'views/job_position_views.xml',
        'views/employee_views.xml',
        'views/dashboard_views.xml',
        'views/menu_views.xml',
        # 4. Wizard
        'wizard/transfer_wizard_views.xml',
        # 5. Rapports
        'report/employee_report.xml',
        'report/employee_report_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'employee_management/static/src/css/em_style.css',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/banner.png'],
}
