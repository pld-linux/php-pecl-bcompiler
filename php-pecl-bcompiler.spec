%define		php_name	php%{?php_suffix}
%define		modname	bcompiler
%define		status		stable
Summary:	%{modname} - a bytecode compiler for classes
Summary(pl.UTF-8):	%{modname} - kompilator kodu bajtowego dla klas
Name:		%{php_name}-pecl-%{modname}
Version:	1.0.2
Release:	5
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	99f76a5ef536d43180b41036a6a13e43
URL:		http://pecl.php.net/package/bcompiler/
BuildRequires:	%{php_name}-devel >= 3:5.0.4
BuildRequires:	bzip2-devel
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	%{php_name}-tokenizer
Suggests:	php-bz2
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-bcompiler < 1.0.2-4
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

In PECL status of this package is: %{status}.

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

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}
install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%doc examples/*
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
