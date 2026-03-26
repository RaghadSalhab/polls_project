# polls/repositories/base_repository.py
from polls.models.database import Session

class BaseRepository:
    model = None 

    @classmethod
    def get(cls, id_):
        """Get object by ID"""
        return Session.query(cls.model).filter(cls.model.id == id_).first()

    @classmethod
    def list_all(cls):
        """Get all objects of this model"""
        return Session.query(cls.model).all()

    @classmethod
    def add(cls, obj, commit=False):
        """Add object to session, refresh it, optionally commit"""
        Session.add(obj)
        Session.flush()
        Session.refresh(obj)
        if commit:
            Session.commit()
        return obj

    @classmethod
    def delete(cls, obj, commit=False):
        """Delete object from session, optionally commit"""
        Session.delete(obj)
        Session.flush()
        if commit:
            Session.commit()

    @classmethod
    def delete_by_id(cls, id_, commit=False):
        """Delete object by ID, optionally commit"""
        obj = cls.get(id_)
        if obj:
            cls.delete(obj, commit=commit)
            return True
        return False

    @classmethod
    def commit(cls):
        """Explicit commit if needed"""
        Session.commit()

    @classmethod
    def flush(cls):
        """Explicit flush if needed"""
        Session.flush()
