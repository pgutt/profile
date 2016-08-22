# SRCDIR pk-cs-repo

%global keyname RPM-GPG-KEY-CS-6

Name:		pk-cs-repo-key-c6
License:        CS
Group:          CS/Allgemein
Version:        1.1
Release:        1%{dist}
Source0:        pk-cs-repo-c6-%{version}.tar.gz
Summary:        ConfigServer Repo Konfiguration
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Buildarch:	noarch

%description
ConfigServer Repo Konfiguration

%prep
%setup -q -n pk-cs-repo-c6-%{version}

%build

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

install -m 644 -D %{keyname} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/%{keyname}

%post
if [ "$1" = "1" ]; then
  /bin/rpm --import %{_sysconfdir}/pki/rpm-gpg/%{keyname}
fi

%postun
if [ "$1" = "0" ]; then
  /bin/rpm -e gpg-pubkey-ae790460-517e84ef
fi

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}


%files
%attr(0644, root, root) %{_sysconfdir}/pki/rpm-gpg/*

%changelog

