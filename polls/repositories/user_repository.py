from django.contrib.auth.models import User

class UserRepository:

    @staticmethod
    def get_user_by_id(user_id):
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def list_users():
        return User.objects.all()

    @staticmethod
    def create_user(username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        return user

    @staticmethod
    def update_user(user_id, **kwargs):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return None
        for attr, value in kwargs.items():
            setattr(user, attr, value)
        user.save()
        return user

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if user:
            user.delete()
