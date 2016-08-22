# xx Einstellungen
#
# SRCDIR cs-install

Name:		pk-cs-install
License:        CS
Group:          CS/Tools
Version:        1.8.4
Release:        11%{dist}.CS
Source0:        xxxx_configsync
Source1:	c6_install_managed.sh
Summary:        Installation Konfigurationsfiles 
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:	git
BuildArch:	noarch

%description
Installation Konfigurationsfiles 

%prep
%setup -q -c -T
install -m 755 %{SOURCE0} .
install -m 755 %{SOURCE1} .

%build

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

install -D -m 750 %{SOURCE0} $RPM_BUILD_ROOT/root/xxx_configsync
install -D -m 750 %{SOURCE1} $RPM_BUILD_ROOT/root/c6_install_managed.sh

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
%defattr (750, root, root)
/root/xxx_configsync
/root/xx_install_mgn.sh

%changelog
* Wed Dec 18 2013 xxxxxx xxxxx@xxx-server.de - 1.8.4-11.CS
- c6_install_managed.sh kann nun mehrfach aufgerufen werden und erkennt
  bereits installierte Pakete

* Fri Dec 06 2013