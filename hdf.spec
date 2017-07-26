Name: hdf
Version: 4.2.13
Release: 2%{?dist}
Summary: A general purpose library and file format for storing scientific data
License: BSD
Group: System Environment/Libraries
URL: http://hdfgroup.org/products/hdf4/index.html
Source0: ftp://ftp.hdfgroup.org/HDF/HDF_Current/src/%{name}-%{version}.tar.bz2
Patch0: hdf-4.2.5-maxavailfiles.patch
Patch1: hdf-ppc.patch
Patch2: hdf-4.2.4-sparc.patch
Patch3: hdf-s390.patch
Patch4: hdf-arm.patch
# Support DESTDIR in install-examples
Patch5: hdf-destdir.patch
# Install examples into the right location
Patch6: hdf-examplesdir.patch
# Add AArch64 definitions
Patch8: hdf-4.2.10-aarch64.patch
# ppc64le support
# https://bugzilla.redhat.com/show_bug.cgi?id=1134385
Patch9: hdf-ppc64le.patch

# Fix syntax error on epel6 builds
# Use only if java is disabled
Patch10: hdf-avoid_syntax_error_el6.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# For destdir/examplesdir patches
BuildRequires: automake libtool
BuildRequires: flex byacc libjpeg-devel zlib-devel
%if "%{?dist}" != ".el4"
BuildRequires: gcc-gfortran
%else
BuildRequires: gcc-g77
%endif


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
Provides: %{name}-static = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: libjpeg-devel zlib-devel

%description devel
HDF development headers and libraries.


%prep
%setup -q
%patch0 -p1 -b .maxavailfiles
%patch1 -p1 -b .ppc
%patch2 -p1 -b .sparc
%patch3 -p1 -b .s390
%patch4 -p1 -b .arm
%patch5 -p1 -b .destdir
%patch6 -p0 -b .examplesdir
%patch8 -p1 -b .aarch64
%patch9 -p1 -b .ppc64le

## Fix syntax error bacause 'CLASSPATH_ENV=$H4_CLASSPATH' line on epel6 builds
# Use only if java is disabled
%if 0%{?rhel} < 7
%patch10 -p0
%endif

chmod a-x *hdf/*/*.c hdf/*/*.h
# restore include file timestamps modified by patching
touch -c -r ./hdf/src/hdfi.h.ppc ./hdf/src/hdfi.h


%build
# For destdir/examplesdir patches
autoreconf -vif
# avoid upstream compiler flags settings
rm config/*linux-gnu
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
export FFLAGS="$RPM_OPT_FLAGS -fPIC -ffixed-line-length-none"
%configure --disable-production --disable-java --disable-netcdf \
 --includedir=%{_includedir}/%{name} --libdir=%{_libdir}/%{name}

make
# correct the timestamps based on files used to generate the header files
touch -c -r hdf/src/hdf.inc hdf/src/hdf.f90
touch -c -r hdf/src/dffunc.inc hdf/src/dffunc.f90
touch -c -r mfhdf/fortran/mffunc.inc mfhdf/fortran/mffunc.f90
# netcdf fortran include need same treatement, but they are not shipped


%install
make install DESTDIR=%{buildroot} INSTALL='install -p'
rm  %{buildroot}%{_libdir}/%{name}/*.la
#Don't conflict with netcdf
for file in ncdump ncgen; do
  mv %{buildroot}%{_bindir}/$file %{buildroot}%{_bindir}/h$file
  # man pages are the same than netcdf ones
  rm %{buildroot}%{_mandir}/man1/${file}.1
done

# this is done to have the same timestamp on multiarch setups
touch -c -r README.txt %{buildroot}/%{_includedir}/hdf/h4config.h

# Remove an autoconf conditional from the API that is unused and cause
# the API to be different on x86 and x86_64
pushd %{buildroot}/%{_includedir}/hdf
grep -v 'H4_SIZEOF_INTP' h4config.h > h4config.h.tmp
touch -c -r h4config.h h4config.h.tmp
mv h4config.h.tmp h4config.h
popd


%check
make check


%files
%license COPYING
%doc MANIFEST README.txt release_notes/*.txt
%exclude %{_defaultdocdir}/%{name}/examples
%{_bindir}/*
%{_mandir}/man1/*.gz

%files devel
%{_includedir}/%{name}/
%{_libdir}/%{name}/
%{_defaultdocdir}/%{name}/examples


%changelog
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Antonio Trande <sagitter@fedoraproject.org> 4.2.13-1
- Update to 4.2.13

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> 4.2.12-1
- Update to 4.2.12

* Wed May 25 2016 Orion Poplawski <orion@cora.nwra.com> 4.2.11-4
- Cleanup spec
- Remove .la files
- Use %%license

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 Orion Poplawski <orion@cora.nwra.com> 4.2.11-1
- Update to 4.2.11
- Drop format patch applied upstream
- Update destdir patch

* Mon Sep 8 2014 Orion Poplawski <orion@cora.nwra.com> - 4.2.10-7
- Updated patch for ppc64le support (bug #1134385)

* Wed Sep 3 2014 Orion Poplawski <orion@cora.nwra.com> - 4.2.10-6
- Add initial attempt at ppc64le support (bug #1134385)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 25 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> 4.2.10-4
- Add AArch64 support.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Jakub Čajka <jcajka@redhat.com> 4.2.10-2
- Fixed build/tests on s390x
- Tests enabled on ppc

* Fri Feb 14 2014 Orion Poplawski <orion@cora.nwra.com> 4.2.10-1
- Update to 4.2.10
- Rebase arm, ppc, and s390 patches
- Add destdir, examplesdir patches to fix installation of examples

* Sat Feb 1 2014 Orion Poplawski <orion@cora.nwra.com> 4.2.9-4
- Fix build with -Werror=format-security (bug #1037120)

* Tue Aug 13 2013 Karsten Hopp <karsten@redhat.com> 4.2.9-3
- temporarily skip checks on ppc* (#961007)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Orion Poplawski <orion@cora.nwra.com> 4.2.9-1
- Update to 4.2.9
- Add patch for some missing declarations
- Add patch to fix integer wrapping in test

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 4.2.8-3
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 4.2.8-2
- rebuild against new libjpeg

* Wed Aug 15 2012 Orion Poplawski <orion@cora.nwra.com> 4.2.8-1
- Update to 4.2.8

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 DJ Delorie <dj@redhat.com> 4.2.7-2
- Add patch for ARM support

* Wed Feb 15 2012 Orion Poplawski <orion@cora.nwra.com> 4.2.7-1
- Update to 4.2.7

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Orion Poplawski <orion@cora.nwra.com> 4.2.6-1
- Update to 4.2.6
- Drop jpeg patch, fixed upstream
- Update ppc,s390 patches

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 10 2010 Orion Poplawski <orion@cora.nwra.com> 4.2.5-2
- Add patch to disable jpeg tests due to change to jpeg-turbo, FTBFS bug 631337

* Tue Mar 2 2010 Orion Poplawski <orion@cora.nwra.com> 4.2.5-1
- Update to 4.2.5

* Fri Sep 18 2009 Orion Poplawski <orion@cora.nwra.com> 4.2r4-5
- Add EL4 build conditionals

* Thu Aug 13 2009 Orion Poplawski <orion@cora.nwra.com> 4.2r4-4
- Add -fPIC to FFLAGS

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2r4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 7 2009 Orion Poplawski <orion@cora.nwra.com> 4.2r4-2
- Add Provides hdf-static to hdf-devel (bug #494529)

* Wed Feb 25 2009 Orion Poplawski <orion@cora.nwra.com> 4.2r4-1
- Update to 4.2r4
- Add patch to increase buffer size in test
- Drop upstreamed libm patch

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2r3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct  1 2008 Orion Poplawski <orion@cora.nwra.com> 4.2r3-4
- Rebase maxavailfiles patch

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 4.2r3-3
- Fix Patch0:/%%patch mismatch.

* Sun Mar  2 2008 Patrice Dumas <pertusus@free.fr> 4.2r3-2
- don't ship an empty netcdf.h file. The related definitions are now
  in hdf4_netcdf.h

* Tue Feb  5 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.r3-1
- Update to 4.2r3

* Tue Feb  5 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.r2-7
- Add patch to add -lm to hdiff link

* Tue Feb  5 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.r2-6
- Add patch for s390 support (bug #431511)

* Mon Jan  7 2008 Orion Poplawski <orion@cora.nwra.com> 4.2.r2-5
- Add patches for sparc support (bug #427639)

* Mon Oct 29 2007 Patrice Dumas <pertusus@free.fr> 4.2r2-4
- install the netcdf.h file that describes the netcdf2 hdf enabled
  API

* Mon Oct 29 2007 Patrice Dumas <pertusus@free.fr> 4.2r2-3
- ship hdf enabled nc* utils as hnc*
- add --disable-netcdf that replaces HAVE_NETCDF
- keep include files timestamps, and have the same accross arches
- fix multiarch difference in include files (#341491)

* Wed Oct 17 2007 Patrice Dumas <pertusus@free.fr> 4.2r2-2
- update to 4.2r2

* Fri Aug 24 2007 Orion Poplawski <orion@cora.nwra.com> 4.2r1-15
- Update license tag to BSD
- Rebuild for BuildID

* Thu May 10 2007 Balint Cristian <cbalint@redhat.com> 4.2r1-14
- Fix ppc64 too.

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
