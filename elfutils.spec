# libelf is used by glib2.0, which in turn is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif
%define major 1

#the old name was _libelfutils1
%define libname %mklibname %{name} %{major}
%define libasm %mklibname asm %{major}
%define libdw %mklibname dw %{major}
%define libelf %mklibname elf %{major}
%define libdebuginfod %mklibname debuginfod %{major}
%define devname %mklibname %{name} -d
%define static %mklibname %{name} -d -s
%define lib32asm libasm%{major}
%define lib32dw libdw%{major}
%define lib32elf libelf%{major}
%define dev32name lib%{name}-devel
%define static32 lib%{name}-static-devel

%define _program_prefix eu-
%global __provides_exclude ^libebl_.*\\.so.*$

# This package uses top level ASM constructs which are incompatible with LTO.
# Top level ASMs are often used to implement symbol versioning.  gcc-10
# introduces a new mechanism for symbol versioning which works with LTO.
# Converting packages to use that mechanism instead of toplevel ASMs is
# recommended.
# Disable LTO
%define _disable_lto 1

%global optflags %{optflags} -Os -fstack-protector-strong -Wno-error -fexceptions

Summary:	A collection of utilities and DSOs to handle compiled objects
Name:		elfutils
Version:	0.185
Release:	1
License:	GPLv2+
Group:		Development/Other
Url:		https://sourceware.org/elfutils/
Source0:	https://sourceware.org/elfutils/ftp/%{version}/%{name}-%{version}.tar.bz2
Patch100:	elfutils.git-c6e1f664254a8ae16e2e6d726c5159ecb7f27d3b.patch

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libmicrohttpd)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(libarchive)
Obsoletes:	%{libname} < 0.155
%if %{with compat32}
BuildRequires:	gcc
BuildRequires:	devel(libz)
BuildRequires:	devel(liblzma)
BuildRequires:	devel(libbz2)
%endif

%description
Elfutils is a collection of utilities, including stack (to show
backtraces), nm (for listing symbols from object files), size
(for listing the section sizes of an object or archive file),
strip (for discarding symbols), readelf (to see the raw ELF file
structures), and elflint (to check for well-formed ELF files).

%package -n %{libasm}
Summary:	Libraries to read and write ELF files
Group:		System/Libraries
Obsoletes:	%{libname} < 0.155

%description -n %{libasm}
Included are the helper library which implement machine-specific ELF handling.

%package -n %{libdw}
Summary:	Libraries to read and write ELF files
Group:		System/Libraries
Obsoletes:	%{libname} < 0.155

%description -n %{libdw}
Included are the helper library which implement DWARF ELF handling.

%package -n %{libelf}
Summary:	Libraries to read and write ELF files
Group:		System/Libraries
Obsoletes:	%{libname} < 0.155
Provides:	%{libname} = %{EVRD}
Requires:	%{libdw} = %{EVRD}
Requires:	%{libasm} = %{EVRD}

%description -n %{libelf}
This package provides DSOs which allow reading and writing ELF files
on a high level.  Third party programs depend on this package to read
internals of ELF files.  The programs of the elfutils package use it
also to generate new ELF files.

%package -n %{libdebuginfod}
Summary:	Libraries to talk to debuginfod servers
Group:		System/Libraries

%description -n %{libdebuginfod}
Libraries to talk to debuginfod servers

%package -n debuginfod
Summary:	Debuginfo server
Group:		Development/Other

%description -n debuginfod
Debuginfo server

%package -n %{devname}
Summary:	Development libraries to handle compiled objects
Group:		Development/Other
Requires:	%{libasm} = %{EVRD}
Requires:	%{libdw} = %{EVRD}
Requires:	%{libelf} = %{EVRD}
Provides:	%{name}-devel

%description -n %{devname}
This package contains the headers and dynamic libraries to create
applications for handling compiled objects.

   * libelf allows you to access the internals of the ELF object file
     format, so you can see the different sections of an ELF file.
   * libebl provides some higher-level ELF access functionality.
   * libasm provides a programmable assembler interface.

%package -n %{static}
Summary:	Static libraries for development with libelfutils
Group:		Development/Other
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel

%description -n %{static}
This package contains the static libraries to create applications for
handling compiled objects.

%if %{with compat32}
%package -n %{lib32asm}
Summary:	Libraries to read and write ELF files (32-bit)
Group:		System/Libraries

%description -n %{lib32asm}
Included are the helper library which implement machine-specific ELF handling.

%package -n %{lib32dw}
Summary:	Libraries to read and write ELF files (32-bit)
Group:		System/Libraries

%description -n %{lib32dw}
Included are the helper library which implement DWARF ELF handling.

%package -n %{lib32elf}
Summary:	Libraries to read and write ELF files (32-bit)
Group:		System/Libraries
Requires:	%{lib32dw} = %{EVRD}
Requires:	%{lib32asm} = %{EVRD}

%description -n %{lib32elf}
This package provides DSOs which allow reading and writing ELF files
on a high level.  Third party programs depend on this package to read
internals of ELF files.  The programs of the elfutils package use it
also to generate new ELF files.

%package -n %{dev32name}
Summary:	Development libraries to handle compiled objects (32-bit)
Group:		Development/Other
Requires:	%{lib32asm} = %{EVRD}
Requires:	%{lib32dw} = %{EVRD}
Requires:	%{lib32elf} = %{EVRD}
Requires:	%{devname} = %{EVRD}

%description -n %{dev32name}
This package contains the headers and dynamic libraries to create
applications for handling compiled objects.

   * libelf allows you to access the internals of the ELF object file
     format, so you can see the different sections of an ELF file.
   * libebl provides some higher-level ELF access functionality.
   * libasm provides a programmable assembler interface.

%package -n %{static32}
Summary:	Static libraries for development with libelfutils (32-bit)
Group:		Development/Other
Requires:	%{dev32name} = %{EVRD}

%description -n %{static32}
This package contains the static libraries to create applications for
handling compiled objects.
%endif

%prep
%autosetup -p1
autoreconf -fi

# (tpg) use gcc, because clang fails to build it because of VLAIS
# https://wiki.openmandriva.org/en/Packages_forcing_gcc_use
# 2021-05-05 still fails with clang
export CC="gcc"
export CXX="g++"
export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
%configure32 \
	%{?_program_prefix: --program-prefix=%{_program_prefix}} \
	--disable-debuginfod \
	--disable-libdebuginfod \
	--disable-thread-safety \
	--with-zlib \
	--with-bzlib \
	--with-lzma
cd ..
%endif

mkdir build
cd build
%configure \
	%{?_program_prefix: --program-prefix=%{_program_prefix}} \
	--enable-debuginfod \
	--enable-libdebuginfod \
	--disable-thread-safety \
	--with-zlib \
	--with-bzlib \
	--with-zstd \
	--with-lzma

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

# (tpg) somehow it stucks on x86_64 and i586
%ifarch %{armx}
%check
make check || true
%endif

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

mkdir %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libelf.so.%{major} %{buildroot}%{_libdir}/libelf-%{version}.so %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libelf.so.%{major} %{buildroot}%{_libdir}/libelf.so

%find_lang %{name}

%files -f %{name}.lang
%doc NOTES README NEWS TODO
%{_bindir}/eu-*
%{_mandir}/man1/eu-*.1.*

%files -n %{libelf}
/%{_lib}/libelf-%{version}.so
/%{_lib}/libelf*.so.%{major}*

%files -n %{libdw}
%{_libdir}/libdw-%{version}.so
%{_libdir}/libdw*.so.%{major}*

%files -n %{libasm}
%{_libdir}/libasm-%{version}.so
%{_libdir}/libasm*.so.%{major}*

%files -n %{devname}
%{_includedir}/dwarf.h
%{_includedir}/libelf.h
%{_includedir}/gelf.h
%{_includedir}/nlist.h
%dir %{_includedir}/elfutils
%{_includedir}/elfutils/*.h
%{_libdir}/libelf.so
%{_libdir}/libdw.so
%{_libdir}/libasm.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/elf_*.3.*

%files -n %{static}
%{_libdir}/*.a

%files -n debuginfod
%{_sysconfdir}/profile.d/debuginfod.csh
%{_sysconfdir}/profile.d/debuginfod.sh
%{_bindir}/debuginfod
%{_bindir}/debuginfod-find
%{_mandir}/*/debuginfod*

%files -n %{libdebuginfod}
%{_libdir}/libdebuginfod-%{version}.so
%{_libdir}/libdebuginfod.so
%{_libdir}/libdebuginfod.so.1

%if %{with compat32}
%files -n %{lib32elf}
%{_prefix}/lib/libelf-%{version}.so
%{_prefix}/lib/libelf*.so.%{major}*

%files -n %{lib32dw}
%{_prefix}/lib/libdw-%{version}.so
%{_prefix}/lib/libdw*.so.%{major}*

%files -n %{lib32asm}
%{_prefix}/lib/libasm-%{version}.so
%{_prefix}/lib/libasm*.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libelf.so
%{_prefix}/lib/libdw.so
%{_prefix}/lib/libasm.so
%{_prefix}/lib/pkgconfig/*.pc

%files -n %{static32}
%{_prefix}/lib/*.a
%endif
