# -*- coding: utf-8 -*-
{
    'name': 'Auroville Housing',
    'version': '0.0.1',
    'author': 'BlueLight',
    'email': 'bluelight@bluelightav.org',
    'website': 'http://bluelightav.org',
    'description': '''

Auroville Residents
----------------------

Description: ******

''',
    'depends': [
        'ir',
        'res',
        'auroville_asyncto',
        'auroville_people',
        'auroville_assets',
    ],
    'xml': [
        'housing.xml',
        'security/access_rights.xml',
    ],
    'translation': [],
}