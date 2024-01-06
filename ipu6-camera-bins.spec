%global debug_package %{nil}

# If you want to install ipu6-camera-hal to build gstreamer1-plugins-icamerasrc
# for the first time, you will first need to build this package
# --with bootstrap to avoid the circular depencency.
%bcond bootstrap 0

%global commit ff21b5556a9048903213c3545745a10fd4bb078a
%global commitdate 20230925
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           ipu6-camera-bins
Summary:        Binary library for Intel IPU6
Version:        0.0
Release:        9.%{commitdate}git%{shortcommit}%{?dist}
License:        Proprietary

Source0: https://github.com/intel/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  chrpath
BuildRequires:  patchelf

ExclusiveArch:  x86_64

Requires:       ipu6-camera-bins-firmware
Requires:       ivsc-firmware
%if %{without bootstrap}
Requires:       gstreamer1-plugins-icamerasrc
Requires:       v4l2-relayd
Requires:       intel-ipu6-kmod
%endif

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
chrpath --delete lib/ipu_*/*.so

%build
# Nothing to build

%install
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
cp -pr include/* %{buildroot}%{_includedir}/
for i in ipu_adl ipu_mtl ipu_tgl; do
  cp -pr lib/$i %{buildroot}%{_libdir}/
  patchelf --set-rpath %{_libdir}/$i %{buildroot}%{_libdir}/$i/*.so
  sed -i -e "s|/lib/|/lib64/|g" %{buildroot}%{_libdir}/$i/pkgconfig/*.pc
done

# IPU6 firmwares
mkdir -p %{buildroot}/usr/lib/firmware/intel
install -p -D -m 0644 lib/firmware/intel/*.bin %{buildroot}/usr/lib/firmware/intel/

%files
%license LICENSE
%dir %{_libdir}/ipu_*
%{_libdir}/ipu_*/*.so*

%files firmware
%license LICENSE
%dir /usr/lib/firmware
%dir /usr/lib/firmware/intel
/usr/lib/firmware/intel/*.bin

%files devel
%dir %{_includedir}/ipu_*
%dir %{_libdir}/ipu_*
%{_includedir}/ipu_*/*
%{_libdir}/ipu_*/pkgconfig/*
%{_libdir}/ipu_*/*.a

%changelog
* Mon Oct  9 2023 Matthias Saou <matthias@saou.eu> 0.0-9.20230925gitff21b55
- Update to commit ff21b5556a9048903213c3545745a10fd4bb078a.
- Major spec rework because of upstream file structure changes.
- Allow bootstraping related package builds (ipu6-camera-hal).

* Tue Aug 08 2023 Kate Hsuan <hpa@redhat.com> - 0.0-8.20230208git276859f
- Updated to commit 276859fc6de83918a32727d676985ec40f31af2b

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.0-7.20221112git4694ba7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 09 2023 Kate Hsuan <hpa@redhat.com> - 0.0-6.20221112git4694ba7
- Updated dependency settings

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
