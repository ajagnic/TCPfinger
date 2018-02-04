from twisted.application import service, strports
from twisted.internet import reactor, protocol, endpoints, defer, utils
from twisted.protocols import basic
from twisted.web import client

class FingerProtocol(basic.LineReceiver):
    def dataReceived(self, data):
        print(data)

    def lineReceived(self, user):
        d = self.factory.getUser(user)

        def onError(err):
            return "internal error"
        d.addErrback(onError)

        def writeResponse(message):
            self.transport.write(message + b"\r\n")
            self.transport.loseConnection()
        d.addCallback(writeResponse)

class FingerFactory(protocol.ServerFactory):
    protocol = FingerProtocol
    def __init__(self, users):
        self.users = users

    def getUser(self, user):
        return defer.succeed(self.users.get(user,b"none"))

application = service.Application('finger')
factory = FingerFactory({b"ajagnic":b"here"})
strports.service("tcp:1079", factory, reactor=reactor).setServiceParent(service.IServiceCollection(application))
