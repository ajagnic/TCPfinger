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

class FingerSetterProtocol(basic.LineReceiver):
    def connectionMade(self):
        self.lines = []

    def lineReceived(self, line):
        self.lines.append(line)

    def connectionLost(self, reason):
        user = self.lines[0]
        status = self.lines[1]
        self.factory.setUser(user, status)

class FingerSetterFactory(protocol.ServerFactory):
    protocol = FingerSetterProtocol
    def __init__(self, fingerFactory):
        self.fingerFactory = fingerFactory

    def setUser(self, user, status):
        self.fingerFactory.users[user] = status

ff = FingerFactory({b"ajagnic":b"here"})
fsf = FingerSetterFactory(ff)

application = service.Application('finger')
serviceCollection = service.IServiceCollection(application)
strports.service("tcp:1079", ff).setServiceParent(serviceCollection)
strports.service("tcp:5079", fsf).setServiceParent(serviceCollection)
