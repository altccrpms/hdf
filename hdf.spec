Name: hdf
Version: 4.2r1
Release: 9%{?dist}
Summary: A general purpose library and file format for storing scientific data
License: BSD-ish
Group: System Environment/Libraries
URL: http://hdf.ncsa.uiuc.edu/hdf4.html
Source0: ftp://ftp.ncsa.uiuc.edu/HDF/HDF/HDF_Current/src/HDF%{version}.tar.gz
Source1: ftp://ftp.ncsa.uiuc.edu/HDF/HDF/HDF_Current/src/patches/4.2r1-hrepack-patch.tar
Patch0: hdf-4.2r1-configure.patch
Patch1: hdf-4.2r1-ppc.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: autoconf flex byacc libjpeg-devel zlib-devel
BuildRequires: gcc-gfortran

%description
HDF is a general purpose library and file format for storing scientific data.
HDF can store two primary objects: datasets and groups. A dataset is 
essentially a multidimensional array of data elements, and a group is a 
structure for organizing objects in an HDF file. Using these two basic 
objects, one can create and store almost any kind of scientific data 
structure, such as images, arrays of vectors, and structured and unstructured 
grids. You can also mix and match them in HDF files according to your needs.

%package devel
Summary: HDF development files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libjpeg-devel zlib-devel

%description devel
HDF development headers and libraries.

%prep
%setup -q -n HDF%{version}
tar xf %{SOURCE1} --directory mfhdf/hrepack 
mv mfhdf/hrepack/4.2r1-hrepack-patch/*.[ch] mfhdf/hrepack
rm -r mfhdf/hrepack/4.2r1-hrepack-patch
%patch0 -p1 -b .orig
%patch1 -p1 -b .orig

%build
autoconf
export CFLAGS="$RPM_OPT_FLAGS -fPIC -DHAVE_NETCDF"
%configure F77=gfortran FFLAGS=-ffixed-line-length-none
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall includedir=${RPM_BUILD_ROOT}%{_includedir}/%{name} \
             libdir=$RPM_BUILD_ROOT%{_libdir}/%{name}
#Don't conflict with netcdf
rm $RPM_BUILD_ROOT%{_bindir}/nc* $RPM_BUILD_ROOT%{_mandir}/man1/nc*

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%post

%postun

%files
%defattr(-,root,root,0755)
%doc COPYING MANIFEST README release_notes/*.txt
%{_bindir}/*
%{_mandir}/man1/*.gz

%files devel
%defattr(-,root,root,0755)
%{_includedir}/%{name}/
%{_libdir}/%{name}/

%changelog
* Mon Feb 13 2006 Orion Poplawski <orion@cora.nwra.com> 4.2r1-9
- Rebuild for gcc/glibc changes

* Wed Feb  8 2006 Orion Poplawski <orion@cora.nwra.com> 4.2r1-8
- Compile with -DHAVE_NETCDF for gdl hdf/netcdf compatibility

* Thu Feb  2 2006 Orion Poplawski <orion@cora.nwra.com> 4.2r1-7
- Add patch to build on ppc

* Wed Dec 21 2005 Orion Poplawski <orion@cora.nwra.com> 4.2r1-6
- Rebuild

* Wed Oct 05 2005 Orion Poplawski <orion@cora.nwra.com> 4.2r1-5
- Add Requires: libjpeg-devel zlib-devel to -devel package

* Tue Aug 23 2005 Orion Poplawski <orion@cora.nwra.com> 4.2r1-4
- Use -fPIC
- Fix project URL

* Fri Jul 29 2005 Orion Poplawski <orion@cora.nwra.com> 4.2r1-3
- Exclude ppc/ppc64 - HDF does not recognize it

* Wed Jul 20 2005 Orion Poplawski <orion@cora.nwra.com> 4.2r1-2
- Fix BuildRequires to have autoconf

* Fri Jul 15 2005 Orion Poplawski <orion@cora.nwra.com> 4.2r1-1
- inital package for Fedora Extras
