# -*- coding: utf-8 -*-
from odoo import api, models, fields


class EquipmentCategory(models.Model):
    _name = "chc_radio_listing.category"
    _description = "Catégorie / Listing d'équipements"
    _order = "sequence, name"

    name = fields.Char(string="Nom", required=True)
    sequence = fields.Integer(string="Ordre", default=10)
    code = fields.Char(string="Code", size=10)
    description = fields.Text(string="Description")
    color = fields.Integer(string="Couleur", default=0)
    active = fields.Boolean(default=True)
    equipment_ids = fields.One2many(
        "chc_radio_listing.equipment",
        "category_id",
        string="Équipements",
    )
    equipment_count = fields.Integer(
        string="Nb équipements",
        compute="_compute_equipment_count",
        store=True,
    )

    @api.depends("equipment_ids")
    def _compute_equipment_count(self):
        data = self.env["chc_radio_listing.equipment"].read_group(
            [("category_id", "in", self.ids)],
            ["category_id"],
            ["category_id"],
        )
        count_map = {d["category_id"][0]: d["category_id_count"] for d in data}
        for rec in self:
            rec.equipment_count = count_map.get(rec.id, 0)

    def action_view_equipments(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Équipements",
            "res_model": "chc_radio_listing.equipment",
            "view_mode": "list,kanban,form",
            "domain": [("category_id", "=", self.id)],
            "context": {"default_category_id": self.id},
        }
