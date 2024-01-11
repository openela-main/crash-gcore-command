#
# crash core analysis suite
#
%global reponame crash-gcore
Summary: Gcore extension module for the crash utility
Name: crash-gcore-command
Version: 1.6.3
Release: 3%{?dist}
License: GPLv2
Group: Development/Debuggers
Source: https://github.com/fujitsu/crash-gcore/archive/v%{version}/%{name}-%{version}.tar.gz
URL: https://github.com/fujitsu/crash-gcore
# Vendor: FUJITSU LIMITED
# Packager: HATAYAMA Daisuke <d.hatayama@jp.fujitsu.com>
ExclusiveOS: Linux
ExclusiveArch: x86_64 %{ix86} arm aarch64 ppc64 ppc64le
Buildroot: %{_tmppath}/%{name}-root
BuildRequires: crash-devel >= 5.1.5, zlib-devel lzo-devel snappy-devel
Requires: crash >= 5.1.5
Patch0: 0001-coredump-use-MEMBER_-OFFSET-SIZE-instead-of-GCORE_-O.patch
Patch1: 0002-gcore-defs-remove-definitions-and-initializations-fo.patch
Patch2: 0003-gcore-fix-memory-allocation-failure-during-processin.patch
Patch3: 0001-x86-Fix-failure-of-collecting-vsyscall-mapping-due-t.patch
Patch4: 0002-coredump-fix-segmentation-fault-caused-by-type-misma.patch
Patch5: 0003-elf-fix-warning-message-caused-by-type-mismatch-of-o.patch
Patch6: 0004-coredump-fix-unexpected-truncation-of-generated-core.patch
Patch7: 0005-gcore.mk-fix-mismatch-of-_FILE_OFFSET_BITS-when-buil.patch

%description
Command for creating a core dump file of a user-space task that was
running in a kernel dumpfile.

%prep
%setup -q -n %{reponame}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
make CFLAGS="%{optflags} -Wl,-z,now" -C src -f gcore.mk

%install
rm -Rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_libdir}/crash/extensions/
cp %{_builddir}/%{reponame}-%{version}/src/gcore.so %{buildroot}%{_libdir}/crash/extensions/

%clean
rm -rf %{buildroot}
rm -Rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/crash/extensions/gcore.so
%doc COPYING

%changelog
* Fri Nov 18 2022 Lianbo Jiang <lijiang@redhat.com> - 1.6.3-3
- Update to upstream commit d2795659986d
- Resolves: rhbz#2119697

* Tue Apr 12 2022 Tao Liu <ltao@redhat.com> - 1.6.3-2
- Rebase to upstream crash-gcore-command-1.6.3
- Fix memory allocation failure issue
- Resolves: rhbz#2060355

* Wed Dec 2 2020 Bhupesh Sharma <bhsharma@redhat.com> - 1.6.0-1
- Rebase crash-gcore-command to github upstream version crash-gcore-command-1.6.0
  Resolves: rhbz#1903465

* Wed Jul 8 2020 Bhupesh Sharma <bhsharma@redhat.com> - 1.5.1-1
- Rebase crash-gcore-command to github upstream version crash-gcore-command-1.5.1
  Resolves: rhbz#1851747

* Tue Jun 25 2019 Dave Anderson <anderson@redhat.com> - 1.3.1-4
- Fix "invalid structure size: pid_link"
  Resolves: rhbz#1722726

* Tue Dec  4 2018 Dave Anderson <anderson@redhat.com> - 1.3.1-3
- Fix x86_64 "invalid structure member offset: thread_struct_fs"
  Resolves: rhbz#1589019
- Fix arm64 "invalid structure member offset: thread_struct_fpsimd_state"
  Resolves: rhbz#1625810

* Wed Sep 10 2018 Dave Anderson <anderson@redhat.com> - 1.3.1-2
- Address annocheck link issue
  Resolves: rhbz#1630556

* Mon Aug 13 2018 Dave Anderson <anderson@redhat.com> - 1.3.1-1
- Bump release for mass rebuild
  Resolves: rhbz#1615509

* Thu Nov 6 2014 Dave Anderson <anderson@redhat.com> - 1.3.1-0
- Rebase to 1.3.1 to address 32-bit x86 build error.
- Resolves: rhbz#1077311

* Tue Nov 4 2014 Dave Anderson <anderson@redhat.com> - 1.3.0-0
- Add aarch64 support
- Resolves: rhbz#1077311
- Add ppc64/ppc64le support
- Resolves: rhbz#1125485

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.2.1-2
- Mass rebuild 2013-12-27


* Tue Aug 20 2013 Dave Anderson <anderson@redhat.com> - 1.2.1-1
  crash utility has added LZO and snappy compression in addition to zlib.

* Thu May 23 2013 HATAYAMA Daisuke <d.hatayama@jp.fujitsu.com> - 1.2.1-0
  Fixes for missing VDSO and vsyscall pages in core dump.

* Wed Nov 21 2012 HATAYAMA Daisuke <d.hatayama@jp.fujitsu.com> - 1.2-0
  Support recent kernels around 3.6.

* Tue Jan 31 2012 Dave Anderson <anderson@redhat.com> - 1.0-3
  Address Pkgwrangler/rpmlint issues.
  Resolves: rbhz#692799

* Wed Jan 25 2012 Dave Anderson <anderson@redhat.com> - 1.0-2
  Compile with RPM_OPT_FLAGS and fix warnings generated from using it. 
  Resolves: rbhz#692799

* Thu Apr 13 2011 HATAYAMA Daisuke <d.hatayama@jp.fujitsu.com> - 1.0-1
- Remove inclusion of kvmdump.h and unwind_x86_64.h due to non-supporting issue
  on crash-devel package. Instead, use a new interface for them.
- Remove ppc64, ia64, s390 and s390x from ExclusiveArch, leave x86_64
  and %%{ix86} there.
- Add descriptions in BuildRequires and Requires about crash and crash-devel.

* Wed Apr 6 2011 HATAYAMA Daisuke <d.hatayama@jp.fujitsu.com> - 1.0-0
- Initial crash-gcore-command package

