from blogapi.extensions import db
from sqlalchemy.exc import SQLAlchemyError

def get_all(model):
    data = model.query.all()
    return data


def get_one(model, **kwargs):
    
    try:
        data = model.query.filter_by(**kwargs).first()
        return data
    except SQLAlchemyError:
        db.session.rollback()
        return False


def add_instance(model, **kwargs):
    try:
        instance = model(**kwargs)
        db.session.add(instance)
        commit_changes()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False
    



def delete_instance(model, **kwargs):
    try:
        model.query.filter_by(**kwargs).delete()
        commit_changes()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False



def edit_instance(model, id, **kwargs):
    kwargs_str = ','.join('{}={}'.format(k,v) for k,v in kwargs.items())

    search = search_field(**kwargs)
    instance = model.query.filter_by(**search).first_or_404(description='There is no {} with {}'.format(model, kwargs_str))
    try:
        for attr, new_value in kwargs.items():
            setattr(instance, attr, new_value)
        commit_changes()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False

def update_instance(model, id, **kwargs):
    kwargs_str = ','.join('{}={}'.format(k,v) for k,v in kwargs.items())

    search = search_field(**kwargs)
    
    instance = model.query.filter_by(**search).first_or_404(description='There is no {} with {}'.format(model, kwargs_str))
    try:
        for attr, new_value in kwargs.items():
            setattr(instance, attr, new_value)
        commit_changes()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False

def commit_changes():
    db.session.commit()

def search_field(**kwargs):
    for k,v in kwargs.items():
        if k=='public_id':
            return {'public_id': v }
        elif k=='id':
            return {'id': v}