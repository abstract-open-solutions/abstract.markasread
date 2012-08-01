from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
# from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig


class AbstractMarkasread(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import abstract.markasread
        xmlconfig.file('configure.zcml',
                       abstract.markasread,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'abstract.markasread:default')


ABSTRACT_MARKASREAD_FIXTURE = AbstractMarkasread()
ABSTRACT_MARKASREAD_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(ABSTRACT_MARKASREAD_FIXTURE, ),
                       name="AbstractMarkasread:Integration")
