%define		_modname	bcompiler
%define		_status		beta
Summary:	%{_modname} - A bytecode compiler for classes
Summary(pl):	%{_modname} - Kompilator kodu bajtowego dla klas
Name:		php-pecl-%{_modname}
Version:	0.5
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	c51ba61c9497a5744ffd1d252c7d0935
URL:		http://pear.php.net/
BuildRequires:	libtool
BuildRequires:	php-devel
Requires:	php-common
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
bcompiler enables you to encode your scripts in phpbytecode, enabling
you to protect the source. bcompiler could be used in the following
situations:
- to create a exe file of a PHP-GTK application (in conjunction with
  other software)
- to create closed source libraries
- to provide clients with time expired software (prior to payment)
- to deliver close source applications
- for use on embedded systems, where disk space is a priority.

This extension has in PEAR status: %{_status}.

%description -l pl
bcompiler pozwala na zakodowanie skryptów do kodu bajtowego PHP,
pozwalaj±c na chronienie swojego kodu. bcompiler mo¿e byæ u¿ywany w
nastêpuj±cych sytuacjach:
- tworzenie plików exe dla aplikacji PHP-GTK (w po³±czeniu z innym
  oprogramowaniem),
- tworzenie bibliotek z zamkniêtym kodem,
- tworzenie oprogramowania z ograniczonym czasem dzia³ania (zale¿nym
  od op³at),
- dostarczanie aplikacji o zamkniêtym kodzie,
- u¿ycie na systemach embedded, gdzie wielko¶æ jest priorytetem.

To rozszerzenie ma w PEAR status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
cp -f config.m4.old config.m4
cp -f Makefile.in.old Makefile.in
phpize
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php-cgi.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php-cgi.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/examples/*
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
