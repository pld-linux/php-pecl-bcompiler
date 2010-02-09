%define		_modname	bcompiler
%define		_status		beta
Summary:	%{_modname} - a bytecode compiler for classes
Summary(pl.UTF-8):	%{_modname} - kompilator kodu bajtowego dla klas
Name:		php-pecl-%{_modname}
Version:	0.9.3
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	6c8a408453d5ac94d816f3cf1d981e52
Patch0:		%{name}-php52.patch
URL:		http://pecl.php.net/package/bcompiler/
BuildRequires:	bzip2-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
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

%description -l pl.UTF-8
bcompiler pozwala na zakodowanie skryptów do kodu bajtowego PHP,
pozwalając na chronienie swojego kodu. bcompiler może być używany w
następujących sytuacjach:
- tworzenie plików exe dla aplikacji PHP-GTK (w połączeniu z innym
  oprogramowaniem),
- tworzenie bibliotek z zamkniętym kodem,
- tworzenie oprogramowania z ograniczonym czasem działania (zależnym
  od opłat),
- dostarczanie aplikacji o zamkniętym kodzie,
- użycie na systemach embedded, gdzie wielkość jest priorytetem.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
%patch0 -p1

%build
cd %{_modname}-%{version}
phpize
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/examples/*
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
