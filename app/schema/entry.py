from marshmallow import Schema, fields

class EntrySchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    user = fields.Nested('UserSchema')
    start_time = fields.DateTime()
    end_time = fields.DateTime()

