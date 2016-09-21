# -*- coding: utf-8 -*-

{
    'name': 'Auroville Assets',
    'version': '0.0.1',
    'author': 'BlueLight',
    'email': 'bluelight@bluelightav.org',
    'website': 'http://bluelightav.org',
    'description': '''

Auroville Assets
----------------------

Description: ******

''',
    'depends': [
        'ir',
        'res',
        'auroville_asyncto',
        'auroville_people'

    ],
    'xml': [
        'assets.xml',
        'data/residence_presence_status.xml',
        'data/residence_type.xml',
        'data/location_area.xml',
        'security/access_rights.xml',
    ],
    'translation': [],
}
