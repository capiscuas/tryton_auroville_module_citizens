'''
Created on Oct 4, 2012

@author: nedden
'''
from trytond.model import ModelView, ModelSQL, fields
import ldap
from trytond.pool import Pool
import logging


class Asyncto(ModelSQL, ModelView):
    "Asyncto"
    _name = "auroville.asyncto"
    _description = __doc__

    asynctoid = fields.Char('asynctoId', required=True)
    aurovillename = fields.Char('aurovilleName', required=True)
    name = fields.Char('name')
    surname = fields.Char('surname')
    address = fields.Char('address', required=True)
    telephone = fields.Char('telephone')
    email = fields.Char('email')
    presence = fields.Char('presence')
    status = fields.Char('status')
    contactperson = fields.Char('contactperson')
    deleteflag = fields.Char('deleteFlag')
    ldapid = fields.Char('ldapId')
    masterlistid = fields.Char('masterlistId', required=True)
    fsid = fields.Char('fsId')
    tsid = fields.Char('tsId')

    def __get_ldap_attr(self, entry, name):
        result =''
        try:
            result = entry[name].strip()
        except:
            pass
        return result

    def ldap_sync (self, ldap_server, username, password):
        log = logging.getLogger('logfile')
        try:
            log.warn('LDAP Syncronization')
            l = ldap.initialize(ldap_server);
            l.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
            l.protocol_version = ldap.VERSION3
            l.start_tls_s()
            l.simple_bind_s(username, password)

            baseDN = "ou=people,dc=asyncto,dc=auroville,dc=org,dc=in"

            searchScope = ldap.SCOPE_SUBTREE

            retrieveAttributes = None

            searchFilter = "objectClass=inetOrgPerson"

            ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
            result_set = []
            while 1:
                result_type, result_data = l.result(ldap_result_id, 0)
                if (result_data == []):
                    break
                else:
                    if result_type == ldap.RES_SEARCH_ENTRY:
                        result_set.append(result_data)

            result_parsed = []

            for i in range(len(result_set)):
                for entry in result_set[i]:
                    entry = entry[1]
                    entry = {k.lower():v[0] for k,v in entry.items()}
                    item = {
                            'asynctoid' : self.__get_ldap_attr(entry, 'uid'),
                            'aurovillename' : self.__get_ldap_attr(entry, 'cn'),
                            'name' : self.__get_ldap_attr(entry, 'givenname'),
                            'surname' : self.__get_ldap_attr(entry, 'sn'),
                            'address' : self.__get_ldap_attr(entry, 'street'),
                            'telephone' : self.__get_ldap_attr(entry, 'telephonenumber'),
                            'email' : self.__get_ldap_attr(entry, 'mail'),
                            'presence' : self.__get_ldap_attr(entry, 'departmentnumber'),
                            'status' : self.__get_ldap_attr(entry, 'employeetype'),
                            'contactperson' : self.__get_ldap_attr(entry, 'manager'),
                            'deleteflag' : self.__get_ldap_attr(entry, 'title'),
                            'ldapid' : self.__get_ldap_attr(entry, 'dn'),
                            'masterlistid' : self.__get_ldap_attr(entry, 'postalcode'),
                            'fsid' : self.__get_ldap_attr(entry, 'facsimiletelephonenumber'),
                            'tsid' : self.__get_ldap_attr(entry, 'pager')
                        }

                    result_parsed.append(item)

            asyncto_obj = Pool().get('auroville.asyncto')

            for item in result_parsed:
                asyncto_id = asyncto_obj.search([('asynctoid', '=', item['asynctoid']),])
                if asyncto_id:
                    asyncto_obj.write(asyncto_id, item)
                else:
                    asyncto_obj.create(item)

            log.warn('LDAP %i records' % len(result_parsed))
        except Exception as e:
            log.error(e)

Asyncto()