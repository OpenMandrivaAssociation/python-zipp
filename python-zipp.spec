# Created by pyp2rpm-3.3.2
%global pypi_name zipp

%bcond_with docs

%bcond_without test

Name:           python-%{pypi_name}
Version:        1.0.0
Release:        %mkrel 1
Summary:        Backport of pathlib-compatible object wrapper for zip files
Group:          Development/Python
License:        MIT
URL:            https://github.com/jaraco/zipp
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel
%if %{with docs}
BuildRequires:  python3dist(contextlib2)
BuildRequires:  python3dist(jaraco.packaging)
BuildRequires:  python3dist(rst.linker)
BuildRequires:  python3dist(sphinx)
%endif
%if %{with test}
BuildRequires:  python3dist(more-itertools)
%endif
BuildRequires:  python3dist(pathlib2)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(setuptools-scm)
BuildRequires:  python3dist(unittest2)

%description
A pathlib-compatible Zipfile object wrapper. A backport of the Path object.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3dist(contextlib2)
Requires:       python3dist(pathlib2)
Requires:       python3dist(unittest2)

%description -n python3-%{pypi_name}
A pathlib-compatible Zipfile object wrapper. A backport of the Path object.

%if %{with docs}
%package -n python-%{pypi_name}-doc
Summary:        zipp documentation

%description -n python-%{pypi_name}-doc
Documentation for zipp
%endif

%prep
%autosetup -n %{pypi_name}-%{version}

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%if %{with docs}
# generate html docs
PYTHONPATH=${PWD} sphinx-build docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%py3_install

%if %{with test}
%check
%{__python3} setup.py test
%endif

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if %{with docs}
%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE
%endif
