# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import date
import re


class Employee(models.Model):
    """
    Modèle principal : Employé.
    Gère le cycle de vie complet d'un employé dans l'entreprise.
    """
    _name = 'em.employee'
    _description = 'Employé'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'
    _rec_name = 'name'

    # ══════════════════════════════════════════════════════════════════
    #  CHAMPS IDENTITÉ
    # ══════════════════════════════════════════════════════════════════
    name = fields.Char(
        string='Nom complet',
        required=True,
        tracking=True,
    )
    employee_ref = fields.Char(
        string='Matricule',
        copy=False,
        readonly=True,
        default=lambda self: _('Nouveau'),
        index=True,
    )
    image = fields.Binary(
        string='Photo',
        attachment=True,
    )
    image_128 = fields.Binary(
        string='Photo (miniature)',
        attachment=True,
        compute='_compute_image_128',
        store=True,
    )

    # ══════════════════════════════════════════════════════════════════
    #  INFORMATIONS PERSONNELLES
    # ══════════════════════════════════════════════════════════════════
    gender = fields.Selection(
        selection=[
            ('male', 'Masculin'),
            ('female', 'Féminin'),
            ('other', 'Autre'),
        ],
        string='Genre',
        tracking=True,
    )
    date_of_birth = fields.Date(
        string='Date de naissance',
    )
    age = fields.Integer(
        string='Âge',
        compute='_compute_age',
        store=True,
    )
    marital_status = fields.Selection(
        selection=[
            ('single', 'Célibataire'),
            ('married', 'Marié(e)'),
            ('divorced', 'Divorcé(e)'),
            ('widowed', 'Veuf/Veuve'),
        ],
        string='Situation familiale',
        default='single',
    )
    children_count = fields.Integer(
        string='Nombre d\'enfants',
        default=0,
    )
    nationality = fields.Char(
        string='Nationalité',
        default='Malgache',
    )
    cin = fields.Char(
        string='CIN',
        size=12,
    )
    cin_date = fields.Date(
        string='Date délivrance CIN',
    )
    address = fields.Text(
        string='Adresse complète',
    )
    phone = fields.Char(
        string='Téléphone',
    )
    mobile = fields.Char(
        string='Mobile',
    )
    email = fields.Char(
        string='Email professionnel',
        tracking=True,
    )
    email_personal = fields.Char(
        string='Email personnel',
    )

    # ══════════════════════════════════════════════════════════════════
    #  INFORMATIONS PROFESSIONNELLES
    # ══════════════════════════════════════════════════════════════════
    department_id = fields.Many2one(
        comodel_name='em.department',
        string='Département',
        required=True,
        tracking=True,
        ondelete='restrict',
    )
    job_position_id = fields.Many2one(
        comodel_name='em.job.position',
        string='Poste',
        required=True,
        tracking=True,
        domain="[('department_id', 'in', [department_id, False])]",
    )
    manager_id = fields.Many2one(
        comodel_name='em.employee',
        string='Manager direct',
        tracking=True,
        domain="[('state', '=', 'active'), ('id', '!=', id)]",
    )
    subordinate_ids = fields.One2many(
        comodel_name='em.employee',
        inverse_name='manager_id',
        string='Subordonnés',
    )
    subordinate_count = fields.Integer(
        string='Équipe',
        compute='_compute_subordinate_count',
    )
    hiring_date = fields.Date(
        string='Date d\'embauche',
        required=True,
        default=fields.Date.today,
        tracking=True,
    )
    end_date = fields.Date(
        string='Date de fin de contrat',
        tracking=True,
        help='Laisser vide pour un CDI ou un contrat sans terme fixé.',
    )
    seniority = fields.Integer(
        string='Ancienneté (années)',
        compute='_compute_seniority',
        store=True,
    )
    seniority_months = fields.Integer(
        string='Ancienneté (mois)',
        compute='_compute_seniority',
    )
    contract_type = fields.Selection(
        selection=[
            ('cdi', 'CDI — Contrat à Durée Indéterminée'),
            ('cdd', 'CDD — Contrat à Durée Déterminée'),
            ('interim', 'Intérim'),
            ('stage', 'Stage'),
            ('apprentissage', 'Apprentissage'),
            ('consultant', 'Consultant / Freelance'),
        ],
        string='Type de contrat',
        default='cdi',
        required=True,
        tracking=True,
    )
    salary = fields.Float(
        string='Salaire brut (Ar)',
        digits=(16, 0),
        required=True,
        tracking=True,
    )
    salary_net = fields.Float(
        string='Salaire net estimé (Ar)',
        digits=(16, 0),
        compute='_compute_salary_net',
        help='Estimation : salaire brut — 23% de charges sociales (CNAPS + OSIE).',
    )
    bank_account = fields.Char(
        string='RIB / Compte bancaire',
    )
    work_location = fields.Selection(
        selection=[
            ('office', 'Présentiel'),
            ('remote', 'Télétravail'),
            ('hybrid', 'Hybride'),
        ],
        string='Lieu de travail',
        default='office',
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('active', 'Actif'),
            ('suspended', 'Suspendu'),
            ('resigned', 'Démissionné'),
        ],
        string='Statut',
        default='draft',
        tracking=True,
        required=True,
        group_expand='_expand_states',
    )
    note = fields.Text(
        string='Notes internes',
    )
    skills = fields.Text(
        string='Compétences',
        help='Liste des compétences et certifications.',
    )
    # Badge couleur selon l'état (pour Kanban)
    color = fields.Integer(
        string='Couleur',
        compute='_compute_color',
    )
    kanban_state = fields.Selection(
        selection=[
            ('normal', 'En cours'),
            ('done', 'Prêt'),
            ('blocked', 'Bloqué'),
        ],
        string='État Kanban',
        default='normal',
    )

    # ══════════════════════════════════════════════════════════════════
    #  COMPUTED FIELDS
    # ══════════════════════════════════════════════════════════════════
    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for emp in self:
            if emp.date_of_birth:
                emp.age = today.year - emp.date_of_birth.year - (
                    (today.month, today.day) < (emp.date_of_birth.month, emp.date_of_birth.day)
                )
            else:
                emp.age = 0

    @api.depends('hiring_date')
    def _compute_seniority(self):
        today = date.today()
        for emp in self:
            if emp.hiring_date:
                years = today.year - emp.hiring_date.year - (
                    (today.month, today.day) < (emp.hiring_date.month, emp.hiring_date.day)
                )
                months = (today.year - emp.hiring_date.year) * 12 + (today.month - emp.hiring_date.month)
                emp.seniority = max(years, 0)
                emp.seniority_months = max(months, 0)
            else:
                emp.seniority = 0
                emp.seniority_months = 0

    @api.depends('salary')
    def _compute_salary_net(self):
        """Estimation du salaire net : brut - 23% charges (CNAPS 1% + OSIE 5% + IR)."""
        for emp in self:
            emp.salary_net = emp.salary * 0.77 if emp.salary else 0.0

    @api.depends('subordinate_ids')
    def _compute_subordinate_count(self):
        for emp in self:
            emp.subordinate_count = len(emp.subordinate_ids)

    @api.depends('image')
    def _compute_image_128(self):
        for emp in self:
            emp.image_128 = emp.image  # Odoo gère le redimensionnement

    @api.depends('state')
    def _compute_color(self):
        mapping = {'draft': 0, 'active': 10, 'suspended': 3, 'resigned': 1}
        for emp in self:
            emp.color = mapping.get(emp.state, 0)

    @api.model
    def _expand_states(self, states, domain, order):
        return [key for key, _ in self._fields['state'].selection]

    # ══════════════════════════════════════════════════════════════════
    #  CONTRAINTES
    # ══════════════════════════════════════════════════════════════════
    @api.constrains('salary')
    def _check_salary(self):
        for emp in self:
            if emp.salary < 0:
                raise ValidationError(_('❌ Le salaire ne peut pas être négatif !'))
            if emp.salary > 0 and emp.salary < 348_000:
                # SMIG Madagascar 2024
                raise ValidationError(
                    _('⚠️ Le salaire (%.0f Ar) est inférieur au SMIG (348 000 Ar) !') % emp.salary
                )

    @api.constrains('email')
    def _check_email(self):
        pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
        for emp in self:
            if emp.email and not re.match(pattern, emp.email):
                raise ValidationError(_('❌ Adresse email invalide : %s') % emp.email)

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for emp in self:
            if emp.date_of_birth:
                if emp.date_of_birth > date.today():
                    raise ValidationError(_('❌ La date de naissance ne peut pas être dans le futur !'))
                if emp.age < 16:
                    raise ValidationError(_('❌ L\'employé doit avoir au moins 16 ans.'))

    @api.constrains('hiring_date', 'end_date')
    def _check_contract_dates(self):
        for emp in self:
            if emp.end_date and emp.hiring_date and emp.end_date < emp.hiring_date:
                raise ValidationError(_('❌ La date de fin de contrat ne peut pas être avant la date d\'embauche !'))

    @api.constrains('children_count')
    def _check_children(self):
        for emp in self:
            if emp.children_count < 0:
                raise ValidationError(_('❌ Le nombre d\'enfants ne peut pas être négatif !'))

    @api.constrains('cin')
    def _check_cin_unique(self):
        for emp in self:
            if emp.cin:
                duplicate = self.search([('cin', '=', emp.cin), ('id', '!=', emp.id)])
                if duplicate:
                    raise ValidationError(
                        _('❌ Le numéro CIN "%s" est déjà utilisé par %s.') % (emp.cin, duplicate[0].name)
                    )

    # ══════════════════════════════════════════════════════════════════
    #  ONCHANGE
    # ══════════════════════════════════════════════════════════════════
    @api.onchange('department_id')
    def _onchange_department_id(self):
        """Réinitialise le poste si le département change."""
        if self.department_id and self.job_position_id:
            if self.job_position_id.department_id and \
               self.job_position_id.department_id != self.department_id:
                self.job_position_id = False
                return {
                    'warning': {
                        'title': '⚠️ Poste réinitialisé',
                        'message': 'Le poste a été vidé car il n\'appartient pas au nouveau département.',
                    }
                }

    @api.onchange('contract_type')
    def _onchange_contract_type(self):
        if self.contract_type == 'cdi':
            self.end_date = False

    # ══════════════════════════════════════════════════════════════════
    #  ORM OVERRIDES
    # ══════════════════════════════════════════════════════════════════
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('employee_ref', _('Nouveau')) == _('Nouveau'):
                vals['employee_ref'] = (
                    self.env['ir.sequence'].next_by_code('em.employee') or 'EMP-0001'
                )
        return super().create(vals_list)

    def unlink(self):
        for emp in self:
            if emp.state == 'active':
                raise UserError(
                    _('❌ Impossible de supprimer un employé actif (%s).\n'
                      'Veuillez d\'abord le désactiver ou le marquer comme démissionné.') % emp.name
                )
        return super().unlink()

    def copy(self, default=None):
        default = dict(default or {})
        default['employee_ref'] = _('Nouveau')
        default['name'] = _('%s (copie)') % self.name
        return super().copy(default)

    # ══════════════════════════════════════════════════════════════════
    #  WORKFLOW BUTTONS
    # ══════════════════════════════════════════════════════════════════
    def action_activate(self):
        for emp in self:
            if emp.state == 'active':
                raise UserError(_('Cet employé est déjà actif.'))
        self.write({'state': 'active'})
        self.message_post(
            body=_('✅ Employé <b>activé</b> par %s.') % self.env.user.name,
            message_type='comment',
            subtype_xmlid='mail.mt_note',
        )

    def action_suspend(self):
        for emp in self:
            if emp.state != 'active':
                raise UserError(_('Seuls les employés actifs peuvent être suspendus.'))
        self.write({'state': 'suspended'})
        self.message_post(
            body=_('⚠️ Employé <b>suspendu</b> par %s.') % self.env.user.name,
            message_type='comment',
            subtype_xmlid='mail.mt_note',
        )

    def action_resign(self):
        for emp in self:
            if emp.state not in ('active', 'suspended'):
                raise UserError(_('Seuls les employés actifs ou suspendus peuvent être marqués comme démissionnaires.'))
        self.write({'state': 'resigned'})
        self.message_post(
            body=_('🚪 Employé marqué <b>démissionnaire</b> par %s.') % self.env.user.name,
            message_type='comment',
            subtype_xmlid='mail.mt_note',
        )

    def action_reset_draft(self):
        self.write({'state': 'draft'})
        self.message_post(
            body=_('🔄 Fiche remise en <b>brouillon</b> par %s.') % self.env.user.name,
            message_type='comment',
            subtype_xmlid='mail.mt_note',
        )

    def action_print_card(self):
        """Imprime la fiche PDF de l'employé."""
        return self.env.ref('employee_management.action_report_employee_card').report_action(self)

    def action_transfer_wizard(self):
        """Ouvre le wizard de mutation de département."""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Mutation / Transfert'),
            'res_model': 'em.transfer.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_employee_ids': self.ids,
                'default_current_department_id': self.department_id.id if len(self) == 1 else False,
            },
        }
