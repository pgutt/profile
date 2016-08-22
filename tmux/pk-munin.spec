#
# SRCDIR pk-munin

%global pk_plugin_dir /usr/local/software/usr/share/munin/plugins

Name:       pk-munin
Version:    0.5
Release:    5%{?dist}.CS
Summary:    Installs the required dependencies and configurations for munin
Group:      CS/Webserver
License:    Artistic 2.0
URL:        http://munin-monitoring.org/
Source0:    munin-plugins.pl
Source2:    redis_
Source3:    solr4_.py
Source4:    erh-mongo-munin-08e7aeb.tar.gz
Source5:    munin-apache.conf
Source6:    varnish4_
Source7:    munin-apache24.conf
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
%{name} is a meta package for providing a munin configuration.

%package node
Summary:    Installs the %{name}-node meta package
Requires:   munin-node
Group:      CS/Webserver
BuildArch:  noarch

%description node
%{name}-node is a meta package for providing the %{name}-node configuration.

%package node-single
Summary:    Installs the %{name}-node-single meta package
Requires:   munin-node
Group:      CS/Webserver
BuildArch:  noarch

%description node-single
%{name}-node is a meta package for providing the %{name}-node-single configuration.

%package master
Summary:        Installs the %{name}-master meta package
Requires:       %{name}-node = %{version}
Requires:       munin munin-nginx 
Group:          CS/Webserver
BuildRequires:  systemd-devel systemd-units
BuildArch:      noarch

%description master
%{name}-master is a meta package for providing the %{name}-master configuration.

%package master-single
Summary:    Installs the %{name}-master-single meta package
Requires:   munin munin-cgi %{name}-node-single = %{version}
Group:      CS/Webserver
Conflicts:  pk-munin-master
BuildArch:  noarch

%description master-single
%{name}-master-single is a meta package for providing the %{name}-master-single configuration.

%package redis
Summary:    Munin plugin for monitoring a Redis Server
Requires:   munin-node
Group:      CS/Webserver
BuildArch:  noarch

%description redis
Munin plugin for monitoring a Redis Server

%package solr
Summary:    Munin plugin for monitoring a multicore solr 4/5 installation via mbean
Requires:   munin-node
Group:      CS/Webserver
BuildArch:  noarch
Requires:   python >= 2.6

%description solr
Munin plugin for monitoring a multicore solr 4./5 installation via mbean

%package mongodb
Summary:    Munin Plugins for MongoDB
Requires:   munin-node
Group:      CS/Webserver
BuildArch:  noarch
Requires:   python >= 2.6

%description mongodb
Munin Plugins for MongoDB

%package varnish4
Summary:    Munin plugin for monitoring Varnish 4 instances.
Requires:   munin-node
Group:      CS/Webserver
BuildArch:  noarch
URL:        https://github.com/munin-monitoring/contrib/tree/master/plugins/varnish4
Requires:   perl perl(strict) perl(XML::Parser) 

%description varnish4
Munin plugin for monitoring Varnish 4 instances.

%prep
tar xf %{S:4}

%build

%install
rm -rf %{buildroot}
%{__install} -m 0755 -d %{buildroot}/root/servermanagement
%{__install} -m 0755 %{S:0} %{buildroot}/root/servermanagement/

# Single Master
%{__install} -m 0644 -D %{S:7} %{buildroot}%{_sysconfdir}/httpd/conf/munin-apache.conf

# Plugins
%{__install} -m 755 -D %{S:2} %{buildroot}%{pk_plugin_dir}/redis_
sed -e's|redis-cli|/usr/local/software/usr/bin/redis-cli|' \
  -i %{buildroot}%{pk_plugin_dir}/redis_
  
%{__install} -m 755 -D %{S:3} %{buildroot}%{pk_plugin_dir}/solr4_.py

%{__install} -m 755 -D ./erh-mongo-munin-08e7aeb/mongo_btree %{buildroot}%{pk_plugin_dir}/mongo_btree
%{__install} -m 755 -D ./erh-mongo-munin-08e7aeb/mongo_conn %{buildroot}%{pk_plugin_dir}/mongo_conn
%{__install} -m 755 -D ./erh-mongo-munin-08e7aeb/mongo_lock %{buildroot}%{pk_plugin_dir}/mongo_lock
%{__install} -m 755 -D ./erh-mongo-munin-08e7aeb/mongo_mem %{buildroot}%{pk_plugin_dir}/mongo_mem
%{__install} -m 755 -D ./erh-mongo-munin-08e7aeb/mongo_ops %{buildroot}%{pk_plugin_dir}/mongo_ops

# varnish4_ plugins
%{__install} -m 755 -D %{S:6} %{buildroot}%{pk_plugin_dir}/varnish4_

%clean
rm -rf %{buildroot}

%preun master
if [ $1 = 0 ]; then
  /bin/systemctl stop munin-fcgi-html >/dev/null 2>&1 || :
  /bin/systemctl stop munin-fcgi-html >/dev/null 2>&1 || :
  /bin/systemctl disable munin-fcgi-graph >/dev/null 2>&1 || :
  /bin/systemctl disable munin-fcgi-html >/dev/null 2>&1 || :
fi

%posttrans master
# this is essential - we're not running apache httpd
# has to run after all txn's has been run
chown nginx /var/log/munin

%posttrans master-single
echo "" > %{_sysconfdir}/httpd/conf.d/munin-cgi.conf
echo "" > %{_sysconfdir}/httpd/conf.d/munin.conf

%post master
# default setup if fresh installation
if [ $1 = 1 ]; then
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  /bin/systemctl enable munin-fcgi-graph >/dev/null 2>&1 || :
  /bin/systemctl enable munin-fcgi-html >/dev/null 2>&1 || :
  /bin/systemctl start munin-fcgi-html >/dev/null 2>&1 || :
  /bin/systemctl start munin-fcgi-graph >/dev/null 2>&1 || :

  [ -r /etc/sysconfig/network-scripts/ifcfg-eth1 -a -r /etc/sysconfig/network ] || exit
  source /etc/sysconfig/network-scripts/ifcfg-eth1
  source /etc/sysconfig/network
  cluster=$(grep -E 'c[0-9X]+' /etc/motd | sed -r 's/.*(c[0-9X]+).*/\1/')
  NETWORK=$(ipcalc -sn ${IPADDR}/${PREFIX} | cut -d'=' -f2)/${PREFIX}
  cluster=${cluster:-"cXXX"}
  cat > /etc/munin/munin.conf <<EOC
# locations where munin find their files
dbdir  /var/lib/munin
htmldir /var/www/html/munin
logdir /var/log/munin
rundir  /var/run/munin

# generate graphs via CGI request
graph_strategy cgi

# gererate html via CGI request
html_strategy cgi 

# we want updates every 60 seconds
update_rate 60

# and we want to store this for
# avg of 60s for 14d
# avg of 5m  for 90d
# avg of 1h  for 180d
# avg of 1d  for 720d
graph_data_size custom 14d, 5m for 90d, 1h for 180d, 1d for 720d

# host definitions below
# i.e.
# [cXXX;node1]
#     address 192.168.X.Y
#     use_node_name yes

[${cluster};LB;maXXX1]
    address ${NETWORK%.*}.1
    use_node_name yes

[${cluster};LB;maXXX2]
    address ${NETWORK%.*}.2
    use_node_name yes

[${cluster};WEB;maXXX3]
    address ${NETWORK%.*}.3
    use_node_name yes

[${cluster};WEB;maXXX4]
    address ${NETWORK%.*}.4
    use_node_name yes

[${cluster};DB-NFS;maXXX5]
    address ${NETWORK%.*}.5
    use_node_name yes

[${cluster};DB-NFS;maXXX6]
    address ${NETWORK%.*}.6
    use_node_name yes
EOC
  test -f /etc/cron.d/munin && cat > /etc/cron.d/munin <<EOCRON
* * * * * munin test -x /usr/bin/munin-cron && /usr/bin/munin-cron
EOCRON
fi

%post node
# default setup if fresh installation
if [ $1 = 1 ]; then
  [ -r /etc/sysconfig/network-scripts/ifcfg-eth1 -a -r /etc/sysconfig/network ] || exit
  source /etc/sysconfig/network-scripts/ifcfg-eth1
  source /etc/sysconfig/network
  [ -n "${NETWORK}" -o -n "${PREFIX}" ] || exit

  cat > /etc/munin/munin-node.conf <<EOC
# log level, from 0 (err) to 4 (verbose)
log_level 1
log_file /var/log/munin-node/munin-node.log
pid_file /var/run/munin/munin-node.pid

# fork into background
background 1
setsid 1

# run under specified user/group
user munin
group munin

# ignore the following file regex's inside the confuration dirs
ignore_file [\#~]\$
ignore_file DEADJOE\$
ignore_file \.bak\$
ignore_file %\$
ignore_file \.dpkg-(tmp|new|old|dist)\$
ignore_file \.rpm(save|new)\$
ignore_file \.pod\$

# allow access to the client from the following addresses
allow ^127\.0\.0\.1\$
allow ^::1\$
cidr_allow 127.0.0.1/32
cidr_allow $(ipcalc -sn ${IPADDR}/${PREFIX} | cut -d'=' -f2)/${PREFIX}

# listen address
host ${IPADDR}

# express yourself 
host_name ${HOSTNAME}

# listening port
port 4949
EOC
fi

%post master-single
if [ $1 = 1 ]; then
  HOST=$(hostname -f)
  HOST_S=$(hostname -s)
  USER=$(getent passwd | egrep -e "c[0-9]{1,}\.psmanaged.com" -e "$HOST" | cut -d':' -f1)
  source %{_sysconfdir}/sysconfig/network-scripts/ifcfg-eth0

  cat <<EOF > /etc/munin/munin.conf
# locations where munin find their files
dbdir  /var/lib/munin
htmldir /var/www/html/munin
logdir /var/log/munin
rundir  /var/run/munin

# generate graphs via CGI request
graph_strategy cgi

# gererate html via CGI request
html_strategy cgi

# we want updates every 60 seconds
update_rate 60

# and we want to store this for
# avg of 60s for 14d
# avg of 5m  for 90d
# avg of 1h  for 180d
# avg of 1d  for 720d
graph_data_size custom 14d, 5m for 90d, 1h for 180d, 1d for 720d

# host definitions below
# i.e.

[$HOST_S]
     address 127.0.0.1
     use_node_name yes
EOF

  [ -f /etc/cron.d/munin ] && cat > /etc/cron.d/munin <<EOF
* * * * * munin test -x /usr/bin/munin-cron && /usr/bin/munin-cron
EOF

  if [ ! -z $USER ]; then 
    chown -R $USER:$USER /var/www/cgi-bin
    chown $USER /var/log/munin
  fi
fi

%post node-single
# default setup if fresh installation
if [ $1 = 1 ]; then
  source /etc/sysconfig/network
  cat > /etc/munin/munin-node.conf <<EOF
# log level, from 0 (err) to 4 (verbose)
log_level 1
log_file /var/log/munin-node/munin-node.log
pid_file /var/run/munin/munin-node.pid

# fork into background
background 1
setsid 1

# run under specified user/group
user munin
group munin

# ignore the following file regex's inside the confuration dirs
ignore_file [\#~]\$
ignore_file DEADJOE\$
ignore_file \.bak\$
ignore_file %\$
ignore_file \.dpkg-(tmp|new|old|dist)\$
ignore_file \.rpm(save|new)\$
ignore_file \.pod\$

# allow access to the client from the following addresses
allow ^127\.0\.0\.1\$
allow ^::1\$
cidr_allow 127.0.0.1/32

# listen address
host 127.0.0.1

# express yourself 
host_name ${HOSTNAME}

# listening port
port 4949
EOF
fi

%files master
%defattr(-,root,root,-)

%files master-single
%defattr(-, root, root, -)
%config %{_sysconfdir}/httpd/conf/munin-apache.conf

%files node
%defattr(-,root,root,-)
/root/servermanagement/munin-plugins.pl

%files node-single
%defattr(-,root,root,-)
/root/servermanagement/munin-plugins.pl

%files solr
%defattr(-,root,root,-)
%{pk_plugin_dir}/solr4_.*

%files redis
%defattr(-,root,root,-)
%{pk_plugin_dir}/redis_

%files mongodb
%defattr(-,root,root,-)
%{pk_plugin_dir}/mongo_*

%files varnish4
%defattr(-,root,root,-)
%{pk_plugin_dir}/varnish4_

%changelog