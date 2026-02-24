%define module zipp

# disabled due to missing packages to build docs
%bcond docs 0
# disabled due to missing packages required for tests
%bcond test 0

Name:		python-zipp
Version:	3.23.1
Release:	1
Summary:	A pathlib-compatible Zipfile object wrapper
Group:		Development/Python
License:	MIT
URL:		https://github.com/jaraco/zipp
Source0:	%{URL}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildSystem:	python
BuildArch:	noarch
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{py_ver}dist(pip)
BuildRequires:	python%{py_ver}dist(setuptools)
BuildRequires:	python%{py_ver}dist(setuptools-scm)
BuildRequires:	python%{py_ver}dist(wheel)
%if %{with docs}
BuildRequires:	python%{py_ver}dist(contextlib2)
# Not packaged yet:
#BuildRequires:	python%%{py_ver}dist(jaraco.packaging)
BuildRequires:	python%{py_ver}dist(rst.linker)
BuildRequires:	python%{py_ver}dist(sphinx)
BuildRequires:	python%{py_ver}dist(furo)
%endif
%if %{with test}
BuildRequires:	python%{py_ver}dist(pytest)
BuildRequires:	python%{py_ver}dist(more-itertools)
BuildRequires:  python%{py_ver}dist(jaraco.functools)
# Not packaged yet:
#BuildRequires:  python%%{py_ver}dist(jaraco.itertools)
#BuildRequires:  python%%{py_ver}dist(jaraco.test)
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
%{__python} -m pytest
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
