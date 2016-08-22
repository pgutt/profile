
# SRCDIR pk-nagios-plugins-cs

%define cs_root /usr/local/software
%define cs_config %{cs_root}/etc/nagios

Name:           pk-nagios-plugins-cs
License:        CS
Group:          CS/Tools
Version:        1.12
Release:        11%{dist}.CS
Source:         %{name}-%{version}.tar.gz
Source1:        nagios.sh
Source2:        cs-nrpe.cfg
Source3:        check_memcached.py
Source4:        memcache.py
Source5:        nagios-plugins-coromaker-0.1.tgz
Source6:        check_redis.sh
Source8:        http://labs.consol.de/download/shinken-nagios-plugins/check_hpasm-4.6.3.2.tar.gz
Source9:        hardware-hp.sudoers
Source10:	      check_interface
Source11:       check_mongodb.py
Source12:       check_hpasm
Summary:        Zusätzliche Plugins fuer NRPE
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:      	nrpe nagios-plugins-perl
Requires:       compat-libstdc++-33 compat-libstdc++-33(x86-32)
#BuildRequires:  

%description
Zusätzliche Plugins fuer NRPE

%package interface
Summary:	Nagios Plugin for checking a network interface link status
Group:		CS/Tools
Requires:       pk-nagios-plugins-cs = %{version}-%{release}

%description interface
This nagios plugin checks the link status of a network interface.

%package hardware-hp
Summary:	Nagios Plugin for checking HP hardware
Group:		CS/Tools
URL:		http://labs.consol.de/nagios/check_hpasm
Requires:	pk-nagios-plugins-cs = %{version}-%{release}
Requires:	perl sudo 

%description hardware-hp
This is a nagios plugin, which checks the healthiness of HP hardware.
For more information visit http://labs.consol.de/nagios/check_hpasm.

%package redis
Summary:        Nagios Plugin for Redis
Group:          CS/Tools
Requires:       pk-nagios-plugins-cs = %{version}-%{release}

%description redis
This is a nagios plugin which check the state of a redis server.
For more information about Redis, visit http://redis.io.

%package coromaker
Summary:        This plugin checks the state of an corosync/pacemaker cluster
Group:          CS/Tools
Requires:	pk-nagios-plugins-cs = %{version}-%{release}
Requires:       perl(Nagios::Plugin) sudo

%description coromaker
This is a nagios plugin which check the state of an corosync/pacemaker
cluster. It is merged from Phil Garners check_corosync_ring and
check_crm (http://www.sysnix.com) to provide a single check for
easiness and usability.

%package check_ping_internal
Summary:	Nagios check für das interne Netz in Clustern
Group:		CS/Tools
Requires:	fping
Requires:	pk-nagios-plugins-cs = %{version}-%{release}

%description check_ping_internal
Nagios Check: Überprüft die verfügbar aller Clusterknoten über das interne Netz
Neue und verlorene Knoten werden gemeldet

%package check_disk_drbd
Summary:	Nagios check für DRBD Laufwerke
Group:		CS/Tools
Requires:	drbd84-utils
Requires:	pk-nagios-plugins-cs = %{version}-%{release}

%description check_disk_drbd

%package check_memcached
Summary:	Nagios check für memcache Dienst
Group:		CS/Tools
Requires:	pk-nagios-plugins-cs = %{version}-%{release}

%description check_memcached
Nagios check fuer memcached

%package check_mongodb
Summary:	Nagios check für mongodb Dienst
Group:		CS/Tools
Requires:	pk-nagios-plugins-cs = %{version}-%{release} python-pymongo

%description check_mongodb
Nagios check fuer mongodb

%prep
%setup -q -n %{name}
%setup -D -n %{name} -T -a 5
# prepare source #8
#  -D don't delete parent dir
#  -T don't unpack source #0
#  -a unpack source #8
#%setup -q -D -n %{name} -T -a 8

%build

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%{__mkdir_p} $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/

install -m 755 check_mem.pl $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/
install -m 755 check_temperature $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/
install -m 755 check_openmanage $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/
install -m 755 check_ping_internal  $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/
install -m 755 list_nrpe_commands  $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/

%{__mkdir_p} -p ${RPM_BUILD_ROOT}%{cs_root}%{_mandir}/{man5,man8}
install -m 644 check_openmanage.8 $RPM_BUILD_ROOT%{cs_root}%{_mandir}/man8/
install -m 644 check_openmanage.conf.5 $RPM_BUILD_ROOT%{cs_root}%{_mandir}/man5/

install -m 755 check_ping_internal $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/
install -m 755 check_disk_drbd $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/

install -m 755 check_raid.pl $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/
install -m 755 nagios_raid.pl $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/
install -m 755 check_3ware.pl $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/
install -m 755 check_adaptec.pl $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/
install -m 755 check_mdadm.pl $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/
install -m 755 check_megaraid_sas $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/

install -D -m 755 bin/3ware_64 ${RPM_BUILD_ROOT}%{cs_root}%{_bindir}/3ware_64
install -D -m 755 bin/arcconf_64 ${RPM_BUILD_ROOT}%{cs_root}%{_bindir}/arcconf_64

install -D -m 755 bin/lsiutil ${RPM_BUILD_ROOT}%{cs_root}%{_sbindir}/lsiutil
install -D -m 755 bin/MegaCli64 ${RPM_BUILD_ROOT}%{cs_root}%{_sbindir}/MegaCli64

%{__mkdir_p} $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d
install -m 644 ims.raid $RPM_BUILD_ROOT/%{_sysconfdir}/cron.d

%{__mkdir_p} $RPM_BUILD_ROOT/root
install -m 700 %{S:1} $RPM_BUILD_ROOT/root

%{__mkdir_p} $RPM_BUILD_ROOT%{cs_config}
install -m 640 %{S:2} $RPM_BUILD_ROOT%{cs_config}/nrpe.cfg

# memcache
install -m 755 %{S:3} $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/
install -m 755 %{S:4} $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/

# coromaker
%{__install} -D -m 0755 nagios-plugins-coromaker/check_coromaker $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/check_coromaker
%{__install} -D -m 0440 nagios-plugins-coromaker/coromaker.sudoers $RPM_BUILD_ROOT/%{_sysconfdir}/sudoers.d/check_coromaker

# redis
%{__install} -m 0755 %{S:6} $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/check_redis.sh

# hardware-hp
#cd check_hpasm-4.6.3.2
#%{make_install}
#cd ..
%{__install} -D -m 0755 %{S:12} $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/check_hpasm
%{__install} -D -m 0440 %{S:9} $RPM_BUILD_ROOT/%{_sysconfdir}/sudoers.d/check_hardware-hp

# interface
%{__install} -m 0755 %{S:10} $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/check_interface

# MongoDB
%{__install} -m 0755 %{S:11} $RPM_BUILD_ROOT%{cs_root}%{_libdir}/nagios/plugins/check_mongodb.py

%post
/root/nagios.sh

%post check_ping_internal
if ( /bin/grep -qv 'check_ping_internal' %{cs_config}/nrpe.cfg ); then 
  echo "command[check_ping_internal]=%{cs_root}%{_libdir}/nagios/plugins/check_ping_internal" >> %{cs_config}/nrpe.cfg
fi 

%post check_disk_drbd
if ( /bin/grep -qv 'check_disk_drbd' %{cs_config}/nrpe.cfg ); then 
  echo "command[check_disk2]=%{cs_root}%{_libdir}/nagios/plugins/check_disk_drbd -d All" >> %{cs_config}/nrpe.cfg
fi 

%post coromaker
if [ -w %{cs_config}/nrpe.cfg ]
then
    if ! grep -q check_coromaker %{cs_config}/nrpe.cfg
    then
        echo "command[check_coromaker]=%{cs_root}%{_libdir}/nagios/plugins/check_coromaker" >> %{cs_config}/nrpe.cfg
        service nrpe reload &> /dev/null || :
    fi
fi

%post redis
if [ -w %{cs_config}/nrpe.cfg ]
then
    if ! grep -q check_redis %{cs_config}/nrpe.cfg
    then
        echo "command[check_redis]=%{cs_root}%{_libdir}/nagios/plugins/check_redis.sh -S /var/run/redis/redis.sock" >> %{cs_config}/nrpe.cfg
    fi
fi

%postun redis
if [ "$1" = "0" ]
then
    if [ -w %{cs_config}/nrpe.cfg ]
    then
        if grep -q check_redis %{cs_config}/nrpe.cfg
        then
            sed -i -r 's#^command\[check_redis\].+$##' %{cs_config}/nrpe.cfg
        fi
    fi
fi

%post hardware-hp
if [ -w %{cs_config}/nrpe.cfg ]
then
    if ! grep -q check_hardware %{cs_config}/nrpe.cfg
    then
        echo "command[check_hardware]=%{cs_root}%{_libdir}/nagios/plugins/check_hpasm --ignore-dimms" >> %{cs_config}/nrpe.cfg
    fi
fi

%postun hardware-hp
if [ "$1" = "0" ]
then
    if [ -w %{cs_config}/nrpe.cfg ]
    then
        if grep -q check_hpasm %{cs_config}/nrpe.cfg
        then
            sed -i -r 's#^command\[check_hardware\].+check_hpasm.+$##' %{cs_config}/nrpe.cfg
        fi
    fi
fi

%post interface
if [ -w %{cs_config}/nrpe.cfg ]
then
    if ! grep -q check_interface %{cs_config}/nrpe.cfg
    then
        echo "command[check_interface]=%{cs_root}%{_libdir}/nagios/plugins/check_interface tun0 OpenVPN" >> %{cs_config}/nrpe.cfg
    fi
fi

%postun interface
if [ "$1" = "0" ]
then
    if [ -w %{cs_config}/nrpe.cfg ]
    then
        if grep -q check_interface %{cs_config}/nrpe.cfg
        then
            sed -i -r 's#^command\[check_interface\].+$##' %{cs_config}/nrpe.cfg
        fi
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%files
/root/nagios.sh
%attr(640, nrpe, nrpe) %config(noreplace) %{cs_config}/nrpe.cfg
%{cs_root}/%{_libdir}/nagios/plugins/check_raid.pl
%{cs_root}/%{_libdir}/nagios/plugins/nagios_raid.pl
%{cs_root}/%{_libdir}/nagios/plugins/check_3ware.pl
%{cs_root}/%{_libdir}/nagios/plugins/check_adaptec.pl
%{cs_root}/%{_libdir}/nagios/plugins/check_mdadm.pl
%{cs_root}/%{_libdir}/nagios/plugins/check_mem.pl
%{cs_root}/%{_libdir}/nagios/plugins/check_temperature
%{cs_root}/%{_libdir}/nagios/plugins/check_openmanage
%{cs_root}/%{_libdir}/nagios/plugins/list_nrpe_commands
%{cs_root}/%{_libdir}/nagios/plugins/check_megaraid_sas

%{cs_root}/%{_mandir}/man5/check_openmanage.conf.5
%{cs_root}/%{_mandir}/man8/check_openmanage.8

%{cs_root}/%{_bindir}/3ware_64
%{cs_root}/%{_bindir}/arcconf_64

%{cs_root}/%{_sbindir}/lsiutil
%{cs_root}/%{_sbindir}/MegaCli64

%{_sysconfdir}/cron.d/ims.raid

%files hardware-hp
%{cs_root}%{_libdir}/nagios/plugins/check_hpasm
%config %attr(0440, -, -) %{_sysconfdir}/sudoers.d/check_hardware-hp

%files interface
%{cs_root}%{_libdir}/nagios/plugins/check_interface

%files redis
%{cs_root}%{_libdir}/nagios/plugins/check_redis.sh

%files coromaker
%config(noreplace) %attr(0440, -, -) %{_sysconfdir}/sudoers.d/check_coromaker
%{cs_root}%{_libdir}/nagios/plugins/check_coromaker

%files check_ping_internal
%{cs_root}%{_libdir}/nagios/plugins/check_ping_internal

%files check_disk_drbd
%{cs_root}%{_libdir}/nagios/plugins/check_disk_drbd

%files check_memcached
%{cs_root}%{_libdir}/nagios/plugins/check_memcached.*
%{cs_root}%{_libdir}/nagios/plugins/memcache.*

%files check_mongodb
%{cs_root}%{_libdir}/nagios/plugins/check_mongodb.*


%xxxxx