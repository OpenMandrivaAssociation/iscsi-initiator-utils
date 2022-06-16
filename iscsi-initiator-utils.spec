%global optflags %{optflags} -Wno-error=unused-command-line-argument
%global commit0			20d0aa96f2170339b1967f4be81e9c5042bbce03
%global shortcommit0		%(c=%{commit0}; echo ${c:0:7})
%global _disable_ld_no_undefined 1

# Disable python2 build by default
%bcond_with python2

Summary: iSCSI daemon and utility programs
Name: iscsi-initiator-utils
Version: 2.1.5
Release: 1
License: GPLv2+
URL: https://github.com/open-iscsi/open-iscsi
Source0: https://github.com/open-iscsi/open-iscsi/archive/%{commit0}.tar.gz#/open-iscsi-%{shortcommit0}.tar.gz
Source4: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/04-iscsi
Source5: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/iscsi-tmpfiles.conf

Patch0001: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0001-unit-file-tweaks.patch
Patch0002: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0002-idmb_rec_write-check-for-tpgt-first.patch
Patch0003: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0003-idbm_rec_write-seperate-old-and-new-style-writes.patch
Patch0004: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0004-idbw_rec_write-pick-tpgt-from-existing-record.patch
Patch0005: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0005-update-initscripts-and-docs.patch
Patch0006: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0006-use-var-for-config.patch
# We disagree with this. We're open-iscsi, not RH
#Patch0007: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0007-use-red-hat-for-name.patch
Patch0008: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0008-libiscsi.patch
Patch0009: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0009-Add-macros-to-release-GIL-lock.patch
Patch0010: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0010-libiscsi-introduce-sessions-API.patch
Patch0011: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0011-libiscsi-fix-discovery-request-timeout-regression.patch
Patch0012: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0012-libiscsi-format-security-build-errors.patch
Patch0013: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0013-libiscsi-fix-build-to-use-libopeniscsiusr.patch
Patch0014: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0014-libiscsi-fix-build-against-latest-upstream-again.patch
Patch0015: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0015-remove-the-offload-boot-supported-ifdef.patch
Patch0016: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0016-Revert-iscsiadm-return-error-when-login-fails.patch
Patch0017: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0017-dont-install-scripts.patch
Patch0018: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0018-use-var-lib-iscsi-in-libopeniscsiusr.patch
Patch0019: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0019-Coverity-scan-fixes.patch
Patch0020: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0020-fix-upstream-build-breakage-of-iscsiuio-LDFLAGS.patch
# We disagree with this... Why change the version number?
# Incorrectly versioning the package is a dumb idea too.
#Patch0021: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0021-use-Red-Hat-version-string-to-match-RPM-package-vers.patch
Patch0022: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0022-iscsi_if.h-replace-zero-length-array-with-flexible-a.patch
Patch0023: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0023-stop-using-Werror-for-now.patch
Patch0024: https://src.fedoraproject.org/rpms/iscsi-initiator-utils/raw/rawhide/f/0024-minor-service-file-updates.patch

Patch1000: open-iscsi-compile.patch

BuildRequires: flex bison doxygen kmod-devel systemd-units
BuildRequires: autoconf automake libtool libmount-devel
BuildRequires: pkgconfig(openssl)
BuildRequires: %mklibname -d isns
BuildRequires: pkgconfig(libsystemd)
Requires: %{name}-iscsiuio >= %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

# Old NetworkManager expects the dispatcher scripts in a different place
Conflicts: NetworkManager < 1.20

%global _hardened_build 1
%global __provides_exclude_from ^(%{python2_sitearch}/.*\\.so|%{python3_sitearch}/.*\\.so)$

%description
The iscsi package provides the server daemon for the iSCSI protocol,
as well as the utility programs used to manage it. iSCSI is a protocol
for distributed disk access using SCSI commands sent over Internet
Protocol networks.

%package iscsiuio
Summary: Userspace configuration daemon required for some iSCSI hardware
License: BSD
Requires: %{name} = %{version}-%{release}

%description iscsiuio
The iscsiuio configuration daemon provides network configuration help
for some iSCSI offload hardware.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if %{with python2}
%package -n python2-%{name}
%{?python_provide:%python_provide python2-%{name}}
Summary: Python %{python2_version} bindings to %{name}
Requires: %{name} = %{version}-%{release}
BuildRequires: python2-devel
BuildRequires: python2-setuptools

%description -n python2-%{name}
The %{name}-python2 package contains Python %{python2_version} bindings to the
libiscsi interface for interacting with %{name}
%endif
# ended with python2

%package -n python-%{name}
%{?python_provide:%python_provide python-%{name}}
Summary: Python %{python3_version} bindings to %{name}
Requires: %{name} = %{version}-%{release}
BuildRequires: python-devel
BuildRequires: python-setuptools
BuildRequires: make

%description -n python-%{name}
The python-%{name} package contains Python %{python3_version} bindings to the
libiscsi interface for interacting with %{name}

%prep
%autosetup -p1 -n open-iscsi-%{commit0}

# change exec_prefix, there's no easy way to override
%{__sed} -i -e 's|^exec_prefix = /$|exec_prefix = %{_exec_prefix}|' Makefile

%build
# avoid undefined references linking failures
%undefine _ld_as_needed

# configure sub-packages from here
# letting the top level Makefile do it will lose setting from rpm
cd iscsiuio
autoreconf --install
%{configure}
cd ..

%{__make} OPTFLAGS="%{optflags}"
pushd libiscsi
%if %{with python2}
%py2_build
%endif
# ended with python2
%py3_build
popd


%install
%{__make} DESTDIR=%{?buildroot} install_programs install_doc install_etc install_libopeniscsiusr
# upstream makefile doesn't get everything the way we like it
#rm $RPM_BUILD_ROOT%%{_sbindir}/iscsi_discovery
rm $RPM_BUILD_ROOT%{_mandir}/man8/iscsi_discovery.8
rm $RPM_BUILD_ROOT%{_mandir}/man8/iscsi_fw_login.8
%{__install} -pm 755 usr/iscsistart $RPM_BUILD_ROOT%{_sbindir}
%{__install} -pm 644 doc/iscsistart.8 $RPM_BUILD_ROOT%{_mandir}/man8
%{__install} -pm 644 doc/iscsi-iname.8 $RPM_BUILD_ROOT%{_mandir}/man8
%{__install} -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -pm 644 iscsiuio/iscsiuiolog $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d

%{__install} -d $RPM_BUILD_ROOT%{_sharedstatedir}/iscsi
%{__install} -d $RPM_BUILD_ROOT%{_sharedstatedir}/iscsi/nodes
%{__install} -d $RPM_BUILD_ROOT%{_sharedstatedir}/iscsi/send_targets
%{__install} -d $RPM_BUILD_ROOT%{_sharedstatedir}/iscsi/static
%{__install} -d $RPM_BUILD_ROOT%{_sharedstatedir}/iscsi/isns
%{__install} -d $RPM_BUILD_ROOT%{_sharedstatedir}/iscsi/slp
%{__install} -d $RPM_BUILD_ROOT%{_sharedstatedir}/iscsi/ifaces

# for %%ghost
%{__install} -d $RPM_BUILD_ROOT%{_rundir}/lock/iscsi
touch $RPM_BUILD_ROOT%{_rundir}/lock/iscsi/lock


%{__install} -d $RPM_BUILD_ROOT%{_unitdir}
%{__install} -pm 644 etc/systemd/iscsi.service $RPM_BUILD_ROOT%{_unitdir}
%{__install} -pm 644 etc/systemd/iscsi-init.service $RPM_BUILD_ROOT%{_unitdir}
%{__install} -pm 644 etc/systemd/iscsi-onboot.service $RPM_BUILD_ROOT%{_unitdir}
%{__install} -pm 644 etc/systemd/iscsi-shutdown.service $RPM_BUILD_ROOT%{_unitdir}
%{__install} -pm 644 etc/systemd/iscsid.service $RPM_BUILD_ROOT%{_unitdir}
%{__install} -pm 644 etc/systemd/iscsid.socket $RPM_BUILD_ROOT%{_unitdir}
%{__install} -pm 644 etc/systemd/iscsiuio.service $RPM_BUILD_ROOT%{_unitdir}
%{__install} -pm 644 etc/systemd/iscsiuio.socket $RPM_BUILD_ROOT%{_unitdir}

%{__install} -d $RPM_BUILD_ROOT%{_libexecdir}
%{__install} -pm 755 etc/systemd/iscsi-mark-root-nodes $RPM_BUILD_ROOT%{_libexecdir}

%{__install} -d $RPM_BUILD_ROOT%{_prefix}/lib/NetworkManager/dispatcher.d
%{__install} -pm 755 %{SOURCE4} $RPM_BUILD_ROOT%{_prefix}/lib/NetworkManager/dispatcher.d

%{__install} -d $RPM_BUILD_ROOT%{_tmpfilesdir}
%{__install} -pm 644 %{SOURCE5} $RPM_BUILD_ROOT%{_tmpfilesdir}/iscsi.conf

%{__install} -d $RPM_BUILD_ROOT%{_libdir}
%{__install} -pm 755 libiscsi/libiscsi.so.0 $RPM_BUILD_ROOT%{_libdir}
%{__ln_s}    libiscsi.so.0 $RPM_BUILD_ROOT%{_libdir}/libiscsi.so
%{__install} -d $RPM_BUILD_ROOT%{_includedir}
%{__install} -pm 644 libiscsi/libiscsi.h $RPM_BUILD_ROOT%{_includedir}

%if %{with python2}
%{__install} -d $RPM_BUILD_ROOT%{python2_sitearch}
%endif
# ended with python2
%{__install} -d $RPM_BUILD_ROOT%{python3_sitearch}
pushd libiscsi
%if %{with python2}
%py2_install
%endif
# ended with python2
%py3_install
popd


%post
%systemd_post iscsi.service iscsid.service iscsid.socket iscsi-onboot.service iscsi-init.service iscsi-shutdown.service

%preun
%systemd_preun iscsi.service iscsid.service iscsid.socket iscsi-onboot.service iscsi-init.service iscsi-shutdown.service

%postun
%systemd_postun iscsi.service iscsid.service iscsid.socket iscsi-onboot.service iscsi-init.service iscsi-shutdown.service

%post iscsiuio
%systemd_post iscsiuio.service iscsiuio.socket

%preun iscsiuio
%systemd_preun iscsiuio.service iscsiuio.socket

%postun iscsiuio
%systemd_postun iscsiuio.service iscsiuio.socket

%triggerun -- iscsi-initiator-utils < 6.2.0.873-25
# prior to 6.2.0.873-24 iscsi.service was missing a Wants=remote-fs-pre.target
# this forces remote-fs-pre.target active if needed for a clean shutdown/reboot
# after upgrading this package
if [ $1 -gt 0 ]; then
    /usr/bin/systemctl -q is-active iscsi.service
    if [ $? -eq 0 ]; then
        /usr/bin/systemctl -q is-active remote-fs-pre.target
        if [ $? -ne 0 ]; then
            SRC=`/usr/bin/systemctl show --property FragmentPath remote-fs-pre.target | cut -d= -f2`
            DST=/run/systemd/system/remote-fs-pre.target
            if [ $SRC != $DST ]; then
                cp $SRC $DST
            fi
            sed -i 's/RefuseManualStart=yes/RefuseManualStart=no/' $DST
            /usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
            /usr/bin/systemctl start remote-fs-pre.target >/dev/null 2>&1 || :
        fi
    fi
fi
# added in 6.2.0.873-25
if [ $1 -gt 0 ]; then
    systemctl start iscsi-shutdown.service >/dev/null 2>&1 || :
fi


%files
%doc README
%dir %{_sharedstatedir}/iscsi
%dir %{_sharedstatedir}/iscsi/nodes
%dir %{_sharedstatedir}/iscsi/isns
%dir %{_sharedstatedir}/iscsi/static
%dir %{_sharedstatedir}/iscsi/slp
%dir %{_sharedstatedir}/iscsi/ifaces
%dir %{_sharedstatedir}/iscsi/send_targets
%ghost %attr(0700, root, root) %dir %{_rundir}/lock/iscsi
%ghost %attr(0600, root, root) %{_rundir}/lock/iscsi/lock
%{_unitdir}/iscsi.service
%{_unitdir}/iscsi-onboot.service
%{_unitdir}/iscsi-init.service
%{_unitdir}/iscsi-shutdown.service
%{_unitdir}/iscsid.service
%{_unitdir}/iscsid.socket
%{_libexecdir}/iscsi-mark-root-nodes
%{_prefix}/lib/NetworkManager/dispatcher.d/04-iscsi
%{_tmpfilesdir}/iscsi.conf
%dir %{_sysconfdir}/iscsi
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/iscsi/iscsid.conf
%{_sbindir}/iscsi-iname
%{_sbindir}/iscsiadm
%{_sbindir}/iscsid
%{_sbindir}/iscsistart
%{_libdir}/libiscsi.so.0
%{_mandir}/man8/iscsi-iname.8*
%{_mandir}/man8/iscsiadm.8*
%{_mandir}/man8/iscsid.8*
%{_mandir}/man8/iscsistart.8*
%{_libdir}/libopeniscsiusr.so.*

%files iscsiuio
%{_sbindir}/iscsiuio
%{_unitdir}/iscsiuio.service
%{_unitdir}/iscsiuio.socket
%config(noreplace) %{_sysconfdir}/logrotate.d/iscsiuiolog
%{_mandir}/man8/iscsiuio.8*

%files devel
%doc libiscsi/html
%{_libdir}/libiscsi.so
%{_includedir}/libiscsi.h
%{_libdir}/libopeniscsiusr.so
%{_includedir}/libopeniscsiusr.h
%{_includedir}/libopeniscsiusr_common.h
%{_includedir}/libopeniscsiusr_iface.h
%{_includedir}/libopeniscsiusr_node.h
%{_includedir}/libopeniscsiusr_session.h
%{_libdir}/pkgconfig/libopeniscsiusr.pc

%if %{with python2}
%files -n python2-%{name}
%{python2_sitearch}/*
%endif
# ended with python2

%files -n python-%{name}
%{python3_sitearch}/*
