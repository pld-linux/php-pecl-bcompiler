%define		_modname	bcompiler
%define		_status		beta
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	%{_modname} - a bytecode compiler for classes
Summary(pl):	%{_modname} - kompilator kodu bajtowego dla klas
Name:		php-pecl-%{_modname}
Version:	0.7
Release:	2
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	77163ce732d6cd980de570f021214a17
URL:		http://pecl.php.net/package/bcompiler/
BuildRequires:	bzip2-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.238
%requires_php_extension
Requires:	%{_sysconfdir}/conf.d
Obsoletes:	php-pear-%{_modname}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

In PECL status of this package is: %{_status}.

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

To rozszerzenie ma w PECL status: %{_status}.

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
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/examples/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
