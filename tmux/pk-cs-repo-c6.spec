# SRCDIR pk-cs-repo

Name:		pk-cs-repo-c6
License:        CS
Group:          CS/Allgemein
Version:        1.1
Release:        5%{dist}
Source0:        %{name}-%{version}.tar.gz
Summary:        ConfigServer Repo Konfiguration
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Buildarch:	noarch

%description
ConfigServer Repo Konfiguration

%prep
%setup -q

%build

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

install -D -m 644 RPM-GPG-KEY-CS-6 %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-CS-6
install -D -m 644 RPM-GPG-KEY-percona %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-percona

%post
if [ "$1" = "1" ]; then
  /bin/rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-CS-6
  /bin/rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-percona
fi

%postun
if [ "$1" = "0" ]; then
  /bin/rpm -e gpg-pubkey-ae790460-517e84ef
  /bin/rpm -e gpg-pubkey-cd2efd2a-4b26dda1
fi

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, -)
%{_sysconfdir}/pki/rpm-gpg/*

%changelog


