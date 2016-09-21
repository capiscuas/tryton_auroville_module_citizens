'''
Created on Oct 9, 2012

@author: nedden
'''
from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateView, Button, StateTransition
from trytond.pool import Pool
from trytond.transaction import Transaction


class AgreementWizardStep1(ModelView):
    'Agreement Wizard 1'
    _name = 'auroville_assets.wizard1'
    _description = __doc__

    resident = fields.Many2One('auroville.people', 'Resident', required=True, select=True)

AgreementWizardStep1()

class AgreementWizardStep2(ModelView):
    'Agreement Wizard 2'
    _name = 'auroville_assets.wizard2'
    _description = __doc__

    assets = fields.Many2One('auroville.assets', 'Assets', required=True, select=True)


AgreementWizardStep2()


class AgreementWizard(Wizard):
    'Agreement Wizard'
    _name = 'auroville_assets.agreement_wizard'

    start = StateView('auroville_assets.wizard1',
        'auroville_assets.assets_wizard_form1', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Next', 'assets', 'tryton-go-next', True),
            ])
    assets = StateView('auroville_assets.wizard2',
        'auroville_assets.assets_wizard_form2', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('New agreement', 'add', 'tryton-ok', True),
            ])

    add = StateTransition()

    def transition_add(self, session):
        people_obj = Pool().get('auroville.people')
        assets_obj = Pool().get('auroville.assets')
        user_obj = Pool().get('res.user')

        values = session.data['start'].copy()
        print values

        values = session.data['assets'].copy()
        print values
        #people_id = people_obj.create(values)

        user = user_obj.browse(Transaction().user)
        return 'end'

AgreementWizard()
