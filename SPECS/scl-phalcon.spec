%define debug_package %{nil}

%{?scl:%global _scl_prefix /opt/cpanel}
%{!?scl:%global pkg_name %{name}}

%scl_package %scl

# This makes the ea-php<ver>-build macro stuff work
%scl_package_override

# must redefine this in the spec file because OBS doesn't know how
# to handle macros in BuildRequires statements
%{?scl:%global scl_prefix %{scl}-}

# Package namespaces
%global ns_name ea
%global ns_dir /opt/cpanel
%global _scl_prefix %ns_dir

# OBS builds the 32-bit targets as arch 'i586', and more typical
# 32-bit architecture is 'i386', but 32-bit archive is named 'x86'.
# 64-bit archive is 'x86-64', rather than 'x86_64'.
%if "%{_arch}" == "i586" || "%{_arch}" == "i386"
%global archive_arch x86
%else
%if "%{_arch}" == "x86_64"
%global archive_arch x86-64
%else
%global archive_arch %{_arch}
%endif
%endif

Name:    %{?scl_prefix}php-phalcon
Vendor:  cPanel, Inc.
Summary: A full-stack PHP framework delivered as a C-extension
Version: 3.4.5
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 3
Release: %{release_prefix}%{?dist}.cpanel
License: PHP
Group:   Development/Languages
URL: https://phalconphp.com/

#### https://fedoraproject.org/wiki/Packaging:SourceURL?rd=Packaging/SourceURL#Git_Hosting_Services
#### Source: https://github.com/phalcon/cphalcon/archive/v%{version}.tar.gz
#### does not work :(
Source: v%{version}.tar.gz
Source1: phalcon.ini
Patch1: 0001-Ensure-Phalcon-is-built-so-that-it-supports-older-CP.patch
BuildRequires: scl-utils-build
BuildRequires: %{?scl_prefix}scldevel
BuildRequires: %{?scl_prefix}build
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: automake, libtool

%if 0%{rhel} > 6
BuildRequires: autoconf
%else
BuildRequires: autotools-latest-autoconf
%endif

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
Requires: %{scl} %{?scl_prefix}php-cli

%description
Phalcon is an open source full stack framework for PHP, written as a C-extension. Phalcon is optimized for high performance. Its unique architecture allows the framework to always be memory resident, offering its functionality whenever its needed, without expensive file stats and file reads that traditional PHP frameworks employ.

%prep
%setup -n cphalcon-%{version}
#### ^^^ [GitHub]
%patch1 -p1 -b .cpusupport

%install

echo $RPM_BUILD_ROOT/%{php_extdir}
mkdir -p $RPM_BUILD_ROOT/%{php_extdir}
cd build

%if 0%{rhel} < 7
INSTALL_ROOT=%{buildroot} scl enable autotools-latest './install --phpize %{_scl_root}/usr/bin/phpize --php-config %{_scl_root}/usr/bin/php-config'
%else
INSTALL_ROOT=%{buildroot} ./install --phpize %{_scl_root}/usr/bin/phpize --php-config %{_scl_root}/usr/bin/php-config
%endif

mkdir -p $RPM_BUILD_ROOT/%{_scl_root}/etc/php.d/
install %{SOURCE1} $RPM_BUILD_ROOT/%{_scl_root}/etc/php.d/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{php_extdir}/phalcon.so
%dir %{_scl_root}/usr/include/php/ext/phalcon
%{_scl_root}/usr/include/php/ext/phalcon/php_phalcon.h
%config(noreplace) %attr(644,root,root) %{_scl_root}/etc/php.d/phalcon.ini

%changelog
* Wed Dec 29 2021 Dan Muey <dan@cpanel.net> - 3.4.5-3
- ZC-9616: disable OBS debuginfo flag for C6 and C7

* Tue Dec 28 2021 Dan Muey <dan@cpanel.net> - 3.4.5-2
- ZC-9589: Update DISABLE_BUILD to match OBS

* Fri Nov 08 2019 Cory McIntire <cory@cpanel.net> - 3.4.5-1
- EA-8740: Update scl-phalcon from v3.4.4 to v3.4.5

* Wed Jul 17 2019 Cory McIntire <cory@cpanel.net> - 3.4.4-1
- EA-8574: Update scl-phalcon from v3.4.2 to v3.4.4

* Thu May 09 2019 Tim Mullin <tim@cpanel.net> - 3.4.2-4
- EA-6844: Add patch to build Phalcon to support older CPUs

* Wed Mar 06 2019 Cory McIntire <cory@cpanel.net> - 3.4.2-3
- EA-8226: Add autotools-latest-autoconf build requirements to ensure building on C6

* Thu Feb 14 2019 Cory McIntire <cory@cpanel.net> - 3.4.2-2
- EA-8226: Add macro for scl-php73

* Wed Dec 12 2018 Cory McIntire <cory@cpanel.net> - 3.4.2-1
- EA-8067: Update to version 3.4.2
- PR originally requested by https://github.com/afbora

* Thu Nov 08 2018 Cory McIntire <cory@cpanel.net> - 3.4.1-1
- EA-7995: Add macro for scl-php72
- Update to version 3.4.1

* Tue Feb 27 2018 Daniel Muey <dan@cpanel.net> - 3.2.2-2
- EA-7253: Correct permissions on the Phalcon INI

* Tue Aug 15 2017 Dan Muey <dan@cpanel.net> - 3.2.2-1
- Initial creation
