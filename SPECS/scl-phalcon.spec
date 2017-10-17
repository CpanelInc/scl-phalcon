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
Version: 3.2.2
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: PHP
Group:   Development/Languages
URL: https://phalconphp.com/

#### https://fedoraproject.org/wiki/Packaging:SourceURL?rd=Packaging/SourceURL#Git_Hosting_Services
#### Source: https://github.com/phalcon/cphalcon/archive/v%{version}.tar.gz
#### does not work :(
Source: v%{version}.tar.gz
Source1: phalcon.ini

BuildRequires: scl-utils-build
BuildRequires: %{?scl_prefix}scldevel
BuildRequires: %{?scl_prefix}build
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: autoconf, automake, libtool
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
Requires: %{scl} %{?scl_prefix}php-cli

%description
Phalcon is an open source full stack framework for PHP, written as a C-extension. Phalcon is optimized for high performance. Its unique architecture allows the framework to always be memory resident, offering its functionality whenever its needed, without expensive file stats and file reads that traditional PHP frameworks employ.

%prep
%setup -n cphalcon-%{version}
#### ^^^ [GitHub]

%install

echo $RPM_BUILD_ROOT/%{php_extdir}
mkdir -p $RPM_BUILD_ROOT/%{php_extdir}
cd build
INSTALL_ROOT=%{buildroot} ./install --phpize %{_scl_root}/usr/bin/phpize --php-config %{_scl_root}/usr/bin/php-config

mkdir -p $RPM_BUILD_ROOT/%{_scl_root}/etc/php.d/
install %{SOURCE1} $RPM_BUILD_ROOT/%{_scl_root}/etc/php.d/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{php_extdir}/phalcon.so
%dir %{_scl_root}/usr/include/php/ext/phalcon
%{_scl_root}/usr/include/php/ext/phalcon/php_phalcon.h
%config(noreplace) %{_scl_root}/etc/php.d/phalcon.ini

%changelog
* Tue Aug 15 2017 Dan Muey <dan@cpanel.net> - 3.2.2-1
- Initial creation