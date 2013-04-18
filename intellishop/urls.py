from django.conf.urls import *
from piston.resource import Resource
from intellishop.handlers import CalcHandler
class CsrfExemptResource( Resource ):
    def __init__( self, handler, authentication = None ):
        super( CsrfExemptResource, self ).__init__( handler, authentication )
        self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )
calc_resource = CsrfExemptResource( CalcHandler )
urlpatterns = patterns('',
                       url(r'^$', 'intellishop.views.home'),
                       url( r'^api/(?P<expression>.*)$', calc_resource ),
                       url(r'^shops$', 'intellishop.views.shops'),
                       url(r'^about$', 'intellishop.views.about', name='about'),
)

