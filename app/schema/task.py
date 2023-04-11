from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    entry_id = fields.Int()
    entry = fields.Nested('EntrySchema')
