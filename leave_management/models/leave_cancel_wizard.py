# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LeaveCancelWizard(models.TransientModel):
    """
    Wizard d'annulation groupée : permet à un manager d'annuler
    plusieurs demandes approuvées ou en attente en une seule opération.
    """
    _name = 'lm.leave.cancel.wizard'
    _description = 'Wizard : Annulation groupée de congés'

    leave_ids = fields.Many2many(
        comodel_name='lm.leave.request',
        string='Demandes à annuler',
        readonly=True,
    )
    cancellation_reason = fields.Text(
        string='Motif de l\'annulation',
        required=True,
        help='Expliquez pourquoi ces congés sont annulés. Ce message sera visible dans le chatter.',
    )
    notify_employees = fields.Boolean(
        string='Notifier les employés',
        default=True,
        help='Envoie un message dans le chatter de chaque demande annulée.',
    )

    @api.constrains('cancellation_reason')
    def _check_reason(self):
        for rec in self:
            if not rec.cancellation_reason or len(rec.cancellation_reason.strip()) < 5:
                raise ValidationError(
                    _('⚠️ Le motif d\'annulation doit contenir au moins 5 caractères.')
                )

    def action_confirm_cancel(self):
        """Annule toutes les demandes sélectionnées."""
        for leave in self.leave_ids:
            if leave.state in ('draft',):
                continue  # Les brouillons ne sont pas concernés
            leave.write({
                'state': 'cancelled',
                'cancelled_by': self.env.uid,
                'cancelled_date': fields.Datetime.now(),
            })
            if self.notify_employees:
                leave.message_post(
                    body=_(
                        '🚫 Demande <b>ANNULÉE</b> par <b>%s</b>.<br/>'
                        '<b>Motif :</b> %s'
                    ) % (self.env.user.name, self.cancellation_reason),
                    message_type='comment',
                    subtype_xmlid='mail.mt_note',
                )
        return {'type': 'ir.actions.act_window_close'}
