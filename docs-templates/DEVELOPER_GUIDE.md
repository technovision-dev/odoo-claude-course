# Developer guide

## Models

### `{model.name}` ({Description})

| Field | Type | Notes |
|---|---|---|
| `{field}` | {Char} | {required, default, constraint} |

Constraints: {list}.

## Extending

| Method | Purpose | Safe to override? |
|---|---|---|
| `{_method}` | {what it does} | {Yes: call super() and ...} |

## Tests

    ./odoo/odoo-bin -c odoo.conf -d test_db -i {module} --test-enable --test-tags /{module} --stop-after-init

{N} tests: {what they cover}.
