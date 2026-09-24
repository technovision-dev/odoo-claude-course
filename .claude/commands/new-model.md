---
description: Add a new model to a module with its security, views, menu and a first test
argument-hint: <module> <model.name> <one-line purpose>
---

Add a new model to a module in addons-custom. Arguments: $ARGUMENTS
(the module, the model's technical name, then what it is for).

1. Read the module's `__manifest__.py`, `models/__init__.py`, `security/ir.model.access.csv`
   and `views/menus.xml` first. Follow CLAUDE.md and the rules for the module's series.
2. Plan before writing: list the fields you propose (type, required, default, help), the
   `_order`, any constraint, which groups get which access, and where the menu goes. If a field
   refers to a core model, grep `./odoo` for it and name the file you checked. Wait for my
   approval.
3. Then write: `models/<model_underscored>.py` (with `_name`, `_description`, `_order`),
   the import, access lines for every group in the plan, list/form/search views and the action
   in `views/<model_underscored>_views.xml`, the menu, and the manifest `data` entries in the
   right order.
4. Add `tests/test_<model_underscored>.py` with at least: creating a record works, and each
   constraint refuses bad data. Import it in `tests/__init__.py`.
5. Run the install + test command from CLAUDE.md on a fresh test database and quote the
   summary line.
