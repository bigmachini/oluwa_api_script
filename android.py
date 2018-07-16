# API Commander
import os
import sys
import csv
import logging
# from lib.api import API
from lib.api import API as L_API


# Legacy API
def android_api():
    """
    Imports Copia Loyalty Lines from a CSV via XMLRPC with the
    following format (partner_id,name,credit,comment)

    return: int id of the created loyalty line
    """

    api = L_API()

    def get_customer_commission():
        res = api.do_wierd("res.partner",
                     "signin_hpa",
                     "hpa_five",
                     "565569")


        return res

    get_customer_commission()

android_api()