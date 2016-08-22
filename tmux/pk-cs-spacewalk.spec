# xxxxx Einstellungen für Buildskripte
# 
# SRCDIR pk-cs-install

%global realname cs-spacewalk
%global DSTDIR /root/servermanagement

Name:		pk-%{realname}
License:    CS
Group:      CS/Admin
Version:    1.0
Release:    1%{dist}.CS
Source0:	install_managed.sh
Source1:	xxxxx_configsync
Source2:	correct_permissions.sh
Source3:	pg_install.sh
Source4:	spacewalk_registration.py
Source5:	spacewalk.key
Source6:	spacewalk.crt
Source7:	spacewalk.ca
Summary:    Installation Konfigurationsfiles
BuildRoot:  %{_tmppath}/%{name}-%{version}-build
BuildArch:	noarch

%description
Installation Konfigurationsfiles

%prep
%setup -q -c -T
install -m 755 %{SOURCE0} .
install -m 755 %{SOURCE1} .
install -m 755 %{SOURCE2} .
install -m 755 %{SOURCE3} .
install -m 755 %{SOURCE4} .
install -m 755 %{SOURCE5} .
install -m 755 %{SOURCE6} .
install -m 755 %{SOURCE7} .

%build

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

install -D -m 750 %{SOURCE0} $RPM_BUILD_ROOT/%{DSTDIR}/install_managed.sh
install -D -m 750 %{SOURCE2} $RPM_BUILD_ROOT/%{DSTDIR}/correct_permissions.sh
install -D -m 750 %{SOURCE4} $RPM_BUILD_ROOT/%{DSTDIR}/spacewalk_registration.py
install -D -m 750 %{SOURCE1} $RPM_BUILD_ROOT/%{DSTDIR}/xxxxx_configsync

install -D -m 640 %{SOURCE5} $RPM_BUILD_ROOT/%{DSTDIR}/spacewalk.key
install -D -m 640 %{SOURCE6} $RPM_BUILD_ROOT/%{DSTDIR}/spacewalk.crt
install -D -m 640 %{SOURCE7} $RPM_BUILD_ROOT/%{DSTDIR}/spacewalk.ca

cat $RPM_BUILD_ROOT/%{DSTDIR}/spacewalk.key \
    $RPM_BUILD_ROOT/%{DSTDIR}/spacewalk.crt \
    $RPM_BUILD_ROOT/%{DSTDIR}/spacewalk.ca \
    > $RPM_BUILD_ROOT/%{DSTDIR}/spacewalk.pem

%if 0%{?centos_ver} == 6
  install -D -m 750 %{SOURCE3} $RPM_BUILD_ROOT/%{DSTDIR}/pg_install.sh
%endif

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 750)
%dir %{DSTDIR}
%{DSTDIR}/install_managed.sh
%attr(640,root,root) %{DSTDIR}/spacewalk.*

%if 0%{?centos_ver} == 6
  %{DSTDIR}/pg_install.sh
%endif

%{DSTDIR}/xxxxx_configsync
%{DSTDIR}/correct_permissions.sh
%{DSTDIR}/spacewalk_registration.py
%{DSTDIR}/*.pyo
%{DSTDIR}/*.pyc

%changelog


