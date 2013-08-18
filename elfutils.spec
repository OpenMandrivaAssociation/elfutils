%define	major 1

#the old name was _libelfutils1
%define	libname	%mklibname %{name} %{major}

%define	libasm	%mklibname asm %{major}
%define libdw	%mklibname dw %{major}
%define	libelf	%mklibname elf %{major}
%define	devname	%mklibname %{name} -d
%define	static	%mklibname %{name} -d -s

%define _program_prefix eu-

Summary:	A collection of utilities and DSOs to handle compiled objects
Name:		elfutils
Version:	0.156
Release:	1
License:	GPLv2+
Group:		Development/Other
Url:		http://fedorahosted.org/elfutils/
Source0:	https://fedorahosted.org/releases/e/l/elfutils/%{version}/%{name}-%{version}.tar.bz2
# these 2 patches are from ftp://sources.redhat.com/pub/systemtap/elfutils/ 
# this hasn't been used since 200700 import why keep around
#Patch0:	https://fedorahosted.org/releases/e/l/elfutils/%{version}/elfutils-portability.patch
Patch1:		https://fedorahosted.org/releases/e/l/elfutils/%{version}/elfutils-robustify.patch
#Patch2:		elfutils-0.155-binutils-pr-ld-13621.patch
#Patch4:         elfutils-no-po-test-build.diff
Patch5:         libebl-prototype-fix.diff
Patch6:         elfutils-uninitialized.diff
Patch7:         elfutils-0.137-dwarf-header-check-fix.diff
Patch8:         elfutils-0.148-dont-crash.diff
Patch9:         elfutils-revert-portability-scanf.patch

# mdv patches
Patch10:	elfutils-0.155-mips_backend.patch
Patch11:	elfutils-0.139-sparc-align.patch
Patch12:	elfutils-0.139-fix-special-sparc-elf32-plt-entries.patch
Patch13:	elfutils-0.152-strip-.GCC.command.line-section.patch
Patch14:	elfutils-0.153-add-missing-lpthread-linkage.patch
Patch15:	elfutils_signed_comparison.patch
Patch17:	elfutils-0.153-dont-fail-on-strip-reloc-check-against-self.patch
Patch18:	elfutils-aarch64.patch

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	bzip2-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(zlib)
Obsoletes:	%{libname} < 0.155

%description
Elfutils is a collection of utilities, including ld (a linker),
nm (for listing symbols from object files), size (for listing the
section sizes of an object or archive file), strip (for discarding
symbols), readelf (to see the raw ELF file structures), and elflint
(to check for well-formed ELF files).

%package -n	%{libasm}
Summary:	Libraries to read and write ELF files
Group:		System/Libraries
Obsoletes:	%{libname} < 0.155

%description -n	%{libasm}
Included are the helper library which implement machine-specific ELF handling.

%package -n	%{libdw}
Summary:	Libraries to read and write ELF files
Group:		System/Libraries
Obsoletes:	%{libname} < 0.155

%description -n	%{libdw}
Included are the helper library which implement DWARF ELF handling.

%package -n	%{libelf}
Summary:	Libraries to read and write ELF files
Group:		System/Libraries
Obsoletes:	%{libname} < 0.155
Provides:	%{libname} = %{EVRD}
Requires:	%{libdw} = %{EVRD}
Requires:	%{libasm} = %{EVRD}

%description -n	%{libelf}
This package provides DSOs which allow reading and writing ELF files
on a high level.  Third party programs depend on this package to read
internals of ELF files.  The programs of the elfutils package use it
also to generate new ELF files.

%package -n	%{devname}
Summary:	Development libraries to handle compiled objects
Group:		Development/Other
Requires:	%{libasm} = %{EVRD}
Requires:	%{libdw} = %{EVRD}
Requires:	%{libelf} = %{EVRD}
Provides:	%{name}-devel

%description -n	%{devname}
This package contains the headers and dynamic libraries to create
applications for handling compiled objects.

   * libelf allows you to access the internals of the ELF object file
     format, so you can see the different sections of an ELF file.
   * libebl provides some higher-level ELF access functionality.
   * libasm provides a programmable assembler interface.

%package -n	%{static}
Summary:	Static libraries for development with libelfutils
Group:		Development/Other
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel

%description -n	%{static}
This package contains the static libraries to create applications for
handling compiled objects.

%prep
%setup -q
%apply_patches

%build
autoreconf -fi
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
pushd build-%{_target_platform}
make check || true
popd

%install
%makeinstall_std -C build-%{_target_platform}

mkdir %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libelf.so.%{major} %{buildroot}%{_libdir}/libelf-%{version}.so %{buildroot}/%{_lib}
ln -srf %{buildroot}/%{_lib}/libelf.so.%{major} %{buildroot}%{_libdir}/libelf.so

%find_lang %{name}

%files -f %{name}.lang
%doc NOTES README NEWS TODO
%{_bindir}/eu-*
%dir %{_libdir}/elfutils
%{_libdir}/elfutils/lib*.so

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

%files -n %{static}
%{_libdir}/*.a
