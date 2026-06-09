# 👥 Employee Management — Module Odoo 16

<div align="center">

![Odoo Version](https://img.shields.io/badge/Odoo-16.0-875A7B?style=for-the-badge&logo=odoo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-ORM-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-LGPL--3-blue?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-2.0.0-success?style=for-the-badge)

**Module de gestion complète des Ressources Humaines pour Odoo 16**

*Gestion des employés · Départements hiérarchiques · Postes · Workflow de statut · Rapports PDF*

</div>

---

## 📋 Table des matières

- [Aperçu](#-aperçu)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture technique](#-architecture-technique)
- [Prérequis et installation](#-prérequis-et-installation)
- [Structure du module](#-structure-du-module)
- [Modèles de données](#-modèles-de-données)
- [Workflow et états](#-workflow-et-états)
- [Sécurité et droits d'accès](#-sécurité-et-droits-daccès)
- [Vues et interface](#-vues-et-interface)
- [Validations et contraintes](#-validations-et-contraintes)
- [Rapport PDF](#-rapport-pdf)
- [Wizard de mutation](#-wizard-de-mutation)
- [Dashboard et statistiques](#-dashboard-et-statistiques)
- [Personnalisation CSS](#-personnalisation-css)
- [Guide de développement](#-guide-de-développement)
- [FAQ](#-faq)
- [Auteur](#-auteur)

---

## 🎯 Aperçu

`employee_management` est un module Odoo 16 complet permettant de gérer le cycle de vie entier d'un employé dans une organisation — de l'embauche à la démission — avec une interface soignée, un workflow d'approbation des statuts, et des outils de reporting.

Ce module a été conçu pour illustrer les bonnes pratiques de développement Odoo :

- **MVC** : séparation modèles / vues / contrôleurs
- **ORM Odoo** : computed fields, constrains, onchange, create/unlink overrides
- **Sécurité** : groupes, ACL différenciés par rôle
- **QWeb** : rapports PDF avec mise en page professionnelle
- **TransientModel** : wizard de mutation
- **CSS Backend** : design cohérent avec le backend Odoo

---

## ✨ Fonctionnalités

### 👤 Gestion des Employés
| Fonctionnalité | Détail |
|---|---|
| **Fiche complète** | Photo, nom, matricule auto-généré (`EMP-XXXX`), genre, date de naissance, CIN, adresse |
| **Informations professionnelles** | Département, poste, manager direct, date d'embauche, type de contrat, salaire |
| **Workflow de statut** | Brouillon → Actif → Suspendu / Démissionné (avec traçabilité chatter) |
| **Calculs automatiques** | Âge, ancienneté en années et en mois, salaire net estimé |
| **Chatter intégré** | Historique de toutes les modifications, activités, suivi des changements |
| **Compétences** | Champ texte pour lister langues, certifications, expertises |
| **Équipe** | Smart button affichant les subordonnés directs |

### 🏢 Départements
| Fonctionnalité | Détail |
|---|---|
| **Hiérarchie** | Départements parents/enfants avec `_parent_store` |
| **Compteurs** | Effectif direct et total (sous-départements inclus) |
| **Masse salariale** | Calcul automatique de la masse salariale par département |
| **Responsable** | Lien vers l'employé responsable |
| **Données par défaut** | IT, RH, Finance, Commercial pré-installés |

### 💼 Postes
| Fonctionnalité | Détail |
|---|---|
| **Niveaux** | Junior / Intermédiaire / Senior / Lead / Manager / Directeur |
| **Grille salariale** | Salaire minimum et maximum par poste |
| **Description HTML** | Éditeur riche pour les missions et responsabilités |
| **Compteur d'effectifs** | Nombre d'employés occupant chaque poste |
| **Contrainte unique** | Un même intitulé de poste ne peut exister deux fois dans le même département |

### 🔄 Wizard de Mutation
- Transfert d'un ou plusieurs employés vers un nouveau département
- Changement optionnel de poste et de salaire
- Date de mutation et motif obligatoires
- Message automatique dans le chatter avec l'historique complet

### 🖨️ Rapport PDF
- Fiche employé imprimable en un clic
- Sections : identité, contact, informations professionnelles, compétences
- Design professionnel avec en-tête dégradé et logo
- Accessible depuis la liste (action groupée) ou le formulaire

### 📊 Dashboard & Reporting
- **Vue Graphique** : effectifs par département, colorés par statut
- **Vue Pivot** : répartition croisée département × type de contrat avec masse salariale
- Filtres rapides : actifs, CDI, embauches du mois
- Groupes : par département, poste, manager, lieu de travail

---

## 🏗️ Architecture technique

```
Couche Modèle (Python/ORM)
    ├── em.department       → Départements (hiérarchie _parent_store)
    ├── em.job.position     → Postes / Fonctions
    ├── em.employee         → Employés (modèle principal)
    └── em.transfer.wizard  → TransientModel (mutation)

Couche Vue (XML/QWeb)
    ├── Form View           → Formulaire détaillé avec onglets
    ├── Tree View           → Liste avec multi-edit et actions rapides
    ├── Kanban View         → Cartes groupées par département
    ├── Search View         → Filtres, groupby, recherche full-text
    ├── Graph View          → Histogramme empilé
    ├── Pivot View          → Tableau croisé dynamique
    └── QWeb Report         → Fiche PDF imprimable

Couche Sécurité
    ├── group_em_reader     → Consultation uniquement
    ├── group_em_manager    → CRUD + salaires visibles
    └── group_em_admin      → Tout y compris suppression

Assets Backend
    └── em_style.css        → Design custom (200+ lignes CSS)
```

---

## 📦 Prérequis et installation

### Prérequis
- Odoo **16.0** (Community ou Enterprise)
- Python **3.10+**
- PostgreSQL **12+**
- Modules Odoo requis : `base`, `mail`, `web`

### Installation

**1. Cloner le dépôt**
```bash
git clone https://github.com/votre-username/employee_management.git
```

**2. Copier dans le dossier addons d'Odoo**
```bash
cp -r employee_management/ /path/to/odoo/addons/
# ou créez un lien symbolique :
ln -s /path/to/employee_management /path/to/odoo/addons/employee_management
```

**3. Déclarer le chemin dans la configuration Odoo**

Éditez votre fichier `odoo.conf` :
```ini
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/path/to/your/addons
```

**4. Mettre à jour la liste des modules**
```bash
# Via l'interface : Paramètres → Applications → Mettre à jour la liste
# Ou via CLI :
./odoo-bin -c odoo.conf -d votre_base --update=base
```

**5. Installer le module**
```bash
# Via l'interface : Applications → rechercher "Employee Management" → Installer
# Ou via CLI :
./odoo-bin -c odoo.conf -d votre_base --install=employee_management
```

**6. Vérifier l'installation**

Après l'installation, le menu **Gestion RH** doit apparaître dans la barre de navigation. Les données initiales (4 départements, 5 postes) sont automatiquement créées.

### Mise à jour

Pour mettre à jour le module après modification du code :

```bash
./odoo-bin -c odoo.conf -d votre_base --update=employee_management
```

---

## 📁 Structure du module

```
employee_management/
│
├── __init__.py                         ← Point d'entrée Python
├── __manifest__.py                     ← Déclaration du module (métadonnées, dépendances, fichiers)
│
├── models/
│   ├── __init__.py
│   ├── department.py                   ← Modèle em.department
│   ├── job_position.py                 ← Modèle em.job.position
│   └── employee.py                     ← Modèle em.employee (principal)
│
├── wizard/
│   ├── __init__.py
│   ├── transfer_wizard.py              ← TransientModel em.transfer.wizard
│   └── transfer_wizard_views.xml       ← Vue du wizard (popup)
│
├── views/
│   ├── assets.xml                      ← Injection des assets CSS
│   ├── department_views.xml            ← Form + Tree + Search + Action
│   ├── job_position_views.xml          ← Form + Tree + Search + Action
│   ├── employee_views.xml              ← Form + Tree + Kanban + Search + Actions
│   ├── dashboard_views.xml             ← Graph + Pivot + Actions reporting
│   └── menu_views.xml                  ← Structure des menus
│
├── report/
│   ├── __init__.py
│   ├── employee_report.xml             ← Déclaration de l'action rapport PDF
│   └── employee_report_template.xml    ← Template QWeb (HTML/CSS du PDF)
│
├── security/
│   ├── security.xml                    ← Définition des groupes de sécurité
│   └── ir.model.access.csv             ← Règles d'accès CRUD par modèle et groupe
│
├── data/
│   └── department_data.xml             ← Données initiales (départements, postes, séquence)
│
└── static/
    ├── description/
    │   └── index.html                  ← Page de description dans l'App Store Odoo
    └── src/css/
        └── em_style.css                ← Styles CSS du backend (200+ lignes)
```

---

## 🗃️ Modèles de données

### `em.employee` — Employé (37 champs)

| Champ | Type | Description |
|---|---|---|
| `name` | `Char` | Nom complet (requis, tracké) |
| `employee_ref` | `Char` | Matricule auto (`EMP-XXXX`), readonly |
| `image` | `Binary` | Photo (attachment) |
| `gender` | `Selection` | Masculin / Féminin / Autre |
| `date_of_birth` | `Date` | Date de naissance |
| `age` | `Integer` | Âge calculé (`@api.depends`) |
| `marital_status` | `Selection` | Célibataire / Marié / Divorcé / Veuf |
| `children_count` | `Integer` | Nombre d'enfants |
| `nationality` | `Char` | Nationalité (défaut : Malgache) |
| `cin` | `Char` | Numéro CIN (unique en base) |
| `cin_date` | `Date` | Date de délivrance CIN |
| `address` | `Text` | Adresse complète |
| `phone` | `Char` | Téléphone fixe |
| `mobile` | `Char` | Téléphone mobile |
| `email` | `Char` | Email professionnel (validé regex) |
| `email_personal` | `Char` | Email personnel |
| `department_id` | `Many2one` | Département (requis, tracké) |
| `job_position_id` | `Many2one` | Poste (requis, domain dynamique) |
| `manager_id` | `Many2one` | Manager direct |
| `subordinate_ids` | `One2many` | Liste des subordonnés |
| `subordinate_count` | `Integer` | Compteur subordonnés (calculé) |
| `hiring_date` | `Date` | Date d'embauche (requis) |
| `end_date` | `Date` | Fin de contrat (optionnel) |
| `seniority` | `Integer` | Ancienneté en années (calculé) |
| `seniority_months` | `Integer` | Ancienneté en mois (calculé) |
| `contract_type` | `Selection` | CDI / CDD / Intérim / Stage / Apprentissage / Consultant |
| `salary` | `Float` | Salaire brut en Ariary |
| `salary_net` | `Float` | Salaire net estimé (brut × 77%) |
| `bank_account` | `Char` | RIB / Compte bancaire |
| `work_location` | `Selection` | Présentiel / Télétravail / Hybride |
| `state` | `Selection` | Brouillon / Actif / Suspendu / Démissionné |
| `note` | `Text` | Notes internes (managers uniquement) |
| `skills` | `Text` | Compétences et certifications |
| `color` | `Integer` | Couleur Kanban (calculée selon état) |
| `kanban_state` | `Selection` | En cours / Prêt / Bloqué |

### `em.department` — Département (12 champs)

| Champ | Type | Description |
|---|---|---|
| `name` | `Char` | Nom (unique, requis) |
| `code` | `Char` | Code court (ex : IT, RH) |
| `parent_id` | `Many2one` | Département parent (hiérarchie) |
| `parent_path` | `Char` | Chemin hiérarchique (indexé) |
| `child_ids` | `One2many` | Sous-départements |
| `manager_id` | `Many2one` | Responsable |
| `employee_ids` | `One2many` | Employés directs |
| `employee_count` | `Integer` | Effectif direct (calculé, stocké) |
| `total_employee_count` | `Integer` | Total avec sous-départements |
| `total_salary` | `Float` | Masse salariale actifs |
| `description` | `Text` | Description du département |
| `active` | `Boolean` | Archivage logique |

### `em.job.position` — Poste (11 champs)

| Champ | Type | Description |
|---|---|---|
| `name` | `Char` | Intitulé (requis) |
| `department_id` | `Many2one` | Département |
| `level` | `Selection` | Junior / Intermédiaire / Senior / Lead / Manager / Directeur |
| `description` | `Html` | Description riche du poste |
| `requirements` | `Text` | Compétences requises |
| `salary_min` | `Float` | Plancher salarial |
| `salary_max` | `Float` | Plafond salarial |
| `employee_ids` | `One2many` | Employés sur ce poste |
| `employee_count` | `Integer` | Effectif (calculé, stocké) |
| `active` | `Boolean` | Archivage logique |

### `em.transfer.wizard` — Wizard Mutation (TransientModel)

| Champ | Type | Description |
|---|---|---|
| `employee_ids` | `Many2many` | Employés à transférer |
| `current_department_id` | `Many2one` | Département actuel (readonly) |
| `new_department_id` | `Many2one` | Nouveau département (requis) |
| `new_job_position_id` | `Many2one` | Nouveau poste (optionnel) |
| `new_salary` | `Float` | Nouveau salaire (optionnel) |
| `transfer_date` | `Date` | Date effective de mutation |
| `reason` | `Text` | Motif de la mutation |

---

## 🔁 Workflow et états

L'employé suit un cycle de vie en 4 états :

```
                    ┌─────────────────────────────┐
                    │          BROUILLON           │
                    │  (draft — état par défaut)   │
                    └──────────────┬──────────────┘
                                   │ [Activer]
                    ┌──────────────▼──────────────┐
                    │            ACTIF             │
                    │         (active)             │
                    └──────┬───────────┬──────────┘
                           │[Suspendre]│[Démission]
              ┌────────────▼──┐   ┌───▼──────────────┐
              │   SUSPENDU    │   │   DÉMISSIONNAIRE  │
              │  (suspended)  │   │    (resigned)     │
              └───────────────┘   └──────────────────┘
                        │                  │
                        └──────┬───────────┘
                               │ [Remettre en brouillon]
                    ┌──────────▼──────────────┐
                    │          BROUILLON       │
                    └─────────────────────────┘
```

### Règles du workflow

| Transition | Condition | Action Python |
|---|---|---|
| `draft → active` | Depuis n'importe quel état sauf `active` | `action_activate()` |
| `active → suspended` | Uniquement depuis `active` | `action_suspend()` |
| `active/suspended → resigned` | Uniquement depuis `active` ou `suspended` | `action_resign()` |
| `any → draft` | Depuis tout état sauf `draft` | `action_reset_draft()` |

Chaque transition enregistre automatiquement un message dans le **chatter** avec le nom de l'utilisateur ayant effectué l'action.

### Suppression protégée
Un employé `active` ne peut pas être supprimé. Il faut d'abord le désactiver (suspendu ou démissionnaire).

---

## 🔐 Sécurité et droits d'accès

### Groupes définis

| Groupe | XML ID | Description |
|---|---|---|
| **Lecteur** | `group_em_reader` | Consultation uniquement — lecture de toutes les fiches |
| **Responsable RH** | `group_em_manager` | Création, modification, archivage + accès aux salaires |
| **Administrateur RH** | `group_em_admin` | Accès complet incluant la suppression et la configuration |

Les groupes sont **hiérarchiques** : `admin` implique `manager` qui implique `reader`.

L'administrateur système (`base.user_admin`) est automatiquement dans le groupe Admin.

### Matrice des droits (ACL)

| Modèle | Lecteur | Manager | Admin |
|---|---|---|---|
| `em.department` | R | R+W+C | R+W+C+D |
| `em.job.position` | R | R+W+C | R+W+C+D |
| `em.employee` | R | R+W+C | R+W+C+D |
| `em.transfer.wizard` | — | R+W+C+D | R+W+C+D |

*R=Read, W=Write, C=Create, D=Delete*

### Visibilité conditionnelle dans les vues

- **Champ salaire** : visible uniquement pour `group_em_manager`
- **Champ notes internes** : visible uniquement pour `group_em_manager`
- **Bouton Mutation** : visible uniquement pour `group_em_manager`
- **Menu Reporting** : visible uniquement pour `group_em_manager`
- **Menu Configuration** : visible uniquement pour `group_em_manager`

### Assigner un groupe à un utilisateur

```
Paramètres → Utilisateurs et Sociétés → Utilisateurs
→ Sélectionner un utilisateur
→ Section "Gestion des Employés"
→ Choisir le niveau d'accès
```

---

## 🖥️ Vues et interface

### Form View — Fiche Employé

La fiche employé est organisée en zones :

```
┌─────────────────────────────────────────────────────┐
│  [Header] Boutons d'action + Barre de statut        │
├─────────────────────────────────────────────────────┤
│  [Alerte] Bandeau coloré selon le statut actuel     │
├─────────────────────────────────────────────────────┤
│  [Smart Buttons] Compteur équipe | Bouton Mutation  │
├──────────────────────┬──────────────────────────────┤
│  [Photo]   Nom       │                              │
│            Matricule │                              │
├──────────────────────┴──────────────────────────────┤
│  Infos personnelles  │  Infos professionnelles      │
│  - Genre, âge, CIN   │  - Département, poste        │
│  - Situation fam.    │  - Manager, embauche         │
│  - Nationalité       │  - Contrat, lieu travail     │
├──────────────────────┼──────────────────────────────┤
│  Contact             │  Rémunération (managers)     │
│  - Téléphone, email  │  - Salaire brut / net        │
│                      │  - RIB                       │
├──────────────────────┴──────────────────────────────┤
│  [Onglets] Adresse | Compétences | Notes internes   │
├─────────────────────────────────────────────────────┤
│  [Chatter] Historique, activités, messages          │
└─────────────────────────────────────────────────────┘
```

### Tree View — Liste des Employés

La liste supporte le **multi-edit** (sélection multiple → modification groupée) et affiche :
- Matricule, photo miniature, nom, département, poste
- Type de contrat, date d'embauche, ancienneté
- Salaire (masqué pour les lecteurs)
- Badge coloré du statut
- Boutons d'action rapide (Activer, Imprimer)

Coloration des lignes :
- 🟢 Vert : Actif
- 🟡 Jaune : Suspendu
- 🔴 Rouge : Démissionnaire
- ⬜ Gris : Brouillon

### Kanban View — Cartes par Département

Groupement par défaut par département. Chaque carte affiche :
- Photo + Nom + Matricule
- Poste, téléphone, email
- Badge de statut coloré

### Search View — Filtres disponibles

**Recherche textuelle :**
- Nom ou matricule (champ combiné)
- Département, poste, manager, CIN

**Filtres rapides :**
- Actifs / Brouillons / Suspendus / Démissionnaires
- CDI / CDD / Stage
- Sans manager direct
- Embauché ce mois

**Groupements :**
- Par département, poste, type de contrat, statut, manager, lieu de travail, mois d'embauche

---

## ✅ Validations et contraintes

### Contraintes Python (`@api.constrains`)

| Champ | Règle | Message d'erreur |
|---|---|---|
| `salary` | Supérieur ou égal à 0 | `❌ Le salaire ne peut pas être négatif !` |
| `salary` | Supérieur au SMIG (348 000 Ar) | `⚠️ Salaire inférieur au SMIG (348 000 Ar)` |
| `email` | Format valide (regex) | `❌ Adresse email invalide` |
| `date_of_birth` | Non future, âge ≥ 16 ans | `❌ Date invalide` / `❌ Âge minimum 16 ans` |
| `hiring_date` + `end_date` | Fin ≥ Début | `❌ Date de fin avant date d'embauche` |
| `children_count` | Valeur ≥ 0 | `❌ Nombre d'enfants négatif` |
| `cin` | Unique en base | `❌ CIN déjà utilisé par [nom de l'employé]` |
| `department` (wizard) | Requis | Validation standard Odoo |

### Contraintes SQL (`_sql_constraints`)

```python
# em.job.position
('unique_name_dept', 'UNIQUE(name, department_id)',
 'Un poste avec ce nom existe déjà dans ce département !')
```

### Comportements `@api.onchange`

| Déclencheur | Comportement |
|---|---|
| Changement de `department_id` | Vide `job_position_id` si le poste n'appartient pas au nouveau département + warning |
| Changement de `contract_type` vers CDI | Efface automatiquement `end_date` |

### Protection à la suppression (`unlink`)

- Un employé avec `state == 'active'` ne peut pas être supprimé
- Message : `❌ Impossible de supprimer un employé actif. Désactivez-le d'abord.`

---

## 🖨️ Rapport PDF

### Générer la fiche d'un employé

**Depuis la liste :**
1. Sélectionner un ou plusieurs employés (cocher les cases)
2. Menu `Action` → `Fiche Employé`

**Depuis le formulaire :**
1. Ouvrir la fiche de l'employé
2. Cliquer sur le bouton **🖨️ Fiche PDF** (visible si l'employé n'est pas en brouillon)

### Contenu du rapport

- **En-tête** : photo, nom, poste, département, matricule, badge statut
- **Informations personnelles** : genre, date de naissance, âge, nationalité, CIN, situation familiale, adresse
- **Contact** : téléphone, mobile, email pro, email perso
- **Informations professionnelles** : département, poste, manager, lieu de travail, dates d'embauche/fin, ancienneté, type de contrat
- **Compétences** (si renseignées)
- **Pied de page** : date de génération + mention CONFIDENTIEL

### Personnaliser le template

Le template QWeb se trouve dans `report/employee_report_template.xml`. Pour le modifier :

```xml
<template id="report_employee_card_template">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="emp">
            <t t-call="web.external_layout">
                <div class="page">
                    <!-- Votre HTML ici -->
                    <t t-esc="emp.name"/>
                </div>
            </t>
        </t>
    </t>
</template>
```

Variables disponibles dans le template :

| Variable | Type | Description |
|---|---|---|
| `docs` | `recordset` | Ensemble des employés à imprimer |
| `emp` | `em.employee` | Employé courant dans la boucle |
| `emp.name` | `str` | Nom complet |
| `emp.image` | `bytes` | Photo (utiliser `image_data_uri()`) |
| `emp.department_id.name` | `str` | Nom du département |
| `context_today()` | `date` | Date du jour |

---

## 🔄 Wizard de Mutation

Le wizard permet de transférer un ou plusieurs employés dans un autre département, en une seule opération atomique.

### Déclencher le wizard

**Depuis le formulaire d'un employé actif :**
```
Bouton "🔄 Mutation" (visible pour les managers uniquement)
```

**Depuis la liste (action groupée) :**
```
Sélectionner plusieurs employés → Action → (appel programmatique)
```

### Fonctionnement

```python
def action_transfer_wizard(self):
    return {
        'type': 'ir.actions.act_window',
        'res_model': 'em.transfer.wizard',
        'view_mode': 'form',
        'target': 'new',  # Ouvre en popup
        'context': {
            'default_employee_ids': self.ids,
            'default_current_department_id': self.department_id.id,
        },
    }
```

Le wizard :
1. Affiche les employés concernés (readonly)
2. Demande le nouveau département (requis)
3. Propose optionnellement un nouveau poste (filtré sur le département choisi)
4. Permet de modifier le salaire
5. Demande la date effective et le motif
6. Confirme la mutation → met à jour tous les champs + log chatter

### Message chatter généré

```
🔄 Mutation effectuée le 01/06/2025 par Admin.
📁 Nouveau département : Informatique
💼 Nouveau poste : Développeur Odoo Senior
📝 Motif : Promotion interne suite à l'évaluation annuelle
```

---

## 📊 Dashboard et statistiques

Accessible via **Gestion RH → Reporting → Tableau de bord** (managers uniquement).

### Vue Graphique (Histogramme)
- **Axe X** : Départements
- **Colonnes** : Empilées par statut (Actif / Suspendu / Démissionnaire / Brouillon)
- Filtre par défaut : employés actifs uniquement

### Vue Pivot (Tableau croisé)
- **Lignes** : Départements
- **Colonnes** : Types de contrat (CDI, CDD, Stage, etc.)
- **Mesure** : Masse salariale (somme des salaires bruts)
- Extensible : ajouter des dimensions personnalisées

### Vue Graphique — Répartition par contrat
Accessible via **Reporting → Répartition par contrat** :
- Camembert ou histogramme selon le type de contrat
- Filtré sur les employés actifs

---

## 🎨 Personnalisation CSS

Le fichier `static/src/css/em_style.css` contient 200+ lignes de CSS organisées en sections :

```css
/* Variables CSS */
:root {
    --em-primary:     #2C3E6B;   /* Bleu marine */
    --em-accent:      #4F8EF7;   /* Bleu accent */
    --em-success:     #27ae60;
    --em-warning:     #f39c12;
    --em-danger:      #e74c3c;
    --em-card-radius: 12px;
}
```

### Sections du CSS

| Section | Description |
|---|---|
| `Page header` | Dégradé bleu sur le titre de la fiche employé |
| `Avatar` | Bordure et effet hover sur la photo |
| `Smart Buttons` | Bordure, hover et animation sur les boutons statistiques |
| `Groups/sections` | Labels majuscules et espacés |
| `Notebook` | Onglets avec indicateur de sélection |
| `Status bar` | Couleur accent sur l'état actif |
| `Tree View` | Coloration des lignes selon le statut |
| `Kanban cards` | Cartes avec en-tête dégradé, corps blanc |
| `Dashboard tiles` | Tuiles colorées pour les KPIs |
| `Rapport PDF` | Styles pour la fiche imprimable |
| `Alertes` | Bandeaux colorés dans les formulaires |

### Modifier les couleurs principales

Éditez les variables CSS dans `em_style.css` :

```css
:root {
    --em-primary: #1a3a5c;     /* Votre couleur primaire */
    --em-accent:  #e63946;     /* Votre couleur d'accent */
}
```

---

## 🛠️ Guide de développement

### Ajouter un nouveau champ

**1. Déclarer le champ dans le modèle Python :**
```python
# models/employee.py
langue = fields.Selection(
    selection=[('fr', 'Français'), ('en', 'Anglais'), ('mg', 'Malgache')],
    string='Langue principale',
    default='fr',
)
```

**2. Ajouter le champ dans la vue XML :**
```xml
<!-- views/employee_views.xml — dans le group approprié -->
<field name="langue"/>
```

**3. Mettre à jour le module :**
```bash
./odoo-bin -c odoo.conf -d votre_base --update=employee_management
```

### Ajouter une contrainte métier

```python
# models/employee.py
@api.constrains('phone')
def _check_phone_format(self):
    import re
    pattern = r'^\+?[\d\s\-]{8,15}$'
    for emp in self:
        if emp.phone and not re.match(pattern, emp.phone):
            raise ValidationError(
                _('❌ Format de téléphone invalide : %s') % emp.phone
            )
```

### Créer une nouvelle action de bouton

```python
# models/employee.py
def action_send_welcome_email(self):
    """Envoie un email de bienvenue à l'employé."""
    for emp in self:
        if not emp.email:
            raise UserError(_('❌ L\'employé n\'a pas d\'email professionnel !'))
        # Logique d'envoi...
        emp.message_post(
            body=_('📧 Email de bienvenue envoyé à %s.') % emp.email,
            message_type='comment',
            subtype_xmlid='mail.mt_note',
        )
```

```xml
<!-- views/employee_views.xml — dans le header -->
<button name="action_send_welcome_email"
        string="📧 Email de bienvenue"
        type="object"
        class="btn-secondary"
        attrs="{'invisible': [('state', '!=', 'active')]}"/>
```

### Étendre le rapport PDF

Pour ajouter une section au rapport :

```xml
<!-- report/employee_report_template.xml -->
<!-- Après la section Compétences -->
<t t-if="emp.bank_account">
    <div class="em-report-section-title">🏦 Coordonnées Bancaires</div>
    <p><t t-esc="emp.bank_account"/></p>
</t>
```

### Bonnes pratiques respectées dans ce module

```python
# ✅ Utilisation de _() pour l'internationalisation
raise ValidationError(_('❌ Le salaire ne peut pas être négatif !'))

# ✅ @api.model_create_multi au lieu de create() simple (Odoo 16+)
@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        if vals.get('employee_ref', _('Nouveau')) == _('Nouveau'):
            vals['employee_ref'] = self.env['ir.sequence'].next_by_code('em.employee')
    return super().create(vals_list)

# ✅ Vérification des droits avec has_group()
def action_transfer_wizard(self):
    if not self.env.user.has_group('employee_management.group_em_manager'):
        raise UserError(_('⛔ Accès refusé.'))

# ✅ Tracking des changements importants
department_id = fields.Many2one(..., tracking=True)

# ✅ Ondelete pour les FK critiques
department_id = fields.Many2one(..., ondelete='restrict')
```

---

## ❓ FAQ

**Q : Pourquoi le menu Reporting n'est-il pas visible ?**
> Le menu Reporting est réservé au groupe `group_em_manager`. Allez dans Paramètres → Utilisateurs → attribuez le rôle "Responsable RH" à votre utilisateur.

**Q : Comment modifier le SMIG de référence ?**
> Dans `models/employee.py`, méthode `_check_salary()` :
> ```python
> if emp.salary > 0 and emp.salary < 348_000:  # ← modifier cette valeur
> ```

**Q : Les données de département ne s'installent pas automatiquement.**
> Vérifiez que `data/department_data.xml` est bien listé dans le `__manifest__.py` et que le tag `noupdate="1"` est présent. En cas de réinstallation, utilisez `--load-language=fr_FR` si des traductions sont en cause.

**Q : Comment désactiver la validation SMIG ?**
> Commentez ou supprimez ce bloc dans `models/employee.py` :
> ```python
> # if emp.salary > 0 and emp.salary < 348_000:
> #     raise ValidationError(...)
> ```

**Q : Le rapport PDF ne génère pas la photo.**
> Assurez-vous que l'employé a bien une photo uploadée. Le template utilise `image_data_uri(emp.image)` qui retourne `None` si aucune image n'est présente — le template gère ce cas avec `t-if="emp.image"`.

**Q : Comment ajouter ce module à Odoo Enterprise ?**
> Le module fonctionne avec Odoo 16 Community et Enterprise. Avec Enterprise, le module `hr` natif existe déjà — vous devrez soit modifier les dépendances pour hériter de `hr`, soit garder ce module indépendant pour un projet de démonstration.

**Q : Puis-je utiliser ce module avec leave_management ?**
> Oui ! Le module `leave_management` du même projet dépend de `employee_management`. Installez d'abord `employee_management` puis `leave_management`.

---

## 🗺️ Roadmap

- [ ] Intégration avec `leave_management` (compteurs de congés sur la fiche employé)
- [ ] Export Excel de la liste des employés
- [ ] Évaluation annuelle (module `performance_review`)
- [ ] Organigramme interactif
- [ ] Import CSV en masse pour la création d'employés
- [ ] Notifications email automatiques (anniversaire d'embauche, fin de CDD)

---

## 👨‍💻 Auteur

**Votre Nom**
- GitHub : (https://github.com/ramisarivelo)
- LinkedIn : (https://linkedin.com/in/mickael-amisarivelo)
- Email : ramisarivelomickael@gmail.com

---

## 📄 Licence

Ce module est distribué sous licence **LGPL-3**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- [Odoo SA](https://www.odoo.com) pour le framework et la documentation

---

<div align="center">

**⭐ Si ce projet vous a aidé, n'hésitez pas à laisser une étoile sur GitHub !**

*Développé avec ❤️ pour illustrer les bonnes pratiques Odoo*

</div>
