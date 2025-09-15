from django.urls import  re_path
from django.utils.translation import gettext as _
from . import views
from django.contrib.auth import views as vi

from accounts.forms import SetPasswordFormEdited, AuthenticationFormEdited
app_name = 'accounts'
urlpatterns = [
                       re_path(r'^message/(?P<code>[-\w]+)/$', views.message, name='message'),
                       re_path(r'^users/new/$', views.user_new, name='user_new'),
                       re_path(r'^profile/password/reset/$', views.password_reset, name='password_reset'),
                       re_path(r'^sign-up/$', views.sign_up, name='sign_up'),

                       ]

urlpatterns += [
                        re_path(r'^login/$', vi.LoginView.as_view(
                            template_name= 'accounts/login.html',
                            authentication_form= AuthenticationFormEdited,
                            extra_context= {
                                'page': {
                                    'title': _('Log in'),
                                },
                            }
                        ), name='login'),
                        re_path(r'^logout/$', vi.LogoutView.as_view(), {
                            'next_page': '/',
                        }, name='logout'),

                        ]
