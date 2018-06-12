from functools import wraps

from flask import g

from dataactcore.interfaces.db import GlobalDB
from dataactcore.models.jobModels import Submission
from dataactcore.models.lookups import PERMISSION_TYPE_DICT, PERMISSION_SHORT_DICT, FABS_PERMISSION_ID_LIST
from dataactcore.utils.jsonResponse import JsonResponse
from dataactcore.utils.responseException import ResponseException
from dataactcore.utils.statusCode import StatusCode

NOT_AUTHORIZED_MSG = "You are not authorized to perform the requested task. Please contact your administrator."

DABS_PERMS = [PERMISSION_SHORT_DICT['w'], PERMISSION_SHORT_DICT['s']]
FABS_PERM = PERMISSION_SHORT_DICT['f']


def requires_login(func):
    """ Decorator requiring that _a_ user be logged in (i.e. that we're not using an anonymous session)

        Args:
            permission: single-letter string representing an application permission
            cgac_code: 3-digit numerical string identifying a CGAC agency
            frec_code: 4-digit numerical string identifying a FREC agency

        Returns:
            Boolean result on whether the user has permissions greater than or equal to permission
    """
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user is None:
            return JsonResponse.create(StatusCode.LOGIN_REQUIRED, {'message': "Login Required"})
        return func(*args, **kwargs)
    return inner


def requires_admin(func):
    """Decorator requiring the requesting user be a website admin"""
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user is None:
            return JsonResponse.create(StatusCode.LOGIN_REQUIRED, {'message': "Login Required"})

        if not g.user.website_admin:
            return JsonResponse.create(StatusCode.LOGIN_REQUIRED, {'message': NOT_AUTHORIZED_MSG})

        return func(*args, **kwargs)
    return inner


def current_user_can(permission, cgac_code, frec_code):
    """ Validate whether the current user can perform the act (described by the permission level) for the given
        cgac_code or frec_code

        Args:
            permission: single-letter string representing an application permission
            cgac_code: 3-digit numerical string identifying a CGAC agency
            frec_code: 4-digit numerical string identifying a FREC agency

        Returns:
            Boolean result on whether the user has permissions greater than or equal to permission
    """
    # If the user is not logged in, or the user is a website admin, there is no reason to check their permissions
    if not hasattr(g, 'user'):
        return False
    elif g.user.website_admin:
        return True

    # Ensure the permission exists and retrieve its ID
    try:
        permission_id = PERMISSION_TYPE_DICT[permission]
    except KeyError:
        return False

    # Loop through user's affiliations and return True if any match the permission
    for aff in g.user.affiliations:
        # Check if affiliation agency matches agency args
        if (aff.cgac and aff.cgac.cgac_code == cgac_code) or (aff.frec and aff.frec.frec_code == frec_code):
            # Check if affiliation has higher permissions than permission args
            is_fabs = aff.permission_type_id in FABS_PERMISSION_ID_LIST
            fabs_perms = aff.permission_type_id <= permission_id and is_fabs
            dabs_perms = aff.permission_type_id >= permission_id and not is_fabs

            if (permission == 'reader') or dabs_perms or fabs_perms:
                return True

    return False


def current_user_can_on_submission(perm, submission, check_owner=True):
    """Submissions add another permission possibility: if a user created a submission, they can do anything to it,
    regardless of submission agency"""
    is_owner = hasattr(g, 'user') and submission.user_id == g.user.user_id
    return (is_owner and check_owner) or current_user_can(perm, submission.cgac_code, submission.frec_code)


def requires_submission_perms(perm, check_owner=True):
    """Decorator that checks the current user's permissions and validates that the submission exists. It expects a
    submission_id parameter and will return a submission object"""
    def inner(fn):
        @requires_login
        @wraps(fn)
        def wrapped(submission_id, *args, **kwargs):
            sess = GlobalDB.db().session
            submission = sess.query(Submission).\
                filter_by(submission_id=submission_id).one_or_none()

            if submission is None:
                # @todo - why don't we use 404s?
                raise ResponseException('No such submission',
                                        StatusCode.CLIENT_ERROR)

            if not current_user_can_on_submission(perm, submission, check_owner):
                raise ResponseException(
                    "User does not have permission to access that submission",
                    StatusCode.PERMISSION_DENIED)
            return fn(submission, *args, **kwargs)
        return wrapped
    return inner


def separate_affiliations(affiliations, app_type):
    cgac_ids, frec_ids = [], []

    for affil in g.user.affiliations:
        perm_type = affil.permission_type_id
        if (app_type == 'fabs' and perm_type == FABS_PERM) or (app_type == 'dabs' and perm_type in DABS_PERMS):
            if affil.frec:
                frec_ids.append(affil.frec.frec_id)
            else:
                cgac_ids.append(affil.cgac.cgac_id)

    return cgac_ids, frec_ids
