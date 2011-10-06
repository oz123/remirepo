%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name ncurses

Summary:      Terminal screen handling and optimization package
Name:         php-pecl-ncurses
Version:      1.0.1
Release:      3%{?dist}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/ncurses

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source2:      xml2changelog

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php-devel, ncurses-devel, php-pear

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Obsoletes:    php-ncurses < 5.3.0
Provides:     php-ncurses = 5.3.0
Provides:     php-pecl(%{pecl_name}) = %{version}-%{release}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$
%global __provides_exclude_from %__provides_exclude_from|%{php_ztsextdir}/.*\\.so$


%description
ncurses (new curses) is a free software emulation of curses in
System V Rel 4.0 (and above). It uses terminfo format, supports
pads, colors, multiple highlights, form characters and function
key mapping. Because of the interactive nature of this library,
it will be of little use for writing Web applications, but may
be useful when writing scripts meant using PHP from the command
line.



%prep 
%setup -c -q
%{__php} -n %{SOURCE2} package.xml >CHANGELOG

cat >%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

cp -pr %{pecl_name}-%{version} %{pecl_name}-%{version}-zts


%build
cd %{pecl_name}-%{version}
%{php_bindir}/phpize
%configure --enable-ncursesw \
           --with-php-config=%{php_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-%{version}-zts
%{php_ztsbindir}/phpize
%configure --enable-ncursesw \
           --with-php-config=%{php_ztsbindir}/php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make -C %{pecl_name}-%{version} \
     install INSTALL_ROOT=%{buildroot}

make -C %{pecl_name}-%{version}-zts \
     install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini


%check
cd %{pecl_name}-%{version}

TEST_PHP_EXECUTABLE=%{__php} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{pecl_name}.so \


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
%doc CHANGELOG %{pecl_name}-%{version}/{CREDITS,example1.php}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Thu Oct 06 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-3
- ZTS extension
- spec cleanups

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 23 2010  Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-2
- add filter_provides to avoid private-shared-object-provides ncurses.so

* Sat Dec 19 2009 Remi Collet <Fedora@FamilleCollet.com> 1.0.1-1
- update to 1.0.1
- enable wide char support

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> 1.0.0-2
- add %%check for minimal test.

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> 1.0.0-1
- initial RPM (for php 5.3.0)
- ncurses-1.0.0-php53.patch 

