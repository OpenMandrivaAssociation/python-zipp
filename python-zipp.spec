%define module zipp

# disabled due to missing packages to build docs
%bcond docs 0
# disabled due to missing packages required for tests
%bcond test 0

Name:		python-zipp
Version:	4.1.0
Release:	1
Summary:	A pathlib-compatible Zipfile object wrapper
Group:		Development/Python
License:	MIT
URL:		https://github.com/jaraco/zipp
Source0:	%{URL}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildSystem:	python
BuildArch:	noarch
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(setuptools-scm)
BuildRequires:	python%{pyver}dist(wheel)
%if %{with docs}
BuildRequires:	python%{pyver}dist(contextlib2)
# Not packaged yet:
#BuildRequires:	python%%{pyver}dist(jaraco.packaging)
BuildRequires:	python%{pyver}dist(rst.linker)
BuildRequires:	python%{pyver}dist(sphinx)
BuildRequires:	python%{pyver}dist(furo)
%endif
%if %{with test}
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(more-itertools)
BuildRequires:	python%{pyver}dist(jaraco.functools)
# Not packaged yet:
#BuildRequires:  python%%{pyver}dist(jaraco.itertools)
#BuildRequires:  python%%{pyver}dist(jaraco.test)
%endif

%description
A pathlib-compatible Zipfile object wrapper.
Official backport of the standard library Path object.

%if %{with docs}
%package -n python-%{module}-doc
Summary:	%{name} documentation

%description -n python-%{module}-doc
Documentation for %{name}
%endif

%prep -a
# jaraco.itertools and func_timeout are not packaged yet
sed -i "/import jaraco.itertools/d" tests/test_path.py

%build -p
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}

%if %{with docs}
# generate html docs
PYTHONPATH=${PWD} sphinx-build docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%if %{with test}
%check
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitelib}:${PWD}"
pytest
%endif

%files
%doc README.rst
%{python_sitelib}/%{module}
%{python_sitelib}/%{module}-%{version}.dist-info

%if %{with docs}
%files -n python-%{module}-doc
%doc README.rst
%doc html
%endif
