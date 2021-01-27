"""
This is the groceries module and supports all the REST actions for the
groceries data
"""

from flask import make_response, abort
from database import db_session as db
from models import Grocery


def get_all():
    """
    This function responds to a request for /api/groceries
    with the complete lists of groceries

    :return:        json string of list of groceries
    """
    # Create the list of groceries from our data
    groceries = Grocery.query.order_by(Grocery.name).all()
    return [grocery.as_dict() for grocery in groceries]


def read_one(grocery_id):
    """
    This function responds to a request for /api/groceries/{grocery_id}
    with one matching grocery from groceries

    :param grocery_id:   Id of grocery to find
    :return:            grocery matching id
    """
    # Get the grocery requested
    grocery = Grocery.query.filter(Grocery.grocery_id == grocery_id).one_or_none()

    # Did we find a grocery?
    if grocery is not None:
        return grocery.as_dict()

    # Otherwise, nope, didn't find that grocery
    else:
        abort(
            404,
            "Grocery not found for Id: {grocery_id}".format(grocery_id=grocery_id),
        )


def create(grocery):
    """
    This function creates a new grocery in the groceries structure
    based on the passed in grocery data

    :param grocery:  grocery to create in groceries structure
    :return:        201 on success, 406 on grocery exists
    """
    # Add the grocery to the database
    new_grocery = Grocery(**grocery)
    db.add(new_grocery)
    db.commit()
    return new_grocery.as_dict(), 201


def update(grocery_id, grocery):
    """
    This function updates an existing grocery in the groceries structure
    Throws an error if a grocery with the name we want to update to
    already exists in the database.

    :param grocery_id:   Id of the grocery to update in the groceries structure
    :param grocery:      grocery to update
    :return:            updated grocery structure
    """
    # Get the grocery requested from the db into session
    update_grocery = Grocery.query.filter(
        Grocery.grocery_id == grocery_id
    ).one_or_none()

    # Are we trying to find a grocery that does not exist?
    if update_grocery is None:
        abort(
            404,
            "Grocery not found for Id: {grocery_id}".format(grocery_id=grocery_id),
        )

    # Otherwise go ahead and update!
    else:
        for update_key, update_value in grocery.items():
            print(update_key, update_value)
            update_grocery.update_key = update_value
        print(update_grocery.as_dict())
        # merge the new object into the old and commit it to the db
        db.merge(update_grocery)
        db.commit()

        return update_grocery.as_dict(), 200


def delete(grocery_id):
    """
    This function deletes a grocery from the groceries structure

    :param grocery_id:   Id of the grocery to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the grocery requested
    grocery = Grocery.query.filter(Grocery.grocery_id == grocery_id).one_or_none()

    # Did we find a grocery?
    if grocery is not None:
        db.delete(grocery)
        db.commit()
        return make_response(
            "Grocery {grocery_id} deleted".format(grocery_id=grocery_id), 200
        )

    # Otherwise, nope, didn't find that grocery
    else:
        abort(
            404,
            "Grocery not found for Id: {grocery_id}".format(grocery_id=grocery_id),
        )
