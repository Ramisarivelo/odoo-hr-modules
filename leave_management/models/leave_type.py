# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LeaveType(models.Model):
    """
    Type de congé : Congé annuel, maladie, maternité, etc.
    Permet de configurer les règles pour chaque catégorie de congé.
    """
    _name = 'lm.leave.type'
    _description = 'Type de Congé'
    _order = 'sequence asc, name asc'

    name = fields.Char(
        string='Libellé',
        required=True,
    )
    code = fields.Char(
        string='Code',
        size=10,
        required=True,
    )
    sequence = fields.Integer(
        string='Séquence',
        default=10,
    )
    color = fields.Integer(
        string='Couleur',
        default=0,
    )
    max_days = fields.Integer(
        string='Jours maximum par an',
        default=30,
        help='Nombre maximum de jours autorisés par an pour ce type de congé. 0 = illimité.',
    )
    requires_justification = fields.Boolean(
        string='Justificatif requis',
        default=False,
        help='Si coché, un motif détaillé est obligatoire.',
    )
    requires_approval = fields.Boolean(
        string='Approbation requise',
        default=True,
    )
    description = fields.Text(
        string='Description',
    )
    active = fields.Boolean(
        string='Actif',
        default=True,
    )
    request_ids = fields.One2many(
        comodel_name='lm.leave.request',
        inverse_name='leave_type_id',
        string='Demandes',
    )
    request_count = fields.Integer(
        string='Nombre de demandes',
        compute='_compute_request_count',
    )

    @api.depends('request_ids')
    def _compute_request_count(self):
        for rec in self:
            rec.request_count = len(rec.request_ids)

    @api.constrains('max_days')
    def _check_max_days(self):
        for rec in self:
            if rec.max_days < 0:
                raise ValidationError('Le nombre maximum de jours ne peut pas être négatif !')

    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'Le code du type de congé doit être unique !'),
    ]
