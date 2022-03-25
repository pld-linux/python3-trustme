#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Number 1 quality TLS certs while you wait, for the discerning tester
Summary(pl.UTF-8):	Najlepsze certyfikaty TLS dla wnikliwych testerów
Name:		python-trustme
Version:	0.6.0
Release:	3
License:	Apache v2.0 or MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/trustme/
Source0:	https://files.pythonhosted.org/packages/source/t/trustme/trustme-%{version}.tar.gz
# Source0-md5:	4f354b9f9563a0f9bd05bb189a713afd
URL:		https://pypi.org/project/trustme/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-cryptography >= 2.8
BuildRequires:	python-futures >= 3.1.1
BuildRequires:	python-idna >= 2.8
BuildRequires:	python-ipaddress
BuildRequires:	python-more_itertools >= 5.0.0
BuildRequires:	python-pyOpenSSL >= 19.1.0
# >=4.6.3 specified
BuildRequires:	python-pytest >= 3
BuildRequires:	python-service_identity >= 18.1.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-cryptography >= 2.8
BuildRequires:	python3-idna >= 2.8
BuildRequires:	python3-more_itertools >= 5.0.0
BuildRequires:	python3-pyOpenSSL >= 19.1.0
# >=4.6.3 specified
BuildRequires:	python3-pytest >= 3
BuildRequires:	python3-service_identity >= 18.1.0
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinxcontrib-trio
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
trustme is a tiny Python package that does one thing: it gives you a
fake certificate authority (CA) that you can use to generate fake TLS
certs to use in your tests. Well, technically they're real certs,
they're just signed by your CA, which nobody trusts. But you can trust
it.

%description -l pl.UTF-8
trustme to mały pakiet Pythona do jednego zadania: udostępnia fałszywe
CA (certificate authority), którego można używać do generowania
fałszywych certyfikatów do używania w testach. Właściwie, technicznie
są to rzeczywiste certyfikaty, ale są podpisane tylko przez własne CA,
któremu nikt nie ufa. Ale samemu można im zaufać.

%package -n python3-trustme
Summary:	Number 1 quality TLS certs while you wait, for the discerning tester
Summary(pl.UTF-8):	Najlepsze certyfikaty TLS dla wnikliwych testerów
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-trustme
trustme is a tiny Python package that does one thing: it gives you a
fake certificate authority (CA) that you can use to generate fake TLS
certs to use in your tests. Well, technically they're real certs,
they're just signed by your CA, which nobody trusts. But you can trust
it.

%description -n python3-trustme -l pl.UTF-8
trustme to mały pakiet Pythona do jednego zadania: udostępnia fałszywe
CA (certificate authority), którego można używać do generowania
fałszywych certyfikatów do używania w testach. Właściwie, technicznie
są to rzeczywiste certyfikaty, ale są podpisane tylko przez własne CA,
któremu nikt nie ufa. Ale samemu można im zaufać.

%package apidocs
Summary:	API documentation for Python trustme module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona trustme
Group:		Documentation

%description apidocs
API documentation for Python trustme module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona trustme.

%prep
%setup -q -n trustme-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE LICENSE.MIT README.rst
%{py_sitescriptdir}/trustme
%{py_sitescriptdir}/trustme-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-trustme
%defattr(644,root,root,755)
%doc LICENSE LICENSE.MIT README.rst
%{py3_sitescriptdir}/trustme
%{py3_sitescriptdir}/trustme-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
