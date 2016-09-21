from trytond.model import ModelView, ModelSQL, fields
from trytond.pyson import Eval
from datetime import datetime
from trytond.pool import Pool
from trytond.transaction import Transaction
import logging
from trytond.wizard import Wizard, StateView, Button, StateTransition

STATES = {
    'readonly': ~Eval('active', True),
    }

DEPENDS = ['active']


class Community(ModelSQL, ModelView):
    "Community"
    _name = "auroville.community"
    _description = __doc__

    name = fields.Char('Community', required=True, select=True)
    asynctoname = fields.Char('Asyncto Name', required=True, select=True)

    def __init__(self):
        super(Community, self).__init__()
        self._order.insert(0, ('name', 'ASC'))


    def asyncto_sync(self):
        log = logging.getLogger('logfile')
        log.warn('Asyncto Community sync')
        try:
            asyncto_obj = Pool().get('auroville.asyncto')
            community_obj = Pool().get('auroville.community')
            asyncto_ids = asyncto_obj.search([])
            for item in asyncto_obj.browse(asyncto_ids):
                if item.address.strip():
                    community_ids = community_obj.search([('asynctoname', '=', item.address),])
                    data = {'name' : item.address, 'asynctoname' : item.address}
                    if community_ids:
                        community_obj.write(community_ids, data)
                    else:
                        community_obj.create(data)

        except Exception as e:
            log.error(e)

Community()

class ResidenceType(ModelSQL, ModelView):
    "Residence status"
    _name = "auroville.residence_type"
    _description = __doc__
    name = fields.Char('Name', required=True, select=True)

ResidenceType()

class ResidencePresenceStatus(ModelSQL, ModelView):
    "Residence presence status"
    _name = "auroville.residence_presence_status"
    _description = __doc__
    name = fields.Char('Name', required=True, select=True)

ResidencePresenceStatus()

class LocationArea(ModelSQL, ModelView):
    "Location area"
    _name = "auroville.location_area"
    _description = __doc__
    name = fields.Char('Name', required=True, select=True)

LocationArea()

class Assets(ModelSQL, ModelView):
    "Assets"
    _name = "auroville.assets"
    _description = __doc__

    community = fields.Many2One('auroville.community', 'Community', required=True, select=True)

    location = fields.Many2One('auroville.location_area', 'Location', required=True, select=True)

    type = fields.Many2One('auroville.residence_type', 'Residence type', required=True, select=True)

    status = fields.Many2One('auroville.residence_presence_status', 'Status of residence', required=True, select=True)

    occupation = fields.Selection([
        ('empty', 'Empty'),
        ('occupied', 'Occupied'),
        ('open', 'Open for transfer'),
        ], 'Occupation', required=True, sort=False)

    carpet_area = fields.Integer('Carpet Area')
    bedroom = fields.Integer('Number of bedrooms')
    level = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ], 'Levels', required=True, sort=False)


    floor_location = fields.Selection([
        ('0', 'Ground'),
        ('1', 'First'),
        ('2', 'Second'),
        ('3', 'Third'),
        ('4', 'Fourth'),
        ('5', 'Fifth'),
        ('6', 'Sixth'),
        ], 'Floor location', required=True, sort=False)

    def default_status(self):
        status_obj = Pool().get('auroville.residence_presence_status')
        status_id = status_obj.browse(1)
        return status_id.id

    def default_bedroom(self):
        return 1

    def default_type(self):
        type_obj = Pool().get('auroville.residence_type')
        type_id = type_obj.browse(1)
        return type_id.id

    def default_location(self):
        location_obj = Pool().get('auroville.location_area')
        location_id = location_obj.browse(1)
        return location_id.id


    def default_occupation(self):
        return 'empty'

    def default_floor_location(self):
        return '0'

    def default_level(self):
        return '1'
Assets()

class Agreement(ModelSQL, ModelView):
    "Agreement"
    _name = "auroville.agreement"
    _description = __doc__

    resident = fields.Many2One('auroville.people', 'Resident', required=True, select=True)
    assets = fields.Many2One('auroville.assets', 'Assets', required=True, select=True)
    date = fields.Date('Date of agreement', required=True)
    user_id = fields.Many2One('res.user', 'Author', required=True, readonly=True)

    community = fields.Function(fields.Char('Community'),'get_community')
    type = fields.Function(fields.Char('Type'),'get_type')

    carpet_area = fields.Function(fields.Char('Carpet Area'),'get_carpet_area')
    floor_location = fields.Function(fields.Char('Floor Location'),'get_floor_location')

    def get_community(self, ids, name):
        res = {}
        for item in self.browse(ids):
            res[item.id] = item.assets.community.name
        return res

    def get_type(self, ids, name):
        res = {}
        for item in self.browse(ids):
            res[item.id] = item.assets.type.name
        return res

    def get_carpet_area(self, ids, name):
        res = {}
        for item in self.browse(ids):
            res[item.id] = item.assets.carpet_area
        return res

    def get_floor_location(self, ids, name):
        res = {}
        for item in self.browse(ids):
            res[item.id] = item.assets.floor_location
        return res

    def default_user_id(self):
        user_obj = Pool().get('res.user')
        user = user_obj.browse(Transaction().user)
        return int(user.id)

    def default_date(self):
        return datetime.now()


Agreement()

class PeopleAssets(ModelSQL, ModelView):
    "People"
    _name = "auroville.people"
    _description = __doc__

    agreement = fields.One2Many('auroville.agreement', 'resident', 'Agreements')

PeopleAssets()

class Request(ModelSQL, ModelView):
    "Request"
    _name = "auroville.request"
    _description = __doc__

    resident = fields.Many2One('auroville.people', 'Resident', required=True, select=True)

    residence_type = fields.Many2One('auroville.residence_type', 'Type of residence', required=True, select=True)

    residence_status = fields.Many2One('auroville.residence_type', 'Type of residence', required=True, select=True)

    residents_number = bedroom = fields.Integer('Number of residents')

    bedroom = fields.Integer('Number of bedrooms')

    level = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ], 'Levels', required=True, sort=False)


    floor_location = fields.Selection([
        ('0', 'Ground'),
        ('1', 'First'),
        ('2', 'Second'),
        ('3', 'Third'),
        ('4', 'Fourth'),
        ('5', 'Fifth'),
        ('6', 'Sixth'),
        ], 'Floor location', required=True, sort=False)

    location = fields.Many2One('auroville.location_area', 'Location', required=True, select=True)

    community = fields.Many2One('auroville.community', 'Community', required=True, select=True)

    special_needs = fields.Text('Special needs', required=True, select=True)

    occupation_date1 = fields.Date('Temporary occupation from', required=True)

    occupation_date2 = fields.Date('to', required=True)

    transfer_date = fields.Date('Transfer date', required=True)

    available_funds1 = fields.Integer('Available Funds from')

    available_funds2 = fields.Integer('to')

    grant = fields.Boolean('Grant to be requested')

    loan = fields.Boolean('Loan to be requested')

    contribution1 = fields.Integer('Possible monthly contribution from')

    contribution2 = fields.Integer('to')


Request()
