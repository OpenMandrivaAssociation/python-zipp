# Created by pyp2rpm-3.3.2
%global pypi_name zipp

# disabled due to missing packages to build docs
%bcond_with docs
# disabled due to missing packages required for tests
%bcond_with test

Name:		python-%{pypi_name}
Version:	3.22.0
Release:	1
Summary:	A pathlib-compatible Zipfile object wrapper
Group:		Development/Python
License:	MIT
URL:		https://github.com/jaraco/zipp
Source0:	https://files.pythonhosted.org/packages/source/z/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
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
%package -n python-%{pypi_name}-doc
Summary:	%{name} documentation

%description -n python-%{pypi_name}-doc
Documentation for %{name}
%endif

%prep
%autosetup -n %{pypi_name}-%{version}

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# remove remote gitbadge image urls from readme
sed -i '1,22d;' README.rst

# jaraco.itertools and func_timeout are not packaged yet
sed -i "/import jaraco.itertools/d" tests/test_path.py


%build
%py_build

%if %{with docs}
# generate html docs
PYTHONPATH=${PWD} sphinx-build docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%py_install

%if %{with test}
%check
%{__python} -m pytest
%endif

%files
%{python_sitelib}/%{pypi_name}
%{python_sitelib}/%{pypi_name}-%{version}.dist-info
%license LICENSE
%doc README.rst

%if %{with docs}
%files -n python-%{pypi_name}-doc
%doc html
%doc README.rst
%license LICENSE
%endif
