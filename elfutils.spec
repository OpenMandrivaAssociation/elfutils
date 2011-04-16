%define major 1
%define libname	%mklibname %{name} %{major}
%define libnamedevel %mklibname %{name} -d
%define libnamestaticdevel %mklibname %{name} -d -s

%define _program_prefix eu-

%bcond_without	check
%bcond_with	compat

Summary:	A collection of utilities and DSOs to handle compiled objects
Name:		elfutils
Version:	0.152
Release:	3
License:	GPLv2+
Group:		Development/Other
Url:		http://fedorahosted.org/elfutils/
Source0:	http://fedorahosted.org/releases/e/l/elfutils/%{name}-%{version}.tar.bz2
Source1:	%{SOURCE0}.sig
# these 2 patches are from ftp://sources.redhat.com/pub/systemtap/elfutils/ 
Patch0:		elfutils-portability.patch
Patch1:		elfutils-robustify.patch

# mdv patches
Patch10:	elfutils-0.145-mips_backend.patch
Patch11:	elfutils-0.139-sparc-align.patch
Patch12:	elfutils-0.139-fix-special-sparc-elf32-plt-entries.patch
Patch13:	elfutils-0.152-strip-.GCC.command.line-section.patch
Requires:	%{libname} = %{version}-%{release}
%if %{with compat}
BuildRequires:	gcc >= 3.2
%else
BuildRequires:	gcc >= 3.4
%endif
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	glibc-devel
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	lzma-devel
BuildRequires:	gettext-devel

%description
Elfutils is a collection of utilities, including ld (a linker),
nm (for listing symbols from object files), size (for listing the
section sizes of an object or archive file), strip (for discarding
symbols), readelf (to see the raw ELF file structures), and elflint
(to check for well-formed ELF files).

%package -n	%{libnamedevel}
Summary:	Development libraries to handle compiled objects
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel 
Provides:	lib%{name}-devel
Obsoletes:	libelf-devel < 0.137
Obsoletes:	libelf0-devel < 0.137
Obsoletes:	%{_lib}%{name}1-devel < 0.137
Provides:	libelf-devel libelf0-devel

%description -n	%{libnamedevel}
This package contains the headers and dynamic libraries to create
applications for handling compiled objects.

   * libelf allows you to access the internals of the ELF object file
     format, so you can see the different sections of an ELF file.
   * libebl provides some higher-level ELF access functionality.
   * libasm provides a programmable assembler interface.

%package -n	%{libnamestaticdevel}
Summary:	Static libraries for development with libelfutils
Group:		Development/Other
Requires:	%{libnamedevel} = %{version}-%{release}
Provides:	%{name}-static-devel 
Obsoletes:	libelf-static-devel < 0.137
Obsoletes:	libelf0-static-devel < 0.137
Provides:	libelf-static-devel
Provides:	libelf0-static-devel
Obsoletes:	%{_lib}%{name}1-static-devel < 0.137

%description -n	%{libnamestaticdevel}
This package contains the static libraries to create applications for
handling compiled objects.

%package -n	%{libname}
Summary:	Libraries to read and write ELF files
Group:		System/Libraries
Provides:	lib%{name}
Obsoletes:	libelf < 0.137
Obsoletes:	libelf0 < 0.137
Provides:	libelf
Provides:	libelf0

%description -n	%{libname}
This package provides DSOs which allow reading and writing ELF files
on a high level.  Third party programs depend on this package to read
internals of ELF files.  The programs of the elfutils package use it
also to generate new ELF files.

Also included are numerous helper libraries which implement DWARF,
ELF, and machine-specific ELF handling.

%prep
%setup -q
%if %{with compat}
%patch0 -p1 -b .portability~
sleep 1
find . \( -name Makefile.in -o -name aclocal.m4 \) -print | xargs touch
sleep 1
find . \( -name configure -o -name config.h.in \) -print | xargs touch
%endif

%patch1 -p1 -b .robustify~
%patch10 -p1 -b .mips~
%patch11 -p1 -b .sparc_align~
%patch12 -p1 -b .sparc_elf32_plt~
%patch13 -p1 -b .gcc_switches~

%build
autoreconf -fiv

mkdir build-%{_target_platform}
pushd build-%{_target_platform}

# [pixel] libld_elf_i386.so is quite weird, could be dropped? workarounding for now...
%define _disable_ld_no_undefined 1

CFLAGS="%{optflags} -Wno-error" \
CONFIGURE_TOP=.. \
%configure2_5x \
	%{?_program_prefix: --program-prefix=%{_program_prefix}} \
	--enable-thread-safety \
	--with-zlib \
	--with-bzlib \
	--with-lzma

%make
popd

%check
%if %{with check}
pushd build-%{_target_platform}
%make check
popd
%endif

%install
%makeinstall_std -C build-%{_target_platform}

chmod +x %{buildroot}%{_libdir}/lib*.so*
chmod +x %{buildroot}%{_libdir}/elfutils/lib*.so*

%find_lang %{name}

%files -f %{name}.lang
%doc NOTES README NEWS TODO
%{_bindir}/eu-*

%files -n %{libnamedevel}
%{_includedir}/dwarf.h
%{_includedir}/libelf.h
%{_includedir}/gelf.h
%{_includedir}/nlist.h
%dir %{_includedir}/elfutils
%{_includedir}/elfutils/*.h
%{_libdir}/libelf.so
%{_libdir}/libdw.so
%{_libdir}/libasm.so
%{_libdir}/elfutils/lib*.so
%exclude %{_libdir}/elfutils/lib*-%{version}.so

%files -n %{libnamestaticdevel}
%{_libdir}/*.a

%files -n %{libname}
%{_libdir}/libelf-%{version}.so
%{_libdir}/libelf*.so.%{major}*
%{_libdir}/libdw-%{version}.so
%{_libdir}/libdw*.so.*
%{_libdir}/libasm-%{version}.so
%{_libdir}/libasm*.so.*
%dir %{_libdir}/elfutils
%{_libdir}/elfutils/lib*-%{version}.so
