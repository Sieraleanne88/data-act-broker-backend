from functools import wraps
from flask import g

from dataactcore.interfaces.db import GlobalDB
from dataactcore.models.domainModels import CGAC, SubTierAgency, FREC
from dataactcore.utils.jsonResponse import JsonResponse
from dataactcore.utils.statusCode import StatusCode


# Add the file submission route
def add_domain_routes(app):
    """ Create routes related to domain values for flask app """

    @app.route("/v1/list_agencies/", methods=["GET"])
    @get_frecs
    @get_cgacs
    def list_agencies(cgacs, frecs):
        """ List all CGAC Agencies
            Args:
            cgacs - List of all cgac codes that are valid for the user, generated by get_cgacs decorator,
                required to list only agencies that user can access
        """
        agency_list = [
            {'agency_name': cgac.agency_name, 'cgac_code': cgac.cgac_code}
            for cgac in cgacs
        ]
        shared_agency_list = [
            {'agency_name': frec.agency_name, 'frec_code': frec.frec_code}
            for frec in frecs
        ]
        return JsonResponse.create(StatusCode.OK, {
            'cgac_agency_list': agency_list,
            'frec_agency_list': shared_agency_list
        })

    @app.route("/v1/list_all_agencies/", methods=["GET"])
    def list_all_agencies():
        sess = GlobalDB.db().session
        cgacs = sess.query(CGAC).all()
        agency_list = [
            {'agency_name': cgac.agency_name, 'cgac_code': cgac.cgac_code}
            for cgac in cgacs
        ]
        frecs = sess.query(FREC).all()
        shared_list = [
            {'agency_name': frec.agency_name, 'frec_code': frec.frec_code}
            for frec in frecs
            ]
        return JsonResponse.create(StatusCode.OK, {'agency_list': agency_list, 'shared_agency_list': shared_list})

    @app.route("/v1/list_sub_tier_agencies/", methods=["GET"])
    @get_cgacs
    def list_sub_tier_agencies(cgacs):
        """ List all Sub-Tier Agencies
            Args:
            cgacs - List of all cgac codes that are valid for the user, generated by get_cgacs decorator,
                required to list only agencies that user can access
        """
        sess = GlobalDB.db().session

        cgac_ids = [cgac.cgac_id for cgac in cgacs]
        sub_tier_agencies = []
        for cgac_id in cgac_ids:
            sub_tier_agencies.extend(sess.query(SubTierAgency).filter_by(cgac_id=cgac_id))

        sub_tier_agency_list = [
            {'agency_name': '{}: {}'.format(sub_tier_agency.cgac.agency_name, sub_tier_agency.sub_tier_agency_name),
             'agency_code': sub_tier_agency.sub_tier_agency_code,
             'priority': sub_tier_agency.priority} for sub_tier_agency in sub_tier_agencies
        ]
        return JsonResponse.create(StatusCode.OK, {'sub_tier_agency_list': sub_tier_agency_list})


def get_cgacs(fn):
    """ Decorator which provides a list of all CGAC Agencies. The function
    should have a cgacs parameter as its first argument. """
    @wraps(fn)
    def wrapped(*args, **kwargs):
        sess = GlobalDB.db().session
        if g.user is None:
            cgacs = []
        elif g.user.website_admin:
            cgacs = sess.query(CGAC).all()
        else:
            cgacs = []
            for affil in g.user.affiliations:
                if affil.permission_type_id >= 2:
                    cgacs.append(affil.cgac)
        return fn(cgacs, *args, **kwargs)
    return wrapped


def get_frecs(fn):
    """ Decorator which provides a list of all FREC Agencies. The function
    should have a frecs parameter as its first argument. """
    @wraps(fn)
    def wrapped(*args, **kwargs):
        sess = GlobalDB.db().session
        if g.user is None:
            frecs = sess.query(FREC).all()
        else:
            frecs = []
            for affil in g.user.affiliations:
                if affil.permission_type_id >= 2:
                    frecs.append(affil.frec)
        return fn(frecs, *args, **kwargs)
    return wrapped
