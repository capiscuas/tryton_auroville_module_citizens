from trytond.model import ModelView, ModelSQL, fields
from datetime import date, datetime
from trytond.pool import Pool
from trytond.transaction import Transaction
import logging

class Nationality(ModelSQL, ModelView):
    "Nationality"
    _name = "auroville.nationality"
    _description = __doc__

    name = fields.Char('Nationality', required=True)


Nationality()

class People(ModelSQL, ModelView):
    "People"
    _name = "auroville.people"
    _description = __doc__

#TODO uniq id
    asynctoid = fields.Char('Asyncto Id', required=False, select=False, readonly=True)
    aurovillename = fields.Char('Auroville name', required=True, translate=False, select=True)
    name = fields.Char('Given name', translate=False, select=True)
    surname = fields.Char('Surname',  translate=False, select=True)
    telephone = fields.Char('Phone number',  translate=False)
    email = fields.Char('Email',  translate=False, select=True)
    contactperson = fields.Char('Contact person', translate=False, select=True)
    masterlistid = fields.Integer('Masterlist ID', readonly=True, select=True)

    date_birth = fields.Date('Date of birth')

    sex = fields.Selection([
        ('Male', 'Male'),
        ('Female', 'Female'),
        ], 'Sex', required=True)

    photo = fields.Binary('Picture')

    nationality = fields.Many2One('auroville.nationality', 'Nationality', select=True)
    age = fields.Function(fields.Integer('Age'),'get_people_age')


    status = fields.Selection([
        ('Aurovilian', 'Aurovilian'),
        ('Newcomer', 'Newcomer'),
        ('Pre-Newcomer', 'Pre-Newcomer'),
        ('Volunteer', 'Volunteer'),
        ('Youth', 'Youth'),
        ('Child', 'Child'),
        ('Friend of Auroville', 'Friend of Auroville'),
        ('Guest', 'Guest'),
        ], 'Status', required=True)

    user_id = fields.Many2One('res.user', 'User', required=True, readonly=True)


    def __init__(self):
        super(People, self).__init__()
        self._order.insert(0, ('masterlistid', 'ASC'))

    def get_people_age(self, ids, name):

        today = date.today()
        res = {}
        for human in self.browse(ids):
            born = human.date_birth
            if born:
                res[human.id] = today.year - born.year - int((today.month, today.day) < (born.month, born.day))
            else:
                res[human.id] = 0
        return res


    def default_user_id(self):
        user_obj = Pool().get('res.user')
        user = user_obj.browse(Transaction().user)
        return int(user.id)

    def default_sex(self):
        return 'Male'

    def default_status(self):
        return 'Aurovilian'

    def asyncto_sync(self):
        log = logging.getLogger('logfile')
        log.warn('Asyncto People sync')
        try:
            asyncto_obj = Pool().get('auroville.asyncto')
            people_obj = Pool().get('auroville.people')
            asyncto_ids = asyncto_obj.search([])
            for item in asyncto_obj.browse(asyncto_ids):
                people_ids = people_obj.search([('asynctoid', '=', item.asynctoid),])
                data = {'asynctoid' : item.asynctoid, 'aurovillename' : item.aurovillename, 'name' : item.name, 'surname' : item.surname,
                        'telephone' : item.telephone, 'email' : item.email, 'contactperson' : item.contactperson,
                        'masterlistid' : int(item.masterlistid)}
                if people_ids:
                    people_obj.write(people_ids, data)
                else:
                    people_obj.create(data)

                # Community


        except Exception as e:
            log.error(e)
People()


