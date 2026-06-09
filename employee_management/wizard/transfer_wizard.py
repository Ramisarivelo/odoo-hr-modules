# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TransferWizard(models.TransientModel):
    """
    Wizard de mutation : change le département et/ou le poste
    d'un ou plusieurs employés en une seule opération.
    """
    _name = 'em.transfer.wizard'
    _description = 'Wizard : Mutation / Transfert d\'employé'

    employee_ids = fields.Many2many('em.employee', string='Employé(s)', required=True)
    current_department_id = fields.Many2one('em.department', string='Département actuel', readonly=True)
    new_department_id = fields.Many2one('em.department', string='Nouveau département', required=True)
    new_job_position_id = fields.Many2one(
        'em.job.position', string='Nouveau poste',
        domain="[('department_id', 'in', [new_department_id, False])]",
    )
    new_salary = fields.Float(string='Nouveau salaire (Ar)', digits=(16, 0))
    transfer_date = fields.Date(string='Date de mutation', default=fields.Date.today, required=True)
    reason = fields.Text(string='Motif de la mutation')

    @api.onchange('new_department_id')
    def _onchange_new_department_id(self):
        self.new_job_position_id = False

    def action_confirm_transfer(self):
        if not self.employee_ids:
            raise UserError(_('Aucun employé sélectionné.'))

        vals = {'department_id': self.new_department_id.id}
        if self.new_job_position_id:
            vals['job_position_id'] = self.new_job_position_id.id
        if self.new_salary and self.new_salary > 0:
            vals['salary'] = self.new_salary

        for emp in self.employee_ids:
            emp.write(vals)
            msg = _(
                '🔄 <b>Mutation effectuée</b> le %(date)s par %(user)s.<br/>'
                '📁 Nouveau département : <b>%(dept)s</b>'
            ) % {
                'date': self.transfer_date.strftime('%d/%m/%Y'),
                'user': self.env.user.name,
                'dept': self.new_department_id.name,
            }
            if self.new_job_position_id:
                msg += _('<br/>💼 Nouveau poste : <b>%s</b>') % self.new_job_position_id.name
            if self.reason:
                msg += _('<br/>📝 Motif : %s') % self.reason
            emp.message_post(body=msg, message_type='comment', subtype_xmlid='mail.mt_note')

        return {'type': 'ir.actions.act_window_close'}
