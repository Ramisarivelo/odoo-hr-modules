# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Department(models.Model):
    _name = 'em.department'
    _description = 'Département'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'
    _parent_name = 'parent_id'
    _parent_store = True

    name = fields.Char(string='Nom du département', required=True, tracking=True)
    code = fields.Char(string='Code', size=10)
    description = fields.Text(string='Description')
    manager_id = fields.Many2one('em.employee', string='Responsable', tracking=True)
    parent_id = fields.Many2one('em.department', string='Département parent', ondelete='restrict')
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many('em.department', 'parent_id', string='Sous-départements')
    employee_ids = fields.One2many('em.employee', 'department_id', string='Employés')

    employee_count = fields.Integer(string='Employés directs', compute='_compute_employee_count', store=True)
    total_employee_count = fields.Integer(string='Total employés', compute='_compute_total_employee_count')
    total_salary = fields.Float(string='Masse salariale (Ar)', compute='_compute_total_salary', digits=(16, 0))
    active = fields.Boolean(string='Actif', default=True)
    color = fields.Integer(string='Couleur', default=0)

    @api.depends('employee_ids')
    def _compute_employee_count(self):
        for dept in self:
            dept.employee_count = len(dept.employee_ids)

    def _compute_total_employee_count(self):
        for dept in self:
            # Inclut les sous-départements
            all_depts = self.search([('id', 'child_of', dept.id)])
            dept.total_employee_count = self.env['em.employee'].search_count(
                [('department_id', 'in', all_depts.ids)]
            )

    def _compute_total_salary(self):
        for dept in self:
            emps = self.env['em.employee'].search([('department_id', '=', dept.id), ('state', '=', 'active')])
            dept.total_salary = sum(emps.mapped('salary'))

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('❌ Hiérarchie circulaire détectée dans les départements !'))

    @api.constrains('name')
    def _check_unique_name(self):
        for rec in self:
            existing = self.search([('name', '=ilike', rec.name), ('id', '!=', rec.id)])
            if existing:
                raise ValidationError(_('❌ Le département "%s" existe déjà !') % rec.name)

    def action_view_employees(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Employés — %s') % self.name,
            'res_model': 'em.employee',
            'view_mode': 'tree,kanban,form',
            'domain': [('department_id', '=', self.id)],
            'context': {'default_department_id': self.id},
        }

    def name_get(self):
        result = []
        for dept in self:
            name = '[%s] %s' % (dept.code, dept.name) if dept.code else dept.name
            result.append((dept.id, name))
        return result
