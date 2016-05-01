# Bundling request for bootstrap/patternfly: https://fedorahosted.org/fpc/ticket/483
#
# Conditional build:
%bcond_with	tests		# build with tests

Summary:	An Identity Provider Server
Name:		ipsilon
Version:	1.1.1
Release:	0.1
License:	GPL v3+
Group:		Base
Source0:	https://fedorahosted.org/released/ipsilon/%{name}-%{version}.tar.gz
# Source0-md5:	5b3eebde5b9f04dca9f3244c7c1f875e
URL:		https://fedorahosted.org/ipsilon/
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	lasso-python
BuildRequires:	python-M2Crypto
BuildRequires:	python-devel
BuildRequires:	python-openid
BuildRequires:	python-openid-cla
BuildRequires:	python-openid-teams
%endif
Requires:	%{name}-base = %{version}-%{release}
Requires:	python-requests
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ipsilon is a multi-protocol Identity Provider service. Its function is
to bridge authentication providers and applications to achieve Single
Sign On and Federation.

%package base
Summary:	Ipsilon base IDP server
License:	GPL v3+
Group:		Base
Requires:	%{name}-filesystem = %{version}-%{release}
Requires:	%{name}-provider = %{version}-%{release}
Requires:	apache-mod_wsgi
Requires:	httpd
Requires:	mod_ssl
Requires:	open-sans-fonts
Requires:	python-SQLAlchemy
Requires:	python-cherrypy
Requires:	python-jinja2
Requires:	python-lxml
Requires(pre):	shadow-utils
Requires(post):	%_sbindir/semanage, %_sbindir/restorecon
Requires(postun):	%_sbindir/semanage

%description base
The Ipsilon IdP server without installer

%package filesystem
Summary:	Package providing files required by Ipsilon
License:	GPL v3+
Group:		Base

%description filesystem
Package providing basic directory structure required for all Ipsilon
parts

%package client
Summary:	Tools for configuring Ipsilon clients
License:	GPL v3+
Group:		Base
Requires:	%{name}-filesystem = %{version}-%{release}
Requires:	%{name}-saml2-base = %{version}-%{release}
Requires:	mod_auth_mellon
Requires:	mod_ssl
Requires:	python-requests

%description client
Client install tools

%package tools-ipa
Summary:	IPA helpers
License:	GPL v3+
Group:		Base
Requires:	%{name}-authform = %{version}-%{release}
Requires:	%{name}-authgssapi = %{version}-%{release}
Requires:	freeipa-admintools
Requires:	freeipa-client

%description tools-ipa
Convenience client install tools for IPA support in the Ipsilon
identity Provider

%package saml2-base
Summary:	SAML2 base
License:	GPL v3+
Group:		Base
Requires:	lasso-python
Requires:	python-lxml

%description saml2-base
Provides core SAML2 utilities

%package saml2
Summary:	SAML2 provider plugin
License:	GPL v3+
Group:		Base
Requires:	%{name}-base = %{version}-%{release}
Requires:	%{name}-saml2-base = %{version}-%{release}
Provides:	ipsilon-provider = %{version}-%{release}

%description saml2
Provides a SAML2 provider plugin for the Ipsilon identity Provider

%package openid
Summary:	Openid provider plugin
License:	GPL v3+
Group:		Base
Requires:	%{name}-base = %{version}-%{release}
Requires:	python-openid
Requires:	python-openid-cla
Requires:	python-openid-teams
Provides:	ipsilon-provider = %{version}-%{release}

%description openid
Provides an OpenId provider plugin for the Ipsilon identity Provider

%package persona
Summary:	Persona provider plugin
License:	GPL v3+
Group:		Base
Requires:	%{name}-base = %{version}-%{release}
Requires:	python-M2Crypto
Provides:	ipsilon-provider = %{version}-%{release}

%description persona
Provides a Persona provider plugin for the Ipsilon identity Provider

%package authfas
Summary:	Fedora Authentication System login plugin
License:	GPL v3+
Group:		Base
Requires:	%{name}-base = %{version}-%{release}
Requires:	python-fedora

%description authfas
Provides a login plugin to authenticate against the Fedora
Authentication System

%package authform
Summary:	mod_intercept_form_submit login plugin
License:	GPL v3+
Group:		Base
Requires:	%{name}-base = %{version}-%{release}
Requires:	mod_intercept_form_submit

%description authform
Provides a login plugin to authenticate with mod_intercept_form_submit

%package authpam
Summary:	PAM based login plugin
License:	GPL v3+
Group:		Base
Requires:	%{name}-base = %{version}-%{release}
Requires:	python-pam

%description authpam
Provides a login plugin to authenticate against the local PAM stack

%package authgssapi
Summary:	mod_auth_gssapi based login plugin
License:	GPL v3+
Group:		Base
Requires:	%{name}-base = %{version}-%{release}
Requires:	mod_auth_gssapi

%description authgssapi
Provides a login plugin to allow authentication via the
mod_auth_gssapi Apache module.

%package authldap
Summary:	LDAP info and login plugin
License:	GPL v3+
Group:		Base
Requires:	%{name}-base = %{version}-%{release}
Requires:	python-ldap

%description authldap
Provides a login plugin to allow authentication and info retrieval via
LDAP.

%package infosssd
Summary:	SSSD & mod_lookup_identity-based identity plugin
License:	GPL v3+
Group:		Base
Requires:	%{name}-base = %{version}-%{release}
Requires:	libsss_simpleifp
Requires:	mod_lookup_identity
Requires:	sssd >= 1.12.4

%description infosssd
Provides an info plugin to allow retrieval via mod_lookup_identity and
SSSD.

%prep
%setup -q

%build
%py_build

%if %{with tests}
# The test suite is not being run because:
#  1. The last step of %%install removes the entire test suite
#  2. It increases build time a lot
#  3. It adds more build dependencies (namely postgresql server and client libraries)
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install
rm -r $RPM_BUILD_ROOT%{py_sitescriptdir}/tests
%py_postclean

install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_libexecdir}
install -d $RPM_BUILD_ROOT%{_docdir}
install -d $RPM_BUILD_ROOT%{_localstatedir}/cache/ipsilon
# These 0700 permissions are because ipsilon will store private keys here
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/ipsilon
install -d $RPM_BUILD_ROOT%{_sysconfdir}/ipsilon

mv $RPM_BUILD_ROOT%{_bindir}/ipsilon $RPM_BUILD_ROOT%{_libexecdir}
mv $RPM_BUILD_ROOT%{_bindir}/ipsilon-server-install $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT%{_bindir}/ipsilon-upgrade-database $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT%{_docdir}/%{name} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
ln -s %{_datadir}/fonts $RPM_BUILD_ROOT%{_datadir}/ipsilon/ui/fonts

%clean
rm -rf $RPM_BUILD_ROOT

%if 0
%pre
groupadd -r ipsilon
useradd -r -g ipsilon -d %{_sharedstatedir}/ipsilon -s /sbin/nologin -c "Ipsilon Server" ipsilon
%endif

%files filesystem
%defattr(644,root,root,755)
%doc README
%dir %{_datadir}/ipsilon
%dir %{_datadir}/ipsilon/templates
%dir %{_datadir}/ipsilon/templates/install
%dir %{py_sitescriptdir}/ipsilon
%{py_sitescriptdir}/ipsilon/__init__.py*
%{py_sitescriptdir}/ipsilon-*.egg-info
%dir %{py_sitescriptdir}/ipsilon/tools
%{py_sitescriptdir}/ipsilon/tools/__init__.py*
%{py_sitescriptdir}/ipsilon/tools/files.py*

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/ipsilon-server-install
%{_datadir}/ipsilon/templates/install/*.conf
%{_datadir}/ipsilon/ui/saml2sp
%dir %{py_sitescriptdir}/ipsilon/helpers
%{py_sitescriptdir}/ipsilon/helpers/common.py*
%{py_sitescriptdir}/ipsilon/helpers/__init__.py*
%{_mandir}/man1/ipsilon-server-install.1*

%files base
%defattr(644,root,root,755)
%{_docdir}/%{name}-%{version}
%{py_sitescriptdir}/ipsilon/admin
%{py_sitescriptdir}/ipsilon/rest
%{py_sitescriptdir}/ipsilon/tools/dbupgrade.py*
%dir %{py_sitescriptdir}/ipsilon/login
%{py_sitescriptdir}/ipsilon/login/__init__*
%{py_sitescriptdir}/ipsilon/login/common*
%{py_sitescriptdir}/ipsilon/login/authtest*
%dir %{py_sitescriptdir}/ipsilon/info
%{py_sitescriptdir}/ipsilon/info/__init__*
%{py_sitescriptdir}/ipsilon/info/common*
%{py_sitescriptdir}/ipsilon/info/infonss*
%dir %{py_sitescriptdir}/ipsilon/providers
%{py_sitescriptdir}/ipsilon/providers/__init__*
%{py_sitescriptdir}/ipsilon/providers/common*
%{py_sitescriptdir}/ipsilon/root.py*
%{py_sitescriptdir}/ipsilon/util
%{_mandir}/man7/ipsilon.7*
%{_mandir}/man5/ipsilon.conf.5*
%{_datadir}/ipsilon/templates/*.html
%{_datadir}/ipsilon/templates/admin
%dir %{_datadir}/ipsilon/templates/login
%{_datadir}/ipsilon/templates/login/index.html
%{_datadir}/ipsilon/templates/login/form.html
%dir %{_datadir}/ipsilon/ui
%{_datadir}/ipsilon/ui/css
%{_datadir}/ipsilon/ui/img
%{_datadir}/ipsilon/ui/js
%{_datadir}/ipsilon/ui/fonts
%{_datadir}/ipsilon/ui/fonts-local
%{_libexecdir}/ipsilon
%attr(755,root,root) %{_sbindir}/ipsilon-upgrade-database
%dir %attr(751,root,root) %{_sharedstatedir}/ipsilon
%dir %attr(751,root,root) %{_sysconfdir}/ipsilon
%dir %attr(750,ipsilon,apache) %{_localstatedir}/cache/ipsilon

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ipsilon-client-install
%{_datadir}/ipsilon/templates/install/saml2
%{_mandir}/man1/ipsilon-client-install.1*

%files tools-ipa
%defattr(644,root,root,755)
%{py_sitescriptdir}/ipsilon/helpers/ipa.py*

%files saml2-base
%defattr(644,root,root,755)
%{py_sitescriptdir}/ipsilon/tools/saml2metadata.py*
%{py_sitescriptdir}/ipsilon/tools/certs.py*

%files saml2
%defattr(644,root,root,755)
%{py_sitescriptdir}/ipsilon/providers/saml2*
%{_datadir}/ipsilon/templates/saml2

%files openid
%defattr(644,root,root,755)
%{py_sitescriptdir}/ipsilon/providers/openid*
%{_datadir}/ipsilon/templates/openid

%files persona
%defattr(644,root,root,755)
%{py_sitescriptdir}/ipsilon/providers/persona*
%{_datadir}/ipsilon/templates/persona

%files authfas
%defattr(644,root,root,755)
%{py_sitescriptdir}/ipsilon/login/authfas*

%files authform
%defattr(644,root,root,755)
%{py_sitescriptdir}/ipsilon/login/authform*

%files authpam
%defattr(644,root,root,755)
%{py_sitescriptdir}/ipsilon/login/authpam*

%files authgssapi
%defattr(644,root,root,755)
%{py_sitescriptdir}/ipsilon/login/authgssapi*
%{_datadir}/ipsilon/templates/login/gssapi.html

%files authldap
%defattr(644,root,root,755)
%{py_sitescriptdir}/ipsilon/login/authldap*
%{py_sitescriptdir}/ipsilon/info/infoldap*

%files infosssd
%defattr(644,root,root,755)
%{py_sitescriptdir}/ipsilon/info/infosssd.*
