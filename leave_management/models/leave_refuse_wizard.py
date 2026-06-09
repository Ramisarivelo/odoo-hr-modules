# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class LeaveRefuseWizard(models.TransientModel):
    """
    Wizard (popup) pour saisir le motif de refus d'une demande de congé.
    TransientModel = modèle temporaire, non stocké en base.
    """
    _name = 'lm.leave.refuse.wizard'
    _description = 'Wizard : Refus de congé'

    leave_ids = fields.Many2many(
        comodel_name='lm.leave.request',
        string='Demandes à refuser',
    )
    refusal_reason = fields.Text(
        string='Motif du refus',
        required=True,
        help='Expliquez pourquoi la demande est refusée. Ce message sera visible par l\'employé.',
    )

    @api.constrains('refusal_reason')
    def _check_reason(self):
        for rec in self:
            if not rec.refusal_reason or len(rec.refusal_reason.strip()) < 5:
                raise UserError(_('⚠️ Veuillez saisir un motif de refus clair (minimum 5 caractères).'))

    def action_confirm_refuse(self):
        """Confirme le refus avec le motif saisi."""
        for leave in self.leave_ids:
            leave.write({
                'state': 'refused',
                'refused_by': self.env.uid,
                'refused_date': fields.Datetime.now(),
                'refusal_reason': self.refusal_reason,
            })
            leave.message_post(
                body=_('❌ Demande de congé <strong>REFUSÉE</strong> par %s.\n'
                       '<b>Motif :</b> %s') % (
                    self.env.user.name,
                    self.refusal_reason,
                ),
                message_type='comment',
                subtype_xmlid='mail.mt_note',
            )
        return {'type': 'ir.actions.act_window_close'}
