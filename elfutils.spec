%define major 1

#the old name was _libelfutils1
%define libname %mklibname %{name} %{major}
%define libasm %mklibname asm %{major}
%define libdw %mklibname dw %{major}
%define libelf %mklibname elf %{major}
%define devname %mklibname %{name} -d
%define static %mklibname %{name} -d -s

%define _program_prefix eu-
# (tpg) 2019-04-18 looks like it still does not work with binutils-2.32
# BUILDSTDERR: stack.c:590: error: undefined reference to 'dwfl_core_file_report'
%define _disable_lto 1
%global __provides_exclude ^libebl_.*\\.so.*$

%global optflags %{optflags} -Os -fstack-protector-strong -Wno-error

Summary:	A collection of utilities and DSOs to handle compiled objects
Name:		elfutils
Version:	0.178
Release:	1
License:	GPLv2+
Group:		Development/Other
Url:		https://sourceware.org/elfutils/
Source0:	https://sourceware.org/elfutils/ftp/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:	gcc
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(zlib)
Obsoletes:	%{libname} < 0.155

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

%prep
%autosetup -p1
autoreconf -fi

%build
# (tpg) use gcc, because clang fails to build it because of VLAIS
# https://wiki.openmandriva.org/en/Packages_forcing_gcc_use
export CC="gcc"
export CXX="g++"

%configure \
	%{?_program_prefix: --program-prefix=%{_program_prefix}} \
	--disable-debuginfod \
	--disable-thread-safety \
	--with-zlib \
	--with-bzlib \
	--with-lzma

%make_build

# (tpg) somehow it stucks on x86_64 and i586
%ifarch %{armx}
%check
make check || true
%endif

%install
%make_install

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
