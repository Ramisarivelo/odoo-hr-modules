# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import date, timedelta


class LeaveRequest(models.Model):
    """
    Demande de congé — modèle principal.

    Workflow :
        draft ──[Soumettre]──► pending ──[Approuver]──► approved
                                       └─[Refuser]───► refused
        (depuis pending/approved/refused) ──[Annuler]──► cancelled
        (depuis pending/approved/refused) ──[Reset]────► draft
    """
    _name = 'lm.leave.request'
    _description = 'Demande de Congé'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, id desc'
    _rec_name = 'reference'

    # ─── Identification ───────────────────────────────────────────────────────
    reference = fields.Char(
        string='Référence',
        default=_('Nouveau'),
        copy=False,
        readonly=True,
        tracking=True,
    )

    # ─── Informations principales ─────────────────────────────────────────────
    employee_id = fields.Many2one(
        comodel_name='em.employee',
        string='Employé',
        required=True,
        tracking=True,
        ondelete='cascade',
        default=lambda self: self._get_default_employee(),
    )
    department_id = fields.Many2one(
        comodel_name='em.department',
        string='Département',
        related='employee_id.department_id',
        store=True,
        readonly=True,
    )
    leave_type_id = fields.Many2one(
        comodel_name='lm.leave.type',
        string='Type de congé',
        required=True,
        tracking=True,
        ondelete='restrict',
    )
    date_start = fields.Date(
        string='Date de début',
        required=True,
        tracking=True,
    )
    date_end = fields.Date(
        string='Date de fin',
        required=True,
        tracking=True,
    )
    number_of_days = fields.Integer(
        string='Nombre de jours',
        compute='_compute_number_of_days',
        store=True,
        readonly=True,
    )
    reason = fields.Text(
        string='Motif',
        tracking=True,
        help='Expliquez la raison de votre demande de congé.',
    )
    attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        relation='lm_leave_attachment_rel',
        column1='leave_id',
        column2='attachment_id',
        string='Pièces jointes',
        help='Justificatifs (certificat médical, etc.)',
    )

    # ─── Approbation ─────────────────────────────────────────────────────────
    state = fields.Selection(
        selection=[
            ('draft', 'Brouillon'),
            ('pending', 'En attente'),
            ('approved', 'Approuvé'),
            ('refused', 'Refusé'),
            ('cancelled', 'Annulé'),
        ],
        string='Statut',
        default='draft',
        required=True,
        tracking=True,
        copy=False,
    )
    approved_by = fields.Many2one(
        comodel_name='res.users',
        string='Approuvé par',
        readonly=True,
        copy=False,
        tracking=True,
    )
    approved_date = fields.Datetime(
        string='Date d\'approbation',
        readonly=True,
        copy=False,
    )
    refused_by = fields.Many2one(
        comodel_name='res.users',
        string='Refusé par',
        readonly=True,
        copy=False,
        tracking=True,
    )
    refused_date = fields.Datetime(
        string='Date de refus',
        readonly=True,
        copy=False,
    )
    refusal_reason = fields.Text(
        string='Motif du refus',
        readonly=True,
        copy=False,
        tracking=True,
    )
    submitted_date = fields.Datetime(
        string='Date de soumission',
        readonly=True,
        copy=False,
    )

    # ─── Computed / helpers ───────────────────────────────────────────────────
    is_manager = fields.Boolean(
        string='Est manager',
        compute='_compute_is_manager',
    )

    def _get_default_employee(self):
        """Pré-rempli avec l'employé lié à l'utilisateur connecté."""
        employee = self.env['em.employee'].search(
            [('state', '=', 'active')], limit=1
        )
        return employee

    @api.depends('date_start', 'date_end')
    def _compute_number_of_days(self):
        for rec in self:
            if rec.date_start and rec.date_end:
                delta = (rec.date_end - rec.date_start).days + 1
                rec.number_of_days = max(delta, 0)
            else:
                rec.number_of_days = 0

    def _compute_is_manager(self):
        is_mgr = self.env.user.has_group('leave_management.group_leave_manager')
        for rec in self:
            rec.is_manager = is_mgr

    # ─── Contraintes de validation ────────────────────────────────────────────
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_start and rec.date_end:
                # 1. Date de fin >= Date de début
                if rec.date_end < rec.date_start:
                    raise ValidationError(
                        _('❌ La date de fin ne peut pas être antérieure à la date de début !')
                    )
                # 2. Pas dans le passé (sauf si déjà approuvé)
                if rec.state == 'draft' and rec.date_start < date.today():
                    raise ValidationError(
                        _('⚠️ La date de début ne peut pas être dans le passé !')
                    )

    @api.constrains('date_start', 'date_end', 'employee_id', 'state')
    def _check_overlap(self):
        """Vérifie qu'il n'existe pas de chevauchement avec une autre demande approuvée ou en attente."""
        for rec in self:
            if rec.state in ('cancelled', 'refused'):
                continue
            if not rec.date_start or not rec.date_end:
                continue
            overlapping = self.search([
                ('employee_id', '=', rec.employee_id.id),
                ('id', '!=', rec.id),
                ('state', 'in', ['pending', 'approved']),
                ('date_start', '<=', rec.date_end),
                ('date_end', '>=', rec.date_start),
            ])
            if overlapping:
                refs = ', '.join(overlapping.mapped('reference'))
                raise ValidationError(
                    _('❌ Chevauchement détecté avec la/les demande(s) : %s\n'
                      'Un employé ne peut pas avoir deux demandes qui se chevauchent.') % refs
                )

    @api.constrains('reason', 'leave_type_id')
    def _check_reason_required(self):
        for rec in self:
            if rec.leave_type_id and rec.leave_type_id.requires_justification:
                if not rec.reason or len(rec.reason.strip()) < 10:
                    raise ValidationError(
                        _('⚠️ Ce type de congé (%s) nécessite un motif détaillé (minimum 10 caractères) !')
                        % rec.leave_type_id.name
                    )

    @api.constrains('number_of_days', 'leave_type_id')
    def _check_max_days(self):
        for rec in self:
            if not rec.leave_type_id or not rec.leave_type_id.max_days:
                continue
            if rec.number_of_days > rec.leave_type_id.max_days:
                raise ValidationError(
                    _('❌ Vous dépassez le maximum autorisé !\n'
                      'Type : %s → Maximum : %s jours\n'
                      'Votre demande : %s jours')
                    % (rec.leave_type_id.name, rec.leave_type_id.max_days, rec.number_of_days)
                )

    # ─── Onchange ────────────────────────────────────────────────────────────
    @api.onchange('leave_type_id')
    def _onchange_leave_type(self):
        if self.leave_type_id and self.leave_type_id.requires_justification:
            return {
                'warning': {
                    'title': '📋 Justificatif requis',
                    'message': 'Ce type de congé nécessite un motif détaillé et éventuellement une pièce jointe (ex: certificat médical).',
                }
            }

    @api.onchange('date_start')
    def _onchange_date_start(self):
        """Propose automatiquement une date de fin = date de début."""
        if self.date_start and not self.date_end:
            self.date_end = self.date_start

    @api.onchange('date_start', 'date_end')
    def _onchange_dates_warning(self):
        if self.date_start and self.date_end and self.date_end < self.date_start:
            return {
                'warning': {
                    'title': '⚠️ Dates invalides',
                    'message': 'La date de fin est antérieure à la date de début !',
                }
            }

    # ─── ORM overrides ───────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', _('Nouveau')) == _('Nouveau'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('lm.leave.request') or 'CONG-0001'
        return super().create(vals_list)

    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'cancelled'):
                raise UserError(
                    _('❌ Impossible de supprimer la demande "%s".\n'
                      'Seules les demandes en état "Brouillon" ou "Annulé" peuvent être supprimées.')
                    % rec.reference
                )
        return super().unlink()

    # ─── Workflow : boutons d'action ──────────────────────────────────────────
    def action_submit(self):
        """Brouillon → En attente"""
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Seules les demandes en brouillon peuvent être soumises.'))
            if not rec.date_start or not rec.date_end:
                raise UserError(_('❌ Veuillez renseigner les dates de début et de fin avant de soumettre.'))
            if not rec.leave_type_id:
                raise UserError(_('❌ Veuillez choisir un type de congé avant de soumettre.'))
            rec.write({
                'state': 'pending',
                'submitted_date': fields.Datetime.now(),
            })
            rec.message_post(
                body=_('📤 Demande de congé soumise pour approbation.\n'
                       '📅 Du %s au %s (%s jours) — Type : %s') % (
                    rec.date_start.strftime('%d/%m/%Y'),
                    rec.date_end.strftime('%d/%m/%Y'),
                    rec.number_of_days,
                    rec.leave_type_id.name,
                ),
                message_type='comment',
                subtype_xmlid='mail.mt_note',
            )

    def action_approve(self):
        """En attente → Approuvé"""
        self._check_manager_access()
        for rec in self:
            if rec.state != 'pending':
                raise UserError(_('Seules les demandes "En attente" peuvent être approuvées.'))
            rec.write({
                'state': 'approved',
                'approved_by': self.env.uid,
                'approved_date': fields.Datetime.now(),
            })
            rec.message_post(
                body=_('✅ Demande de congé <strong>APPROUVÉE</strong> par %s.\n'
                       'Congé accordé du %s au %s (%s jours).') % (
                    self.env.user.name,
                    rec.date_start.strftime('%d/%m/%Y'),
                    rec.date_end.strftime('%d/%m/%Y'),
                    rec.number_of_days,
                ),
                message_type='comment',
                subtype_xmlid='mail.mt_note',
            )

    def action_refuse(self):
        """En attente / Approuvé → Refusé — ouvre un wizard pour saisir le motif."""
        self._check_manager_access()
        for rec in self:
            if rec.state not in ('pending', 'approved'):
                raise UserError(_('Seules les demandes "En attente" ou "Approuvées" peuvent être refusées.'))
        # Ouvre le wizard de refus
        return {
            'type': 'ir.actions.act_window',
            'name': _('Motif du refus'),
            'res_model': 'lm.leave.refuse.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_leave_ids': self.ids},
        }

    def action_cancel(self):
        """Annulation par l'employé (si encore modifiable)."""
        for rec in self:
            if rec.state == 'approved':
                # Un employé ne peut pas annuler lui-même un congé déjà approuvé
                if not self.env.user.has_group('leave_management.group_leave_manager'):
                    raise UserError(
                        _('❌ Votre congé est déjà approuvé.\n'
                          'Veuillez contacter votre manager pour l\'annuler.')
                    )
            if rec.state == 'draft':
                raise UserError(_('Une demande en brouillon peut simplement être supprimée.'))
            rec.write({'state': 'cancelled'})
            rec.message_post(
                body=_('🚫 Demande de congé annulée par %s.') % self.env.user.name,
                message_type='comment',
                subtype_xmlid='mail.mt_note',
            )

    def action_reset_draft(self):
        """Retour en brouillon (depuis refusé ou annulé)."""
        for rec in self:
            if rec.state not in ('refused', 'cancelled'):
                raise UserError(_('Seules les demandes "Refusées" ou "Annulées" peuvent être remises en brouillon.'))
            rec.write({
                'state': 'draft',
                'approved_by': False,
                'approved_date': False,
                'refused_by': False,
                'refused_date': False,
                'refusal_reason': False,
            })
            rec.message_post(
                body=_('🔄 Demande remise en brouillon par %s.') % self.env.user.name,
                message_type='comment',
                subtype_xmlid='mail.mt_note',
            )

    # ─── Méthode interne ──────────────────────────────────────────────────────
    def _check_manager_access(self):
        if not self.env.user.has_group('leave_management.group_leave_manager'):
            raise UserError(
                _('⛔ Accès refusé !\nSeuls les managers RH peuvent approuver ou refuser les demandes de congé.')
            )
