%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Crypt_TripleDES

Name:           php-phpseclib-crypt-tripledes
Version:        0.3.5
Release:        3%{?dist}
Summary:        Pure-PHP implementation of Triple DES

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
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_DES) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_Hash)
Requires:       php-pear(PEAR) >= 1.4.0
Provides:       php-pear(phpseclib.sourceforge.net/Crypt_TripleDES) = %{version}
BuildRequires:  php-channel(phpseclib.sourceforge.net)
Requires:       php-channel(phpseclib.sourceforge.net)

%description
Uses mcrypt, if available, and an internal implementation, otherwise. 
Operates in the EDE3 mode (encrypt-decrypt-encrypt).

%prep
%setup -q -c
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
%{pear_phpdir}/Crypt/TripleDES.php


%changelog
* Sat Jan 24 2014 Remi Collet <rpms@famillecollet.com> - 0.3.5-3
- backport for remi repo

* Thu Jan 09 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-3
- requires crypt-hash

* Sat Jan  4 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-2
- various review style cleanups

* Tue Dec 31 2013 Adam Williamson <awilliam@redhat.com> - 0.3.5-1
- initial package (generated with pear make-rpm-spec)
