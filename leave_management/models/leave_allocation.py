# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class LeaveAllocation(models.Model):
    """
    Allocation de congé : attribue un quota de jours à un employé
    pour un type de congé donné sur une période.

    Exemple : Jean Dupont → Congé Annuel → 30 jours → Année 2025
    """
    _name = 'lm.leave.allocation'
    _description = 'Allocation de Congé'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'employee_id, leave_type_id, date_from desc'
    _rec_name = 'display_name'

    # ── Identification ────────────────────────────────────────────────────────
    display_name = fields.Char(
        string='Libellé',
        compute='_compute_display_name',
        store=True,
    )
    employee_id = fields.Many2one(
        'em.employee', string='Employé',
        required=True, tracking=True, ondelete='cascade',
        domain=[('state', '=', 'active')],
    )
    department_id = fields.Many2one(
        'em.department', string='Département',
        related='employee_id.department_id', store=True, readonly=True,
    )
    leave_type_id = fields.Many2one(
        'lm.leave.type', string='Type de congé',
        required=True, tracking=True, ondelete='restrict',
        domain=[('active', '=', True)],
    )
    number_of_days = fields.Float(
        string='Jours alloués',
        required=True,
        tracking=True,
        digits=(10, 1),
    )
    date_from = fields.Date(
        string='Début de validité',
        required=True,
        default=lambda self: fields.Date.today().replace(month=1, day=1),
        tracking=True,
    )
    date_to = fields.Date(
        string='Fin de validité',
        required=True,
        default=lambda self: fields.Date.today().replace(month=12, day=31),
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('approved', 'Approuvé'),
            ('refused', 'Refusé'),
        ],
        string='Statut',
        default='draft',
        required=True,
        tracking=True,
        copy=False,
    )
    note = fields.Text(string='Note / Justification')

    # ── Computed ──────────────────────────────────────────────────────────────
    days_used = fields.Float(
        string='Jours consommés',
        compute='_compute_days_used',
        store=False,
        help='Jours déjà pris (congés approuvés) sur cette période.',
    )
    days_remaining = fields.Float(
        string='Solde restant',
        compute='_compute_days_used',
        store=False,
        digits=(10, 1),
    )
    usage_percentage = fields.Float(
        string='Taux d\'utilisation (%)',
        compute='_compute_days_used',
        store=False,
    )

    @api.depends('employee_id', 'leave_type_id')
    def _compute_display_name(self):
        for rec in self:
            emp = rec.employee_id.name or '?'
            lt = rec.leave_type_id.name or '?'
            rec.display_name = '%s — %s' % (emp, lt)

    @api.depends('employee_id', 'leave_type_id', 'number_of_days', 'date_from', 'date_to')
    def _compute_days_used(self):
        for rec in self:
            if not rec.employee_id or not rec.leave_type_id:
                rec.days_used = 0.0
                rec.days_remaining = rec.number_of_days
                rec.usage_percentage = 0.0
                continue
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
            rec.usage_percentage = (used / rec.number_of_days * 100) if rec.number_of_days else 0.0

    # ── Contraintes ───────────────────────────────────────────────────────────
    @api.constrains('number_of_days')
    def _check_days(self):
        for rec in self:
            if rec.number_of_days <= 0:
                raise ValidationError(_('❌ Le nombre de jours alloués doit être supérieur à 0 !'))

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for rec in self:
            if rec.date_from and rec.date_to and rec.date_to < rec.date_from:
                raise ValidationError(_('❌ La date de fin doit être postérieure à la date de début !'))

    # ── Actions ───────────────────────────────────────────────────────────────
    def action_approve(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Seules les allocations en brouillon peuvent être approuvées.'))
        self.write({'state': 'approved'})
        self.message_post(
            body=_('✅ Allocation approuvée par <b>%s</b>.') % self.env.user.name,
            message_type='comment',
            subtype_xmlid='mail.mt_note',
        )

    def action_refuse(self):
        for rec in self:
            if rec.state == 'refused':
                raise UserError(_('Cette allocation est déjà refusée.'))
        self.write({'state': 'refused'})
        self.message_post(
            body=_('❌ Allocation refusée par <b>%s</b>.') % self.env.user.name,
            message_type='comment',
            subtype_xmlid='mail.mt_note',
        )

    def action_reset_draft(self):
        self.write({'state': 'draft'})

    _sql_constraints = [
        ('unique_allocation',
         'UNIQUE(employee_id, leave_type_id, date_from)',
         'Une allocation pour cet employé et ce type de congé existe déjà sur cette période !'),
    ]
