from app.extensions import ma

from app.models.user import User


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        fields = ('id', 'date_created', 'date_modified', 'first_name',
                  'last_name', 'email')
