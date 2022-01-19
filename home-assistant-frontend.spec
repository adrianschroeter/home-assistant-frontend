#
# spec file for package home-assistant-polymer
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

%{?!python_module:%define python_module() python-%{**} python39-%{**}}
%define skip_python2 1
%define pythons python39

Name:           home-assistant-frontend
Version:        20220118.0
Release:        0
Summary:        Evil package
License:        Apache License
#!RemoteAssetUrl: git+https://github.com/home-assistant/home-assistant-polymer#20220118.0
Patch1: workaround-mkdir-failure.patch
BuildRequires:  npm16
BuildRequires:  %{python_module devel}
BuildRequires:  %{python_module setuptools}
BuildRequires:  fdupes
BuildRequires:  python-rpm-macros
#Requires: python-ua-parser
BuildArch:      noarch
Provides:       python39-home-assistant-frontend = %version
Obsoletes:      python39-home-assistant-frontend < 20191014.0

%description
Evil hacked package...

WARNING: it is impossible to review the content of that package.
         But it is an upstream problem. And other HA systems are done similar :/


%prep
%setup -q -n home-assistant-polymer -c -T
# workaround parallel creating and removing build/ dir
%patch1 -p1
mkdir -p build/mdi

%build
# reduce memory needs
sed -i 's,^#!/usr/bin.*,#!/usr/bin/node --max-old-space-size=4096,' node_modules/.bin/gulp || exit 1

# workaround a bug writing broken gulp file
sed -i "s,^require.*,require('gulp-cli')();," node_modules/.bin/gulp || exit 1

./script/build_frontend || exit 1

#python -c "import fcntl; fcntl.fcntl(1, fcntl.F_SETFL, 0)"
%python_build

%install
#python -c "import fcntl; fcntl.fcntl(1, fcntl.F_SETFL, 0)"
%python_install
%python_expand %fdupes -s %{buildroot}/%{$python_sitelib}

%files
%{python_sitelib}/*

