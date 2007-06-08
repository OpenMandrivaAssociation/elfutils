%define name	elfutils
%define version	0.127
%define release	%mkrel 1

%define major	1
%define libname	%mklibname %{name} %{major}

%define _gnu	%{nil}
%define _program_prefix eu-

%ifarch %{sunsparc}
%define	build_check		1
%else
%define build_check		1
%endif
%{expand: %{?_without_CHECK:	%%global build_check 0}}
%{expand: %{?_with_CHECK:	%%global build_check 1}}

%define build_compat		0
%if %{mdkversion} < 1010
%define build_compat		1
%endif
%{expand: %{?_without_COMPAT:	%%global build_compat 0}}
%{expand: %{?_with_COMPAT:	%%global build_compat 1}}

Summary:	A collection of utilities and DSOs to handle compiled objects
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
Source0:	elfutils-%{version}.tar.gz
Patch0:		elfutils-0.127-portability.patch
Patch1:		elfutils-0.127-robustify.patch
Patch2:		elfutils-0.120-fix-sparc-build.patch
#Patch3:		elfutils-0.125-warn_unused_result.patch
Patch4:		elfutils-0.124-strip-copy-symtab.patch
Patch5:		elfutils-0.108-align.patch
Patch6:		elfutils-0.123-fix-special-sparc-elf32-plt-entries.patch
Requires:	%{libname} = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
%if %{build_compat}
BuildRequires:	gcc >= 3.2
%else
BuildRequires:	gcc >= 3.4
%endif
BuildRequires:	sharutils
BuildRequires:	libtool-devel

%description
Elfutils is a collection of utilities, including:

   * %{_program_prefix}nm: for listing symbols from object files
   * %{_program_prefix}size: for listing the section sizes of an object or archive file
   * %{_program_prefix}strip: for discarding symbols
   * %{_program_prefix}readelf: the see the raw ELF file structures
   * %{_program_prefix}elflint: to check for well-formed ELF files

%package -n	%{libname}-devel
Summary:	Development libraries to handle compiled objects
Group:		Development/Other
License:	GPL
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel lib%{name}-devel
Obsoletes:	libelf-devel libelf0-devel
Provides:	libelf-devel libelf0-devel

%description -n	%{libname}-devel
This package contains the headers and dynamic libraries to create
applications for handling compiled objects.

   * libelf allows you to access the internals of the ELF object file
     format, so you can see the different sections of an ELF file.
   * libebl provides some higher-level ELF access functionality.
   * libasm provides a programmable assembler interface.

%package -n	%{libname}-static-devel
Summary:	Static libraries for development with libelfutils
Group:		Development/Other
License:	GPL
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	%{name}-static-devel lib%{name}-static-devel
Obsoletes:	libelf-static-devel libelf0-static-devel
Provides:	libelf-static-devel libelf0-static-devel

%description -n	%{libname}-static-devel
This package contains the static libraries to create applications for
handling compiled objects.

%package -n	%{libname}
Summary:	Libraries to read and write ELF files
Group:		System/Libraries
License:	OSL
Provides:	lib%{name}
Obsoletes:	libelf libelf0
Provides:	libelf libelf0

%description -n	%{libname}
This package provides DSOs which allow reading and writing ELF files
on a high level.  Third party programs depend on this package to read
internals of ELF files.  The programs of the elfutils package use it
also to generate new ELF files.

Also included are numerous helper libraries which implement DWARF,
ELF, and machine-specific ELF handling.

%prep
%setup -q
%if %{build_compat}
%patch0 -p1 -b .portability

sleep 1
find . \( -name Makefile.in -o -name aclocal.m4 \) -print | xargs touch
sleep 1
find . \( -name configure -o -name config.h.in \) -print | xargs touch
%endif
# Don't use -Werror with -Wformat=2 -std=gnu99 as %a[ won't be caught
# as the GNU %a extension.
perl -pi -e '/AM_CFLAGS =/ and s/-Werror//g' ./tests/Makefile.{in,am}
%patch1 -p1 -b .robustify
%patch2 -p1 -b .sparc
#%patch3 -p0 -b .warn_unused_result
%patch4 -p1 -b .strip_copy_symtab
%patch5 -p1 -b .align
%patch6 -p1 -b .sparc_elf32_plt

%build
mkdir build-%{_target_platform}
pushd build-%{_target_platform}
CONFIGURE_TOP=.. \
%configure2_5x \
%{?_program_prefix: --program-prefix=%{_program_prefix}} --enable-shared
%make
popd

%check
%if %{build_check}
pushd build-%{_target_platform}
%make check || :
popd
%endif

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_prefix}

%makeinstall_std -C build-%{_target_platform}

chmod +x %{buildroot}%{_libdir}/lib*.so*
chmod +x %{buildroot}%{_libdir}/elfutils/lib*.so*

# XXX Nuke unpackaged files
{ cd %{buildroot}
  rm -f .%{_bindir}/eu-ld
  rm -f .%{_bindir}/eu-objdump
  rm -f .%{_includedir}/elfutils/libasm.h
  rm -f .%{_libdir}/libasm-%{version}.so
  rm -f .%{_libdir}/libasm.{a,so}
}

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc NOTES README NEWS TODO
%{_bindir}/eu-addr2line
%{_bindir}/eu-ar
%{_bindir}/eu-elfcmp
%{_bindir}/eu-findtextrel
%{_bindir}/eu-elflint
#%{_bindir}/eu-ld
%{_bindir}/eu-nm
%{_bindir}/eu-ranlib
%{_bindir}/eu-readelf
%{_bindir}/eu-size
%{_bindir}/eu-strip
%{_bindir}/eu-strings
%{_libdir}/libdw-%{version}.so
%{_libdir}/libdw*.so.*
%dir %{_libdir}/elfutils
%{_libdir}/elfutils/lib*.so

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/dwarf.h
%{_includedir}/libelf.h
%{_includedir}/gelf.h
%{_includedir}/nlist.h
%dir %{_includedir}/elfutils
%{_includedir}/elfutils/elf-knowledge.h
%{_includedir}/elfutils/libebl.h
%{_includedir}/elfutils/libdw.h
%{_includedir}/elfutils/libdwfl.h
#%{_libdir}/libasm.so
#%{_libdir}/libdwarf.so
#%{_libdir}/libebl.so
%{_libdir}/libelf.so
%{_libdir}/libdw.so

%files -n %{libname}-static-devel
%defattr(-,root,root)
#%{_libdir}/libasm.a
%{_libdir}/libebl.a
%{_libdir}/libelf.a
%{_libdir}/libdw.a

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libelf-%{version}.so
%{_libdir}/libelf*.so.*
#%{_libdir}/libasm-%{version}.so
#%{_libdir}/libasm*.so.*
#%{_libdir}/libebl-%{version}.so
#%{_libdir}/libebl*.so.*


