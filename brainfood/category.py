"""
This is the categories module and supports all the REST actions for the
categories data
"""

from flask import make_response, abort
from config import db
from models import Category


def get_all():
    """
    This function responds to a request for /api/categories
    with the complete lists of categories

    :return:        json string of list of categories
    """
    # Create the list of categories from our data
    categories = Category.query.order_by(Category.name).all()
    return [category.as_dict() for category in categories]


def read_one(category_id):
    """
    This function responds to a request for /api/categories/{category_id}
    with one matching category from categories

    :param category_id:   Id of category to find
    :return:            category matching id
    """
    # Get the category requested
    category = Category.query.filter(Category.category_id == category_id).one_or_none()

    # Did we find a category?
    if category is not None:
        return category.as_dict()

    # Otherwise, nope, didn't find that category
    else:
        abort(
            404,
            "Category not found for Id: {category_id}".format(category_id=category_id),
        )


def create(category):
    """
    This function creates a new category in the categories structure
    based on the passed in category data

    :param category:  category to create in categories structure
    :return:        201 on success, 406 on category exists
    """
    name = category.get("name")

    existing_category = (
        Category.query.filter(Category.name == name).one_or_none()
    )

    # Can we insert this category?
    if existing_category is None:
        # Add the category to the database
        new_category = Category(name)
        db.add(new_category)
        db.commit()
        return new_category.as_dict(), 201

    # Otherwise, nope, category exists already
    else:
        abort(
            409,
            "Category name exists already".format(
                name=name
            ),
        )


def update(category_id, category):
    """
    This function updates an existing category in the categories structure
    Throws an error if a category with the name we want to update to
    already exists in the database.

    :param category_id:   Id of the category to update in the categories structure
    :param category:      category to update
    :return:            updated category structure
    """
    # Get the category requested from the db into session
    update_category = Category.query.filter(
        Category.category_id == category_id
    ).one_or_none()

    # Try to find an existing category with the same name as the update
    name = category.get("name")

    existing_category = (
        Category.query.filter(Category.name == name)
        .one_or_none()
    )

    # Are we trying to find a category that does not exist?
    if update_category is None:
        abort(
            404,
            "Category not found for Id: {category_id}".format(category_id=category_id),
        )

    # Would our update create a duplicate of another category already existing?
    elif (
        existing_category is not None and existing_category.category_id != category_id
    ):
        abort(
            409,
            "Category {name} exists already".format(
                name=name
            ),
        )

    # Otherwise go ahead and update!
    else:
        update_category.name = name

        # merge the new object into the old and commit it to the db
        db.merge(update_category)
        db.commit()

        return update_category.as_dict(), 200


def delete(category_id):
    """
    This function deletes a category from the categories structure

    :param category_id:   Id of the category to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the category requested
    category = Category.query.filter(Category.category_id == category_id).one_or_none()

    # Did we find a category?
    if category is not None:
        db.delete(category)
        db.commit()
        return make_response(
            "Category {category_id} deleted".format(category_id=category_id), 200
        )

    # Otherwise, nope, didn't find that category
    else:
        abort(
            404,
            "Category not found for Id: {category_id}".format(category_id=category_id),
        )
