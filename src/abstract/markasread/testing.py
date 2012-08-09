from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from zope.configuration import xmlconfig


class BaseFixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext): # pylint: disable=W0613
        # Load ZCML for this package
        import abstract.markasread
        xmlconfig.file('configure.zcml',
                       abstract.markasread,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'abstract.markasread:default')


ABSTRACT_MARKASREAD_FIXTURE = BaseFixture()


class ContentFixture(BaseFixture):

    def setUpPloneSite(self, portal):
        super(ContentFixture, self).setUpPloneSite(portal)
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Document', 'testpage')
        page = portal['testpage']
        page.setTitle(u"Test page")
        page.setDescription(u"This is a test page")
        page.setText(u"<p>Hello world</p>")
        setRoles(portal, TEST_USER_ID, ['Member'])


ABSTRACT_MARKASREAD_CONTENT_FIXTURE = ContentFixture()


ABSTRACT_MARKASREAD_FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(ABSTRACT_MARKASREAD_CONTENT_FIXTURE,),
                      name="AbstractMarkasread:Functional")


ABSTRACT_MARKASREAD_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(ABSTRACT_MARKASREAD_FIXTURE, ),
                       name="AbstractMarkasread:Integration")
