Name: hdf
Version: 4.2r1
Release: 13%{?dist}
Summary: A general purpose library and file format for storing scientific data
License: BSD-ish
Group: System Environment/Libraries
URL: http://hdf.ncsa.uiuc.edu/hdf4.html
#Source0: ftp://ftp.ncsa.uiuc.edu/HDF/HDF/HDF_Current/src/HDF%{version}.tar.gz
Source0: ftp://ftp.hdfgroup.org/HDF/HDF_Current/src/4.2r1-hrepack-p4.tar.gz
Patch0: hdf-4.2r1p4-maxavailfiles.patch
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
#%setup -q -n HDF%{version}
%setup -q -n 4.2r1-hrepack-p4
%patch -p1 -b .maxavailfiles
%patch1 -p1 -b .orig


%build
autoconf
export CFLAGS="$RPM_OPT_FLAGS -fPIC -DHAVE_NETCDF"
%configure F77=gfortran FFLAGS=-ffixed-line-length-none --disable-production
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
* Thu May 10 2007 Orion Poplawski <orion@cora.nwra.com> 4.2r1-13
- Remove netcdf-devel requires. (bug #239631)

* Fri Apr 20 2007 Orion Poplawski <orion@cora.nwra.com> 4.2r1-12
- Use 4.2r1-hrepack-p4.tar.gz for hrepack patch
- Remove configure patch applied upstream
- Use --disable-production configure flag to avoid stripping -g compile flag
- Add patch to fix open file test when run under mock

* Tue Aug 29 2006 Orion Poplawski <orion@cora.nwra.com> 4.2r1-11
- Rebuild for FC6

* Thu Apr 20 2006 Orion Poplawski <orion@cora.nwra.com> 4.2r1-10
- Add Requires netcdf-devel for hdf-devel (bug #189337)

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
