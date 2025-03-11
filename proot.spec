%ifarch %{x8664}
%define		with_32bit_loader	1
%endif

Summary:	chroot, mount --bind, and binfmt_misc without privilege/setup for Linux
Name:		proot
Version:	5.4.0
Release:	3
License:	GPL v2+
Group:		Applications/System
Source0:	https://github.com/proot-me/proot/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9b6e3e6e0e2c3bf4c2e1c450bf76e715
Patch0:		flags.patch
URL:		https://proot-me.github.io/
BuildRequires:	docutils
BuildRequires:	libarchive-devel
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.8
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	swig
BuildRequires:	swig-python
BuildRequires:	talloc-devel
BuildRequires:	uthash-devel
ExclusiveArch:	%{arm} %{ix86} %{x8664} aarch64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PRoot is a user-space implementation of chroot, mount --bind, and
binfmt_misc. This means that users don't need any privileges or setup
to do things like using an arbitrary directory as the new root
filesystem, making files accessible somewhere else in the filesystem
hierarchy, or executing programs built for another CPU architecture
transparently through QEMU user-mode.

%prep
%setup -q
%patch -P 0 -p1

%build
export CPPFLAGS="%{rpmcppflags}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"
%{__make} -C src loader.elf%{?with_32bit_loader: loader-m32.elf} build.h care proot \
	CC="%{__cc}" \
	V=1

%{__make} -C doc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} -C src install install-care \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR="%{_bindir}" \
	V=1

cp -p doc/proot/man.1 $RPM_BUILD_ROOT%{_mandir}/man1/proot.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.rst HACKING.rst README.rst
%attr(755,root,root) %{_bindir}/care
%attr(755,root,root) %{_bindir}/proot
%{_mandir}/man1/proot.1*
