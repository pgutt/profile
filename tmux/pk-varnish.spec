
# SRCDIR pk-varnish

%define realname varnish

Summary:	High-performance HTTP accelerator
Name:		pk-%{realname}
Version:	3.0.7
Release:	2%{dist}.CS
License:	BSD
Group:		CS/Webserver
URL:		http://www.varnish-cache.org/
Source0:	http://repo.varnish-cache.org/source/varnish-%{version}.tar.gz
Source1:	xxxxx-varnishncsa-logrotate
Source2:	varnishncsa.sysconfig
Patch0:		varnish-xxxxx.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	ncurses-devel libxslt groff pcre-devel pkgconfig readline-devel
Requires:	%{name}-libs = %{version}-%{release} pk-varnish-libvmod-ipcast
Requires:	logrotate ncurses pcre gcc readline
Prefix:		/usr/local/software

%description
This is Varnish Cache, a high-performance HTTP accelerator.
Documentation wiki and additional information about Varnish is
available on the following web site: http://www.varnish-cache.org/

%package libs
Summary: Libraries for %{realname}
Group: CS/Bibliotheken

%description libs
Libraries for varnish. Varnish Cache is a high-performance HTTP accelerator

%package libs-devel
Summary: Development files for varnish-libs
Group: CS/Bibliotheken
Requires: varnish-libs = %{version}-%{release}

%description libs-devel
Development files for varnish-libs. Varnish Cache is a high-performance HTTP accelerator

%package docs
Summary: Documentation files for varnish
Group: CS/Bibliotheken

%description docs
Documentation files for varnish

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1

mkdir examples
cp bin/varnishd/default.vcl etc/zope-plone.vcl examples

%build
./configure \
	--prefix=%{prefix} \
	--libdir=%{prefix}%{_libdir} \
	--bindir=%{prefix}%{_bindir} \
	--sbindir=%{prefix}%{_sbindir} \
	--mandir=%{prefix}%{_mandir} \
	--localstatedir=%{_localstatedir}/lib \
	--includedir=%{prefix}%{_includedir} \
	--sysconfdir=%{prefix}%{_sysconfdir}

%{__make} %{?_smp_mflags}

head -6 etc/default.vcl > redhat/default.vcl

cat << EOF >> redhat/default.vcl
backend default {
  .host = "127.0.0.1";
  .port = "80";
}
EOF

tail -n +11 etc/default.vcl >> redhat/default.vcl

%if 0%{?fedora}%{?rhel} != 0 && 0%{?rhel} <= 4 && 0%{?fedora} <= 8
	# Old style daemon function
	sed -i 's,--pidfile \$pidfile,,g;
		s,status -p \$pidfile,status,g;
		s,killproc -p \$pidfile,killproc,g' \
	redhat/varnish.initrc redhat/varnishlog.initrc redhat/varnishncsa.initrc
%endif

cp -r doc/sphinx/\=build/html doc

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"

# None of these for fedora
find %{buildroot}/%{prefix}%{_libdir}/ -name '*.la' -exec rm -f {} ';'

# Remove this line to build a devel package with symlinks
#find %{buildroot}/%{_libdir}/ -name '*.so' -type l -exec rm -f {} ';'

mkdir -p %{buildroot}/var/lib/varnish
mkdir -p %{buildroot}/var/log/varnish
mkdir -p %{buildroot}/var/run/varnish

%{__install} -D -m 0644 redhat/default.vcl %{buildroot}%{prefix}%{_sysconfdir}/varnish/default.vcl
%{__install} -D -m 0644 redhat/varnish.sysconfig %{buildroot}%{prefix}%{_sysconfdir}/sysconfig/varnish
%{__install} -D -m 0644 %{S:2} %{buildroot}%{prefix}%{_sysconfdir}/sysconfig/varnishncsa
%{__install} -D -m 0755 redhat/varnish.initrc %{buildroot}%{_initrddir}/pk-varnish
%{__install} -D -m 0755 redhat/varnishlog.initrc %{buildroot}%{_initrddir}/pk-varnishlog
%{__install} -D -m 0755 redhat/varnishncsa.initrc %{buildroot}%{_initrddir}/pk-varnishncsa
%{__install} -D -m 0755 redhat/varnish_reload_vcl %{buildroot}%{prefix}%{_bindir}/varnish_reload_vcl
%{__install} -D -m 0644 %{S:1} %{buildroot}%{prefix}%{_sysconfdir}/varnish/varnishncsa_logrotate

# TE-6962
%if 0%{?el6}
    %{__sed} -i -r -e 's#/var/run/varnishncsa.pid#/var/run/varnish/varnishncsa.pid#' \
                   %{buildroot}%{prefix}%{_sysconfdir}/varnish/varnishncsa_logrotate
%endif

%pre
if [ "$1" = "1" ]; then
  getent group varnish >/dev/null || groupadd -r varnish
  getent passwd varnish >/dev/null || \
	useradd -r -g varnish -d /var/lib/varnish -s /sbin/nologin \
		-c "Varnish Cache" varnish
  exit 0
fi

%post
if [ "$1" = "1" ]; then
  /sbin/chkconfig --add pk-varnish
  /sbin/chkconfig --add pk-varnishlog
  /sbin/chkconfig --add pk-varnishncsa 
  test -f %{prefix}/etc/varnish/secret || (uuidgen > %{prefix}/etc/varnish/secret && chmod 0604 %{prefix}/etc/varnish/secret)
fi

%preun
if [ "$1" = "0" ]; then
  /sbin/service pk-varnish stop > /dev/null 2>&1
  /sbin/service pk-varnishlog stop > /dev/null 2>&1
  /sbin/service pk-varnishncsa stop > /dev/null 2>&1
  /sbin/chkconfig --del pk-varnish
  /sbin/chkconfig --del pk-varnishlog
  /sbin/chkconfig --del pk-varnishncsa 
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{prefix}%{_sbindir}/*
%{prefix}%{_bindir}/*
%{prefix}%{_libdir}/varnish
%dir %{_var}/lib/varnish
%dir %{_var}/log/varnish
%dir %{_var}/run/varnish
%{prefix}%{_mandir}/man1/*.1*
%{prefix}%{_mandir}/man3/*.3*
%{prefix}%{_mandir}/man7/*.7*

%doc INSTALL LICENSE README redhat/README.redhat ChangeLog
%doc examples
%dir %{prefix}%{_sysconfdir}/varnish/
%config(noreplace) %{prefix}%{_sysconfdir}/varnish/default.vcl
%config(noreplace) %{prefix}%{_sysconfdir}/sysconfig/varnish
%config(noreplace) %{prefix}%{_sysconfdir}/sysconfig/varnishncsa
%config(noreplace) %{prefix}%{_sysconfdir}/varnish/varnishncsa_logrotate

%{_initrddir}/pk-varnish
%{_initrddir}/pk-varnishlog
%{_initrddir}/pk-varnishncsa

%files libs
%defattr(-,root,root,-)
%{prefix}%{_libdir}/*.so.*
%doc LICENSE

%files libs-devel
%defattr(-,root,root,-)
%{prefix}%{_libdir}/lib*.so
%{prefix}%{_libdir}/lib*.a
%dir %{prefix}%{_includedir}/varnish
%{prefix}%{_includedir}/varnish/*
%{prefix}%{_libdir}/pkgconfig/varnishapi.pc
%doc LICENSE

%files docs
%defattr(-,root,root,-)
%doc LICENSE
%doc doc/sphinx
%doc doc/html
%doc doc/changes*.html


%changelog