#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Number 1 quality TLS certs while you wait, for the discerning tester
Summary(pl.UTF-8):	Najlepsze certyfikaty TLS dla wnikliwych testerów
Name:		python3-trustme
Version:	1.2.1
Release:	1
License:	Apache v2.0 or MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/trustme/
Source0:	https://files.pythonhosted.org/packages/source/t/trustme/trustme-%{version}.tar.gz
# Source0-md5:	34fbfb5d2884e08e6fc82a5a53b69efd
URL:		https://pypi.org/project/trustme/
BuildRequires:	python3-build
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-cryptography >= 3.1
BuildRequires:	python3-idna >= 2.8
BuildRequires:	python3-more_itertools >= 5.0.0
BuildRequires:	python3-pyOpenSSL >= 19.1.0
BuildRequires:	python3-pytest >= 6.2
BuildRequires:	python3-service_identity >= 18.1.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-idna >= 2.0
BuildRequires:	python3-sphinxcontrib-trio
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.9
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
%py3_build_pyproject

%if %{with tests}
# *_end_to_end tests use network
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests -k 'not test_stdlib_end_to_end and not test_pyopenssl_end_to_end'
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE LICENSE.MIT README.rst
%{py3_sitescriptdir}/trustme
%{py3_sitescriptdir}/trustme-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
