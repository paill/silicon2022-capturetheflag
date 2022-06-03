import sys
import io

from twisted.application import service
from twisted.internet.endpoints import serverFromString
from twisted.internet.protocol import ServerFactory
from twisted.python.components import registerAdapter
from twisted.python import log
from ldaptor.inmemory import fromLDIFFile
from ldaptor.interfaces import IConnectedLDAPEntry
from ldaptor.protocols.ldap.ldapserver import LDAPServer

LDIF = b"""\
dn: dc=party
dc: party
objectClass: dcObject

dn: dc=bowsercorp,dc=party
dc: bowsercorp
objectClass: dcObject
objectClass: organization

dn: ou=people,dc=bowsercorp,dc=party
objectClass: organizationalUnit
ou: people

dn: cn=larry,ou=people,dc=bowsercorp,dc=party
cn: larry
mail: larry@bowsercorp.party
objectClass: top
objectClass: person
objectClass: inetOrgPerson

dn: cn=morton,ou=people,dc=bowsercorp,dc=party
cn: morton
mail: morton@bowsercorp.party
objectClass: top
objectClass: person
objectClass: inetOrgPerson

dn: cn=wendy,ou=people,dc=bowsercorp,dc=party
cn: wendy
mail: wendy@bowsercorp.party
objectClass: top
objectClass: person
objectClass: inetOrgPerson

dn: cn=iggy,ou=people,dc=bowsercorp,dc=party
cn: iggy
mail: iggy@bowsercorp.party
objectClass: top
objectClass: person
objectClass: inetOrgPerson

dn: cn=roy,ou=people,dc=bowsercorp,dc=party
cn: roy
mail: roy@bowsercorp.party
objectClass: top
objectClass: person
objectClass: inetOrgPerson

dn: cn=lemmy,ou=people,dc=bowsercorp,dc=party
cn: lemmy
mail: lemmy@bowsercorp.party
address: SILICON{lDap_k0opa_b0S$35}
objectClass: top
objectClass: person
objectClass: inetOrgPerson

dn: cn=ludwig,ou=people,dc=bowsercorp,dc=party
cn: ludwig
mail: ludwig@bowsercorp.party
objectClass: top
objectClass: person
objectClass: inetOrgPerson

dn: cn=wario,ou=people,dc=bowsercorp,dc=party
cn: wario
mail: wario@bowsercorp.party
objectClass: top
objectClass: javaNamingReference
objectClass: inetOrgPerson
javaClassName: mario
javaFactory: Main
javaCodebase: http://localhost:3002/

"""


class Tree:
    def __init__(self):
        global LDIF
        self.f = io.BytesIO(LDIF)
        d = fromLDIFFile(self.f)
        d.addCallback(self.ldifRead)

    def ldifRead(self, result):
        self.f.close()
        self.db = result


class LDAPServerFactory(ServerFactory):
    protocol = LDAPServer

    def __init__(self, root):
        self.root = root

    def buildProtocol(self, addr):
        proto = self.protocol()
        proto.debug = self.debug
        proto.factory = self
        return proto


if __name__ == "__main__":
    from twisted.internet import reactor

    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = 8080
    # First of all, to show logging info in stdout :
    log.startLogging(sys.stderr)
    # We initialize our tree
    tree = Tree()
    # When the LDAP Server protocol wants to manipulate the DIT, it invokes
    # `root = interfaces.IConnectedLDAPEntry(self.factory)` to get the root
    # of the DIT.  The factory that creates the protocol must therefore
    # be adapted to the IConnectedLDAPEntry interface.
    registerAdapter(lambda x: x.root, LDAPServerFactory, IConnectedLDAPEntry)
    factory = LDAPServerFactory(tree.db)
    factory.debug = True
    application = service.Application("ldaptor-server")
    myService = service.IServiceCollection(application)
    serverEndpointStr = f"tcp:{port}"
    e = serverFromString(reactor, serverEndpointStr)
    d = e.listen(factory)
    reactor.run()

