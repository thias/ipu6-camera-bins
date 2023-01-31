%global debug_package %{nil}

%global commit 4694ba7ee51652d29ef41e7fde846b83a2a1c53b
%global commitdate 20221112
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           ipu6-camera-bins
Summary:        Binary library for Intel IPU6
Version:        0.0
Release:        5.%{commitdate}git%{shortcommit}%{?dist}
License:        Proprietary

Source0: https://github.com/intel/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  chrpath
BuildRequires:  patchelf

ExclusiveArch:  x86_64

# For kmod package
Provides:       intel-ipu6-kmod-common = %{version}

%description
This provides the necessary binaries for Intel IPU6, including library and
firmware. The library includes necessary image processing algorithms and
3A algorithm for the camera.

%package firmware
Summary:        IPU6 firmware

%description firmware
This provides the necessary firmware for Intel IPU6.

%package devel
Summary:        IPU6 header files for development.
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This provides the necessary header files for IPU6 development.

%prep

%setup -q -n %{name}-%{commit}
for i in ipu6 ipu6ep; do
  chrpath --delete $i/lib/*.so
done

%build
# Nothing to build

%install
for i in ipu6 ipu6ep; do
  mkdir -p %{buildroot}%{_includedir}/$i
  mkdir -p %{buildroot}%{_libdir}/$i
  cp -pr $i/include/* %{buildroot}%{_includedir}/$i/
  cp -pr $i/lib/lib* $i/lib/pkgconfig %{buildroot}%{_libdir}/$i
  patchelf --set-rpath %{_libdir}/$i %{buildroot}%{_libdir}/$i/*.so
  sed -i \
    -e "s|libdir=/usr/lib|libdir=%{_libdir}|g" \
    -e "s|libdir}|libdir}/$i|g" \
    -e "s|includedir}|includedir}/$i|g" \
    %{buildroot}%{_libdir}/$i/pkgconfig/*.pc
done

# IPU6 firmwares
install -p -D -m 0644 ipu6/lib/firmware/intel/ipu6_fw.bin %{buildroot}/usr/lib/firmware/intel/ipu6_fw.bin
install -p -D -m 0644 ipu6ep/lib/firmware/intel/ipu6ep_fw.bin %{buildroot}/usr/lib/firmware/intel/ipu6ep_fw.bin

%files
%license LICENSE
%dir %{_libdir}/ipu6
%dir %{_libdir}/ipu6ep
%{_libdir}/ipu6/*.so*
%{_libdir}/ipu6ep/*.so*

%files firmware
%license LICENSE
%dir /usr/lib/firmware
%dir /usr/lib/firmware/intel
/usr/lib/firmware/intel/ipu6_fw.bin
/usr/lib/firmware/intel/ipu6ep_fw.bin

%files devel
%dir %{_includedir}/ipu6
%dir %{_includedir}/ipu6ep
%dir %{_libdir}/ipu6/pkgconfig
%dir %{_libdir}/ipu6ep/pkgconfig
%{_includedir}/ipu6/*
%{_includedir}/ipu6ep/*
%{_libdir}/ipu6/pkgconfig/*
%{_libdir}/ipu6ep/pkgconfig/*
%{_libdir}/ipu6/*.a
%{_libdir}/ipu6ep/*.a


%changelog
* Tue Dec 13 2022 Kate Hsuan <hpa@redhat.com> - 0.0-5.20221112git4694ba7
- Fix indentation.
- Remove unnecessary dir macro.

* Thu Dec 8 2022 Kate Hsuan <hpa@redhat.com> - 0.0-4.20221112git4694ba7
- Add Requires to make sure version lock between main and -devel package.
  Move .a files to -devel package.
  Fix dir settings.
  Remove unnecessary for loop and duplicated commands.

* Mon Dec 5 2022 Kate Hsuan <hpa@redhat.com> - 0.0-3.20221112git4694ba7
- Set correct rpath for every .so files and put the ExclusiveArch to the
  suitable place.

* Tue Nov 22 2022 Kate Hsuan <hpa@redhat.com> - 0.0-2.20221112git4694ba7
- Small tweaks as a result of pkg-review (rf#6474), including
  setup macro parameters, path settings, and dependency settings.

* Thu Nov 17 2022 Kate Hsuan <hpa@redhat.com> - 0.0-1.20221112git4694ba7
- Revision is based on the pkg-review (rf#6474#c2).

* Tue Oct 25 2022 Kate Hsuan <hpa@redhat.com> - 0.0.1
- First commit
