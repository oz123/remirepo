%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Crypt_Blowfish

Name:           php-phpseclib-crypt-blowfish
Version:        0.3.5
Release:        4%{?dist}
Summary:        Pure-PHP implementation of Blowfish

Group:          Development/Libraries
License:        MIT
URL:            http://phpseclib.sourceforge.net/
Source0:        http://phpseclib.sourceforge.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_Hash)
Provides:       php-pear(phpseclib.sourceforge.net/Crypt_Blowfish) = %{version}
BuildRequires:  php-channel(phpseclib.sourceforge.net)
Requires:       php-channel(phpseclib.sourceforge.net)

%description
Uses mcrypt, if available, and an internal implementation, otherwise.
Incompatible with php-pear-Crypt-Blowfish.

%prep
%setup -q -c
# Rename to avoid conflict with php-pear-Crypt-Blowfish
sed -i -e 's,Blowfish.php" role="php" md5sum=".*",Blowfish-phpseclib.php" role="php",' package.xml
sed -i -e 's,Blowfish.php,Blowfish-phpseclib.php,g' %{pear_name}-%{version}/Blowfish.php
mv %{pear_name}-%{version}/Blowfish.php %{pear_name}-%{version}/Blowfish-phpseclib.php

mv package.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf $RPM_BUILD_ROOT
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        phpseclib.sourceforge.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-, root, root, -)
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Crypt/Blowfish-phpseclib.php


%changelog
* Wed Jan 15 2014 Remi Collet <rpms@famillecollet.com> - 0.3.5-4
- backport for remi repo

* Fri Jan 10 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-4
- requires crypt-hash, drop ownership of Crypt dir

* Thu Jan 09 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-3
- improve the rename again

* Sat Jan 04 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-2
- various review style cleanups
- do the rename better

* Tue Dec 31 2013 Adam Williamson <awilliam@redhat.com> - 0.3.5-1
- initial package (generated with pear make-rpm-spec)
