%global reponame crash-gcore

Summary: Gcore extension module for the crash utility
Name: crash-gcore-command
Version: 1.6.4
Release: 1%{?dist}
License: GPLv2
Source0: https://github.com/fujitsu/crash-gcore/archive/v%{version}/%{name}-%{version}.tar.gz
URL: https://github.com/fujitsu/crash-gcore
ExclusiveOS: Linux
ExclusiveArch: aarch64 ppc64le x86_64
BuildRequires: crash-devel >= 5.1.5
BuildRequires: gcc
Requires: crash >= 5.1.5

Patch0: 0001-coredump-fix-building-failure-due-to-undefined-macro.patch
Patch1: 0002-x86-fix-extend-gcore.so-taking-much-time-like-more-t.patch

%description
Command for creating a core dump file of a user-space task that was
running in a kernel dump file.

%prep
%autosetup -n %{reponame}-%{version} -p1

%build
%make_build CFLAGS="%{optflags} -Wl,-z,now" -C src -f gcore.mk

%install
install -m 0755 -d %{buildroot}%{_libdir}/crash/extensions
install -m 0755 -t %{buildroot}%{_libdir}/crash/extensions %{_builddir}/%{reponame}-%{version}/src/gcore.so

%files
%dir %{_libdir}/crash
%dir %{_libdir}/crash/extensions
%{_libdir}/crash/extensions/gcore.so
%license COPYING

%changelog
* Fri Jul 05 2024 Lianbo Jiang <lijiang@redhat.com> - 1.6.4-1
- Rebase to upstream 1.6.4

* Fri Nov 18 2022 Lianbo Jiang <lijiang@redhat.com> - 1.6.3-2
- Update to the latest commit d2795659986d

* Mon Dec 27 2021 Lianbo Jiang <lijiang@redhat.com> - 1.6.3-1
- Rebase to upstream 1.6.3

* Wed Dec 15 2021 Lianbo Jiang <lijiang@redhat.com> - 1.6.2-5
- Rebuild for the compatibility issue

* Tue Dec 07 2021 Lianbo Jiang <lijiang@redhat.com> - 1.6.2-4
- Fix the hardening issue "FAIL: bind-now test because not linked with -Wl,-z,now"

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.6.2-3
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 1.6.2-2
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Fri Jan 22 2021 HATAYAMA Daisuke <d.hatayama@fujitsu.com> - 1.6.2-1
- Initial crash-gcore-command package
