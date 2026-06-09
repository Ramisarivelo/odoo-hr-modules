# 🏖️ Leave Management — Module Odoo 16

<div align="center">

![Odoo Version](https://img.shields.io/badge/Odoo-16.0-875A7B?style=for-the-badge&logo=odoo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-ORM-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-LGPL--3-blue?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-2.0.0-success?style=for-the-badge)

**Module de gestion complète des demandes de congé pour Odoo 16**

*Workflow d'approbation · Allocations et soldes · Attestation PDF · Dashboard analytique*

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
- [Allocations et soldes](#-allocations-et-soldes)
- [Wizards](#-wizards)
- [Rapport PDF — Attestation](#-rapport-pdf--attestation)
- [Dashboard et statistiques](#-dashboard-et-statistiques)
- [Design CSS custom](#-design-css-custom)
- [Guide de développement](#-guide-de-développement)
- [FAQ](#-faq)
- [Auteur](#-auteur)

---

## 🎯 Aperçu

`leave_management` est un module Odoo 16 qui gère le cycle de vie complet des demandes de congé dans une organisation. Il dépend du module `employee_management` du même projet.

Ce module illustre les concepts Odoo avancés suivants :

- **Workflow métier** : machines à états avec transitions protégées
- **TransientModel** : wizards de refus et d'annulation groupée
- **Computed fields** : calcul de soldes, jours restants, taux d'utilisation
- **Contraintes croisées** : détection de chevauchement entre demandes
- **QWeb reports** : attestation PDF avec mise en page professionnelle
- **Sécurité** : groupes hiérarchiques, vues conditionnelles par rôle
- **CSS backend** : interface enrichie avec design cohérent

---

## ✨ Fonctionnalités

### 📋 Demandes de Congé
| Fonctionnalité | Détail |
|---|---|
| **Workflow complet** | Brouillon → En attente → Approuvé / Refusé / Annulé |
| **Référence automatique** | Format `CONG/2025/0001` (séquence par année) |
| **Demi-journée** | Option Matin / Après-midi selon le type de congé |
| **Motif obligatoire** | Configurable par type (minimum 10 caractères) |
| **Pièces jointes** | Upload de certificats médicaux, justificatifs |
| **Chatter** | Historique complet de toutes les transitions avec messages |
| **Tracking** | Tous les champs critiques tracés avec horodatage et auteur |

### 🗂️ Types de Congé
| Type | Code | Jours max | Justificatif |
|---|---|---|---|
| Congé Annuel | CA | 30 | Non |
| Congé Maladie | CM | 90 | **Oui** |
| Congé Maternité | CMat | 98 | **Oui** |
| Congé Exceptionnel | CE | 5 | **Oui** |
| RTT | RTT | 20 | Non |

*Entièrement paramétrables : créez vos propres types en quelques clics.*

### 📊 Allocations et Soldes
- Attribution d'un quota de jours par employé et par type
- Calcul automatique des jours consommés et restants
- Taux d'utilisation en temps réel
- Alerte visuelle si solde faible (< 5 jours)
- Pivot des soldes par employé et par type

### 🔄 Wizards
- **Wizard de refus** : motif obligatoire, applicable à plusieurs demandes
- **Wizard d'annulation groupée** : annulation en masse avec notification optionnelle

### 🖨️ Rapport PDF
- Attestation de congé officielle (disponible uniquement pour les congés approuvés)
- En-tête coloré avec référence et statut
- Informations employé, département, poste
- Dates, durée, type, motif
- Zones de signature employé et RH
- Pied de page avec date d'émission

### 📊 Dashboard
- Graphiques : congés par type, par département
- Tableaux croisés : analyse multidimensionnelle
- Indicateurs de soldes globaux

---

## 🏗️ Architecture technique

```
Couche Modèle (Python/ORM)
    ├── lm.leave.type           → Types de congé paramétrables
    ├── lm.leave.allocation     → Quotas par employé (soldes)
    ├── lm.leave.request        → Demandes (modèle principal)
    ├── lm.leave.refuse.wizard  → TransientModel — Refus avec motif
    └── lm.leave.cancel.wizard  → TransientModel — Annulation groupée

Couche Vue (XML/QWeb)
    ├── Form View               → Formulaire avec bandeaux d'état, smart button
    ├── Tree View               → Liste avec multi-edit et actions rapides
    ├── Kanban View             → Cartes groupées par statut
    ├── Search View             → Filtres, groupby, recherche contextuelle
    ├── Graph View (x2)         → Histogramme et camembert
    ├── Pivot View (x2)         → Demandes et soldes d'allocations
    └── QWeb Report             → Attestation PDF officielle

Couche Sécurité
    ├── group_leave_employee    → Création et consultation de ses propres congés
    └── group_leave_manager     → Approbation, refus, toutes les demandes

Assets Backend
    └── lm_style.css            → Design custom (350+ lignes CSS)
```

---

## 📦 Prérequis et installation

### Prérequis
- Odoo **16.0** (Community ou Enterprise)
- Python **3.10+**
- PostgreSQL **12+**
- Module `employee_management` (ce projet — **obligatoire**)

### Installation

> ⚠️ **Important** : installez d'abord `employee_management` avant `leave_management`.

**1. Cloner les deux modules**
```bash
git clone https://github.com/ramisarivelo/odoo-hr-modules.git
```

**2. Copier dans le dossier addons**
```bash
cp -r employee_management/ /path/to/odoo/addons/
cp -r leave_management/    /path/to/odoo/addons/
```

**3. Configurer odoo.conf**
```ini
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/path/to/your/addons
```

**4. Installer dans l'ordre**
```bash
# 1. D'abord employee_management
./odoo-bin -c odoo.conf -d employee_management_db --install=employee_management

# 2. Puis leave_management
./odoo-bin -c odoo.conf -d leave_management_db --install=leave_management
```

**5. Vérifier**

Après installation, le menu **Congés** doit apparaître dans la barre de navigation. Les 5 types de congé par défaut sont automatiquement créés.

### Mise à jour
```bash
./odoo-bin -c odoo.conf -d leave_management_db --update=leave_management
```

---

## 📁 Structure du module

```
leave_management/
│
├── __init__.py
├── __manifest__.py                       ← Métadonnées, dépendances, fichiers
│
├── models/
│   ├── __init__.py
│   ├── leave_type.py                     ← lm.leave.type
│   ├── leave_allocation.py               ← lm.leave.allocation (soldes)
│   ├── leave_request.py                  ← lm.leave.request (principal)
│   ├── leave_refuse_wizard.py            ← TransientModel : refus
│   └── leave_cancel_wizard.py            ← TransientModel : annulation groupée
│
├── wizard/
│   ├── leave_refuse_wizard_views.xml
│   └── leave_cancel_wizard_views.xml
│
├── views/
│   ├── assets.xml                        ← Injection CSS backend
│   ├── leave_type_views.xml              ← Vues types de congé + wizard refus
│   ├── leave_request_views.xml           ← Form + Tree + Kanban + Search + Actions
│   ├── leave_allocation_views.xml        ← Form + Tree + Search + Actions
│   ├── leave_dashboard_views.xml         ← Graph + Pivot + Actions analytiques
│   └── menu_views.xml                    ← Structure de navigation
│
├── report/
│   ├── leave_report.xml                  ← Action rapport PDF
│   └── leave_report_template.xml         ← Template QWeb attestation
│
├── security/
│   ├── security.xml                      ← Groupes : Employé / Manager RH
│   └── ir.model.access.csv              ← Droits CRUD par modèle et groupe
│
├── data/
│   ├── sequence_data.xml                 ← Séquence CONG/YYYY/NNNN
│   └── leave_type_data.xml              ← 5 types préconfigurés
│
└── static/
    ├── description/index.html            ← Page App Store Odoo
    └── src/css/lm_style.css             ← 350+ lignes CSS custom
```

---

## 🗃️ Modèles de données

### `lm.leave.request` — Demande de Congé (26 champs)

| Champ | Type | Description |
|---|---|---|
| `reference` | `Char` | Référence auto `CONG/2025/0001` (readonly) |
| `employee_id` | `Many2one` | Employé (requis, domaine : actifs uniquement) |
| `department_id` | `Many2one` | Département (related depuis employé, readonly) |
| `leave_type_id` | `Many2one` | Type de congé (requis, domaine : actifs) |
| `date_start` | `Date` | Date de début (requis, tracké) |
| `date_end` | `Date` | Date de fin (requis, tracké) |
| `is_half_day` | `Boolean` | Demi-journée |
| `half_day_period` | `Selection` | Matin / Après-midi |
| `number_of_days` | `Float` | Jours calculés automatiquement (0.5 si demi) |
| `reason` | `Text` | Motif (obligatoire selon type) |
| `attachment_ids` | `Many2many` | Pièces jointes (certificats…) |
| `state` | `Selection` | draft / pending / approved / refused / cancelled |
| `approved_by` | `Many2one` | Utilisateur approbateur |
| `approved_date` | `Datetime` | Horodatage d'approbation |
| `refused_by` | `Many2one` | Utilisateur refusant |
| `refused_date` | `Datetime` | Horodatage de refus |
| `refusal_reason` | `Text` | Motif du refus (saisi via wizard) |
| `cancelled_by` | `Many2one` | Utilisateur annulant |
| `cancelled_date` | `Datetime` | Horodatage d'annulation |
| `submitted_date` | `Datetime` | Horodatage de soumission |
| `is_manager` | `Boolean` | Computed : est-ce un manager (pour UI) |
| `remaining_days` | `Float` | Solde restant avant cette demande |
| `color` | `Integer` | Couleur Kanban (computed depuis state) |

### `lm.leave.allocation` — Allocation de Congé (14 champs)

| Champ | Type | Description |
|---|---|---|
| `display_name` | `Char` | "Employé — Type" (computed, stocké) |
| `employee_id` | `Many2one` | Employé (requis) |
| `department_id` | `Many2one` | Département (related, readonly) |
| `leave_type_id` | `Many2one` | Type de congé (requis) |
| `number_of_days` | `Float` | Jours alloués |
| `date_from` | `Date` | Début de validité (défaut : 1er jan.) |
| `date_to` | `Date` | Fin de validité (défaut : 31 déc.) |
| `state` | `Selection` | draft / approved / refused |
| `note` | `Text` | Justification interne |
| `days_used` | `Float` | Jours consommés (computed) |
| `days_remaining` | `Float` | Solde restant (computed) |
| `usage_percentage` | `Float` | Taux d'utilisation en % (computed) |

### `lm.leave.type` — Type de Congé (12 champs)

| Champ | Type | Description |
|---|---|---|
| `name` | `Char` | Libellé (ex : Congé Annuel) |
| `code` | `Char` | Code court (ex : CA) — unique |
| `sequence` | `Integer` | Ordre d'affichage |
| `color` | `Integer` | Couleur Kanban |
| `max_days` | `Integer` | Maximum de jours par demande (0 = illimité) |
| `requires_justification` | `Boolean` | Motif obligatoire |
| `requires_approval` | `Boolean` | Approbation manager requise |
| `allow_half_day` | `Boolean` | Autoriser les demi-journées |
| `description` | `Text` | Conditions d'utilisation |
| `active` | `Boolean` | Archivage logique |
| `request_count` | `Integer` | Compteur total demandes (computed) |
| `approved_count` | `Integer` | Compteur demandes approuvées (computed) |

---

## 🔁 Workflow et états

```
                    ┌──────────────────────────────────┐
                    │           BROUILLON               │
                    │        (draft — défaut)           │
                    └──────────────┬───────────────────┘
                                   │ [📤 Soumettre]
                    ┌──────────────▼───────────────────┐
                    │          EN ATTENTE               │
                    │           (pending)               │
                    └──────┬──────────────┬────────────┘
                     [✅ Approuver]    [❌ Refuser]
              ┌────────────▼──┐   ┌────────▼───────────┐
              │   APPROUVÉ    │   │      REFUSÉ         │
              │  (approved)   │   │     (refused)       │
              └───────┬───────┘   └────────┬────────────┘
                [🚫 Annuler]          [🔄 Brouillon]
              ┌────────▼───────┐          │
              │    ANNULÉ      │          │
              │  (cancelled)   │◄─────────┘
              └────────────────┘
```

### Transitions et règles

| De | Vers | Action | Qui peut ? | Condition |
|---|---|---|---|---|
| `draft` | `pending` | `action_submit()` | Tout utilisateur | Dates et type renseignés |
| `pending` | `approved` | `action_approve()` | Manager RH | État = pending |
| `pending/approved` | `refused` | `action_refuse()` | Manager RH | Via wizard (motif requis) |
| `pending/approved` | `cancelled` | `action_cancel()` | Employé (pending) / Manager (approved) | — |
| `refused/cancelled` | `draft` | `action_reset_draft()` | Tout utilisateur | État = refused ou cancelled |

### Suppression protégée
```python
def unlink(self):
    for rec in self:
        if rec.state not in ('draft', 'cancelled'):
            raise UserError(
                _('❌ Impossible de supprimer "%s".\n'
                  'Seules les demandes Brouillon ou Annulées peuvent être supprimées.')
                % rec.reference
            )
    return super().unlink()
```

### Messages chatter automatiques

Chaque transition poste automatiquement un message dans le chatter :

```
📤 Demande soumise pour approbation.
   Du 01/07/2025 au 15/07/2025 (15 jours) — Type : Congé Annuel

✅ Demande APPROUVÉE par Admin.
   Congé accordé du 01/07/2025 au 15/07/2025 (15 jours).

❌ Demande REFUSÉE par Admin.
   Motif : Période de pointe, effectifs insuffisants.

🚫 Demande annulée par Admin.
```

---

## 🔐 Sécurité et droits d'accès

### Groupes

| Groupe | XML ID | Description |
|---|---|---|
| **Employé** | `group_leave_employee` | Peut créer, soumettre et voir **ses propres** demandes |
| **Manager RH** | `group_leave_manager` | Peut approuver, refuser, voir **toutes** les demandes, gérer allocations |

Les groupes sont **hiérarchiques** : `group_leave_manager` implique `group_leave_employee`.

L'administrateur système est automatiquement dans le groupe Manager RH.

### Matrice des droits (ACL)

| Modèle | Employé | Manager RH |
|---|---|---|
| `lm.leave.type` | R | R+W+C+D |
| `lm.leave.allocation` | R | R+W+C+D |
| `lm.leave.request` | R+W+C | R+W+C+D |
| `lm.leave.refuse.wizard` | — | R+W+C+D |
| `lm.leave.cancel.wizard` | — | R+W+C+D |

*R=Read, W=Write, C=Create, D=Delete*

### Visibilité conditionnelle dans les vues

| Élément | Visible par |
|---|---|
| Boutons Approuver / Refuser | `group_leave_manager` uniquement |
| Wizard d'annulation groupée | `group_leave_manager` uniquement |
| Menu "Gestion" | `group_leave_manager` uniquement |
| Menu "Reporting" | `group_leave_manager` uniquement |
| Menu "Configuration" | `group_leave_manager` uniquement |
| Section allocations | `group_leave_manager` uniquement |

### Assigner un rôle
```
Paramètres → Utilisateurs → [Utilisateur]
→ Section "Gestion des Congés"
→ Choisir : Employé ou Manager RH
```

---

## 🖥️ Vues et interface

### Form View — Demande de Congé

```
┌─────────────────────────────────────────────────────────────┐
│  [Header] 📤 Soumettre | ✅ Approuver | ❌ Refuser | 🚫 ... │
│           Barre de statut : Brouillon → En attente → Approuvé │
├─────────────────────────────────────────────────────────────┤
│  [Bandeau contextuel coloré selon le statut]                 │
│  ex: ⏳ En attente d'approbation — soumis le 01/06/2025      │
├─────────────────────────────────────────────────────────────┤
│  [Smart Button] 📊 Solde restant : 15 jours                  │
├─────────────────────────────────────────────────────────────┤
│  [Titre] 🏷️ CONG/2025/0023                                  │
├──────────────────────────┬──────────────────────────────────┤
│  👤 Employé et type      │  📅 Période du congé             │
│  - Employé (actifs seul) │  - Date début / fin              │
│  - Département (auto)    │  - Demi-journée (optionnel)      │
│  - Type de congé         │  - Nombre de jours (calculé)     │
├──────────────────────────┴──────────────────────────────────┤
│  📝 Motif de la demande                                      │
├─────────────────────────────────────────────────────────────┤
│  📎 Pièces jointes (visible en mode brouillon)               │
├─────────────────────────────────────────────────────────────┤
│  [Chatter] Historique, activités, messages                   │
└─────────────────────────────────────────────────────────────┘
```

### Bandeaux d'état (design CSS)

| État | Couleur | Message |
|---|---|---|
| `pending` | 🟡 Jaune | ⏳ En attente d'approbation — soumise le [date] |
| `approved` | 🟢 Vert | ✅ Approuvé par [manager] le [date] |
| `refused` | 🔴 Rouge | ❌ Refusé par [manager] — Motif : [raison] |
| `cancelled` | ⬜ Gris | 🚫 Annulé par [utilisateur] |

### Tree View — Colonnes et actions rapides

Colonnes : Référence, Employé, Département, Type, Début, Fin, Jours, Soumis le, Statut (badge coloré)

Actions rapides directement dans la liste :
- ✅ **Approuver** (managers, visible si pending)
- ❌ **Refuser** (managers, visible si pending ou approved)
- 🖨️ **Attestation PDF** (visible si approved)

### Kanban View

Groupement par défaut par **état** (draft / pending / approved / refused / cancelled).

Chaque carte affiche :
- Référence + nombre de jours (en-tête coloré selon état)
- Employé, type de congé, dates
- Badge de statut + activités

### Search View — Filtres disponibles

**Recherche textuelle** : référence, employé, type, département

**Filtres rapides** :
- 📝 Brouillons / ⏳ En attente / ✅ Approuvés / ❌ Refusés / 🚫 Annulés
- Ce mois-ci
- À venir (approuvés avec date future)
- En cours (approuvés avec date active aujourd'hui)

**Groupements** : Statut, Employé, Département, Type, Mois de début

---

## ✅ Validations et contraintes

### Contraintes Python (`@api.constrains`)

| Règle | Champs | Message |
|---|---|---|
| Date fin ≥ date début | `date_start`, `date_end` | `❌ La date de fin ne peut pas être antérieure à la date de début !` |
| Date début non passée (brouillon) | `date_start` | `⚠️ La date de début ne peut pas être dans le passé !` |
| Pas de chevauchement | `date_start`, `date_end`, `employee_id` | `❌ Chevauchement détecté avec : [références]` |
| Motif si justificatif requis | `reason`, `leave_type_id` | `⚠️ Ce type exige un motif détaillé (minimum 10 car.)` |
| Dépassement du maximum | `number_of_days`, `leave_type_id` | `❌ Dépassement du maximum autorisé ! [type] → Limite : X jours` |
| Demi-journée non autorisée | `is_half_day`, `leave_type_id` | `⚠️ Ce type n'autorise pas les demi-journées` |

### Algorithme de détection de chevauchement

```python
@api.constrains('date_start', 'date_end', 'employee_id', 'state')
def _check_overlap(self):
    for rec in self:
        if rec.state in ('cancelled', 'refused'):
            continue  # Les demandes inactives ne bloquent pas
        overlapping = self.search([
            ('employee_id', '=', rec.employee_id.id),
            ('id', '!=', rec.id),
            ('state', 'in', ['pending', 'approved']),  # Uniquement actives
            ('date_start', '<=', rec.date_end),
            ('date_end', '>=', rec.date_start),
        ])
        if overlapping:
            raise ValidationError(...)
```

### Onchange interactifs

| Déclencheur | Comportement |
|---|---|
| Sélection d'un type `requires_justification` | Warning : "📋 Justificatif requis" |
| `date_start` renseignée (sans `date_end`) | Auto-remplit `date_end` = `date_start` |
| `date_end < date_start` | Warning : "⚠️ Dates invalides" |
| `is_half_day = True` | Force `date_end = date_start` |

---

## 📊 Allocations et soldes

### Concept

Une **allocation** définit le quota annuel d'un employé pour un type de congé :

```
Jean Dupont → Congé Annuel → 30 jours → du 01/01/2025 au 31/12/2025
```

### Calcul du solde restant

```python
@api.depends('employee_id', 'leave_type_id', 'number_of_days', 'date_from', 'date_to')
def _compute_days_used(self):
    for rec in self:
        # Congés approuvés sur la période
        leaves = self.env['lm.leave.request'].search([
            ('employee_id', '=', rec.employee_id.id),
            ('leave_type_id', '=', rec.leave_type_id.id),
            ('state', '=', 'approved'),
            ('date_start', '>=', rec.date_from),
            ('date_end', '<=', rec.date_to),
        ])
        used = sum(leaves.mapped('number_of_days'))
        rec.days_used = used
        rec.days_remaining = rec.number_of_days - used
        rec.usage_percentage = (used / rec.number_of_days * 100) if rec.number_of_days else 0
```

### Workflow allocation

```
Brouillon ──[✅ Approuver]──► Approuvé
          └──[❌ Refuser]───► Refusé
```

### Contrainte d'unicité

```python
_sql_constraints = [
    ('unique_allocation',
     'UNIQUE(employee_id, leave_type_id, date_from)',
     'Une allocation pour cet employé et ce type existe déjà sur cette période !'),
]
```

---

## 🔧 Wizards

### Wizard de Refus (`lm.leave.refuse.wizard`)

Popup déclenché par le bouton ❌ Refuser. Permet de :
1. Visualiser les demandes concernées (readonly)
2. Saisir un motif de refus (requis, min. 5 caractères)
3. Appliquer le refus sur toutes les demandes sélectionnées

```python
def action_confirm_refuse(self):
    for leave in self.leave_ids:
        leave.write({
            'state': 'refused',
            'refused_by': self.env.uid,
            'refused_date': fields.Datetime.now(),
            'refusal_reason': self.refusal_reason,
        })
        leave.message_post(body=_('❌ Demande REFUSÉE par %s. Motif : %s') % (...))
```

### Wizard d'Annulation Groupée (`lm.leave.cancel.wizard`)

Popup déclenché via l'action groupée manager. Permet de :
1. Visualiser les demandes à annuler
2. Cocher "Notifier les employés" (défaut : oui)
3. Saisir un motif (requis, min. 5 caractères)
4. Annuler toutes les demandes en une opération atomique

---

## 🖨️ Rapport PDF — Attestation

### Générer une attestation

**Depuis le formulaire** (état = Approuvé) :
```
Bouton "🖨️ Attestation PDF"
```

**Depuis la liste** (action groupée) :
```
Sélectionner les lignes → Action → Attestation de Congé
```

> ℹ️ L'attestation n'est disponible que pour les congés en état `approved`. Une `UserError` est levée sinon.

### Contenu de l'attestation

```
┌─────────────────────────────────────────────────────────┐
│  ATTESTATION DE CONGÉ                    ✅ Approuvé    │
│  Référence : CONG/2025/0023                             │
│  Émise le : 15/06/2025                                  │
├─────────────────────────────────────────────────────────┤
│  👤 Informations de l'employé                           │
│  Nom : Jean Dupont        Matricule : EMP-0042          │
│  Département : IT         Poste : Développeur Odoo      │
├─────────────────────────────────────────────────────────┤
│  📅 Détails du congé                                    │
│  Type : Congé Annuel (CA)                               │
│  Du : 01/07/2025          Au : 15/07/2025               │
│  Durée : 15 jour(s)                                     │
│  Motif : Congés d'été                                   │
├─────────────────────────────────────────────────────────┤
│  ✅ Traitement                                           │
│  Soumis le : 15/06/2025   Statut : ✅ APPROUVÉ          │
│  Approuvé par : Admin     Le : 16/06/2025               │
├─────────────────────────────────────────────────────────┤
│  [Signature employé]      [Cachet et signature RH]      │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Dashboard et statistiques

Accessible via **Congés → Reporting** (managers uniquement).

### Tableau de bord général
- **Vue Graphe** : histogramme des jours de congé approuvés par type
- **Vue Pivot** : département × type avec total de jours

### Congés par département
- **Vue Graphe camembert** : proportion par département
- **Vue Pivot** : analyse par département et mois

### Soldes de congés
- **Vue Pivot** : par type — Alloués | Consommés | Restants
- Identifie rapidement les employés avec un solde épuisé

---

## 🎨 Design CSS custom

Le fichier `static/src/css/lm_style.css` (350+ lignes) est organisé en sections :

### Variables CSS
```css
:root {
    --lm-primary:  #1B4F72;   /* Bleu marine profond */
    --lm-accent:   #2E86C1;   /* Bleu clair */
    --lm-success:  #1E8449;   /* Vert */
    --lm-warning:  #D68910;   /* Orange */
    --lm-danger:   #C0392B;   /* Rouge */
    --lm-purple:   #7D3C98;   /* Violet */
}
```

### Éléments stylisés

| Section | Description |
|---|---|
| **En-tête formulaire** | Dégradé bleu sur le titre, référence en badge blanc |
| **Bandeaux d'état** | Alertes colorées avec bordure latérale (pending/approved/refused/cancelled) |
| **Smart Buttons** | Bordure bleue, animation au hover |
| **Tree View** | Coloration des lignes selon statut |
| **Kanban cards** | En-tête coloré selon statut, corps blanc, hover effect |
| **Badges statut** | Mini-badges colorés avec bordure |
| **Jauges de solde** | Barres de progression vert/orange/rouge |
| **Dashboard KPI** | Tuiles colorées avec valeur large |
| **Rapport PDF** | En-tête dégradé, sections titrées, stamp "Approuvé" |
| **Wizard popup** | En-tête de modal coloré |

---

## 🛠️ Guide de développement

### Ajouter un nouveau type de congé

**Via l'interface** :
```
Congés → Configuration → Types de congé → Nouveau
```

**Via les données XML** (recommandé pour les déploiements) :
```xml
<!-- data/leave_type_data.xml -->
<record id="leave_type_paternity" model="lm.leave.type">
    <field name="name">Congé Paternité</field>
    <field name="code">CPat</field>
    <field name="max_days">10</field>
    <field name="requires_justification">True</field>
    <field name="allows_half_day">False</field>
    <field name="color">11</field>
    <field name="sequence">6</field>
    <field name="description">Congé paternité — 10 jours ouvrables.</field>
</record>
```

### Ajouter un champ à la demande

**1. Modèle Python :**
```python
# models/leave_request.py
urgency = fields.Selection(
    selection=[('low', 'Normale'), ('high', 'Urgente')],
    string='Priorité',
    default='low',
    tracking=True,
)
```

**2. Vue XML :**
```xml
<!-- views/leave_request_views.xml — dans le group approprié -->
<field name="urgency" attrs="{'readonly': [('state', '!=', 'draft')]}"/>
```

**3. Mise à jour :**
```bash
./odoo-bin -c odoo.conf -d leave_management_db --update=leave_management
```

### Ajouter une règle de validation métier

```python
# models/leave_request.py
@api.constrains('employee_id', 'leave_type_id', 'date_start')
def _check_employee_not_on_probation(self):
    """Interdit le congé annuel pendant la période d'essai (3 mois)."""
    from datetime import timedelta
    for rec in self:
        if rec.leave_type_id.code == 'CA' and rec.employee_id.hiring_date:
            probation_end = rec.employee_id.hiring_date + timedelta(days=90)
            if rec.date_start < probation_end:
                raise ValidationError(
                    _('❌ Le congé annuel n\'est pas autorisé pendant '
                      'la période d\'essai (avant le %s).')
                    % probation_end.strftime('%d/%m/%Y')
                )
```

### Personnaliser l'attestation PDF

Le template QWeb se trouve dans `report/leave_report_template.xml` :

```xml
<!-- Ajouter une section après les détails du congé -->
<t t-if="leave.employee_id.seniority > 5">
    <div class="lm-report-section-title">⭐ Prime ancienneté</div>
    <p style="font-size:0.88rem;">
        Cet employé bénéficie de la prime d'ancienneté
        (<t t-esc="leave.employee_id.seniority"/> ans de service).
    </p>
</t>
```

### Bonnes pratiques respectées

```python
# ✅ _() pour l'i18n
raise ValidationError(_('❌ Message traduit'))

# ✅ @api.model_create_multi (Odoo 16)
@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        if vals.get('reference', _('Nouveau')) == _('Nouveau'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('lm.leave.request')
    return super().create(vals_list)

# ✅ has_group() pour vérifier les droits
def action_approve(self):
    self._check_manager_access()
    ...

def _check_manager_access(self):
    if not self.env.user.has_group('leave_management.group_leave_manager'):
        raise UserError(_('⛔ Accès refusé !'))

# ✅ message_post() pour le chatter
rec.message_post(
    body=_('✅ Approuvé par <b>%s</b>.') % self.env.user.name,
    message_type='comment',
    subtype_xmlid='mail.mt_note',
)

# ✅ group_expand pour Kanban par état
@api.model
def _expand_states(self, states, domain, order):
    return [key for key, _ in self._fields['state'].selection]
```

---

## ❓ FAQ

**Q : Le menu "Gestion" n'est pas visible.**
> Attribuez le groupe "Manager RH" à votre utilisateur dans Paramètres → Utilisateurs.

**Q : L'attestation PDF donne une erreur.**
> L'attestation n'est générée que pour les congés `approved`. Vérifiez le statut de la demande.

**Q : Comment désactiver la vérification des dates passées ?**
> Dans `models/leave_request.py`, méthode `_check_dates()` :
> ```python
> # Commentez ces lignes :
> # if rec.state == 'draft' and rec.date_start < date.today():
> #     raise ValidationError(...)
> ```

**Q : Puis-je avoir plusieurs allocations du même type pour le même employé ?**
> Non, par contrainte SQL `UNIQUE(employee_id, leave_type_id, date_from)`. Pour des périodes différentes (années différentes), c'est possible.

**Q : Comment rendre le motif obligatoire pour tous les types ?**
> Activez `requires_justification = True` sur chaque type via Configuration → Types de congé.

**Q : Le module fonctionne-t-il sans `employee_management` ?**
> Non. `leave_management` dépend de `employee_management` pour les modèles `em.employee` et `em.department`. Les deux modules sont conçus pour fonctionner ensemble.

**Q : Comment créer des allocations en masse pour tous les employés ?**
> Utilisez un script Python ou la console Odoo :
> ```python
> employees = env['em.employee'].search([('state', '=', 'active')])
> leave_type = env['lm.leave.type'].search([('code', '=', 'CA')], limit=1)
> for emp in employees:
>     env['lm.leave.allocation'].create({
>         'employee_id': emp.id,
>         'leave_type_id': leave_type.id,
>         'number_of_days': 30,
>         'state': 'approved',
>     })
> ```

---

## 🗺️ Roadmap

- [ ] Intégration avec le calendrier Odoo (affichage des congés)
- [ ] Notifications email automatiques (soumission, approbation, refus)
- [ ] Solde prévisionnel (congés en attente déduits du solde)
- [ ] Règle de cumul progressif (ex: +2.5 jours/mois)
- [ ] Report annuel des soldes non consommés
- [ ] Export Excel des congés par période

---

## 👨‍💻 Auteur

**Votre Nom**
- GitHub : (https://github.com/ramisarivelo)
- LinkedIn : [votre-profil](https://linkedin.com/in/mickael-ramisarivelo)
- Email : ramisarivelomickael@gmail.com

---

## 📄 Licence

Ce module est distribué sous licence **LGPL-3**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🔗 Modules connexes

| Module | Description | Lien |
|---|---|---|
| `employee_management` | Gestion des employés, départements, postes | [Voir le README](../employee_management/README.md) |
| `leave_management` | Ce module | — |

---

<div align="center">

**⭐ Si ce projet vous a aidé, n'hésitez pas à laisser une étoile sur GitHub !**

*Développé avec ❤️ — Projet Odoo complet pour démonstration professionnelle*

</div>
