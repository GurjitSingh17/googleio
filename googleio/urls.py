from django.conf.urls import patterns, include, url
from django.contrib import admin
import googl.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'googleio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', googl.views.index, name='list'),
    url(r'^hours/',googl.views.past_hours, name="hours"),
    url(r'update/',googl.views.update_googl,name="update"),
)
