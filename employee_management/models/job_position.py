# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class JobPosition(models.Model):
    _name = 'em.job.position'
    _description = 'Poste / Fonction'
    _order = 'name asc'

    name = fields.Char(string='Intitulé du poste', required=True)
    department_id = fields.Many2one('em.department', string='Département')
    description = fields.Html(string='Description du poste')
    requirements = fields.Text(string='Compétences requises')
    salary_min = fields.Float(string='Salaire minimum (Ar)', digits=(16, 0))
    salary_max = fields.Float(string='Salaire maximum (Ar)', digits=(16, 0))
    level = fields.Selection([
        ('junior', 'Junior'),
        ('intermediate', 'Intermédiaire'),
        ('senior', 'Senior'),
        ('lead', 'Lead / Expert'),
        ('manager', 'Manager'),
        ('director', 'Directeur'),
    ], string='Niveau', default='intermediate')
    employee_ids = fields.One2many('em.employee', 'job_position_id', string='Employés')
    employee_count = fields.Integer(string='Effectif', compute='_compute_employee_count', store=True)
    active = fields.Boolean(string='Actif', default=True)

    @api.depends('employee_ids')
    def _compute_employee_count(self):
        for job in self:
            job.employee_count = len(job.employee_ids)

    @api.constrains('salary_min', 'salary_max')
    def _check_salary_range(self):
        for rec in self:
            if rec.salary_min and rec.salary_max and rec.salary_min > rec.salary_max:
                raise ValidationError(_('❌ Le salaire minimum ne peut pas dépasser le salaire maximum !'))

    _sql_constraints = [
        ('unique_name_dept', 'UNIQUE(name, department_id)',
         'Un poste avec ce nom existe déjà dans ce département !'),
    ]
