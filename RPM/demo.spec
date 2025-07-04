Name:       android-remote-mediaserver-tv
Summary:    MediaServer for Tizen TV
Version:    0.0.5
Release:    0
Group:      Multimedia/MediaServer
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(ttrace)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(boost)
BuildRequires:  pkgconfig(jsoncpp)
BuildRequires:  pkgconfig(ecore-wayland)
BuildRequires:  pkgconfig(appcore-efl)
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(evas)
BuildRequires:  pkgconfig(ecore-wl2)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(tizen-extension-client)
BuildRequires:  pkgconfig(tv-resource-manager)
BuildRequires:  pkgconfig(tv-resource-information)
BuildRequires:  pkgconfig(resource-center-api)
BuildRequires:  pkgconfig(audio-control)
BuildRequires:  pkgconfig(plusplayer)
BuildRequires:  pkgconfig(capi-trackrenderer-tv)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(libavoc)
BuildRequires:  pkgconfig(factory-api)
BuildRequires:  pkgconfig(capi-screensaver)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(logger)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(capi-boost-tv)
BuildRequires:  pkgconfig(capi-android-utils-tv)
BuildRequires:  pkgconfig(capi-encoder-tv)

#for drm
BuildRequires:  pkgconfig(drmdecrypt)

# For gbinder
BuildRequires:  pkgconfig(libglibutil)
BuildRequires:  pkgconfig(libgbinder)

# For Texturing
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(graphics-control)
BuildRequires:  pkgconfig(libdrm)

# For download ignore app list
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(VDCurl)
BuildRequires:  pkgconfig(vd-capi-network)
BuildRequires:  pkgconfig(capi-network-connection)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(deviced)

# For google test
BuildRequires:  pkgconfig(gtest)

%define _packagedir /usr
%define _bindir %{_packagedir}/bin
%define _includedir %{_packagedir}/include
%define _pkgconfigdir %{_libdir}/pkgconfig

%description
MediaServer for Tizen TV

%package devel
Summary:    Developement for MediaServer
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
%devel_desc

%if 0%{?enable_ut:1}
%package ut
Summary:    Unit Testing for MediaServer
Group:      Development/Testing
Requires:   %{name} = %{version}-%{release}

%description ut
A testing package for mediaserver

%if 0%{?vd_gcov:1}
%package gcov
Summary: gcov enabled package
Group: gcov package

%description gcov
This package is gcov package for coverage measurement.
%endif  # << vd_gcov
%endif  # << enable_ut

%prep
%setup -q

%build
# export CFLAGS="$CFLAGS -static-libasan"
# export CXXFLAGS="$CXXFLAGS -static-libasan"

%if 0%{?enable_ut:1}
%if 0%{?vd_gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov --coverage"
%endif  # << vd_gcov
%endif  # << enable_ut

%if 0%{?enable_ut:1}
%define _build_tests ON
%else   # << enable_ut
%define _build_tests OFF
%endif  # << enable_ut

%if 0%{?enable_tools:1}
%define _build_tools ON
%else   # << enable_tools
%define _build_tools OFF
%endif  # << enable_tools

%if "%{_vd_cfg_product_type}" == "IWB"
%define _audio_enable_service OFF
%define _codec_multiwindow_support ON
%define _codec_use_feature_list OFF
%else
%define _audio_enable_service ON
%define _codec_multiwindow_support OFF
%define _codec_use_feature_list ON
%endif

%cmake . \
    -DBUILD_TESTS=%{_build_tests} \
    -DBUILD_TOOLS=%{_build_tools} \
    -DAUDIO_ENABLE_SERVICE=%{_audio_enable_service} \
    -DCODEC_MULTI_WINDOW=%{_codec_multiwindow_support} \
    -DCODEC_USE_FEATURELIST=%{_codec_use_feature_list} \
    -DLIBDIR=%{_libdir}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%define _service_target basic.target.wants

mkdir -p %{buildroot}%{_unitdir}/%{_service_target}
%if 0%{?enable_tools:1}
install -m 0644 packaging/aot-aidl-mediaserver.service %{buildroot}%{_unitdir}/aot-aidl-mediaserver.service
install -m 0644 packaging/aot-hidl-mediaserver.service %{buildroot}%{_unitdir}/aot-hidl-mediaserver.service
%endif  # << enable_tools
install -m 0644 packaging/aot-mediaserver.service %{buildroot}%{_unitdir}/aot-mediaserver.service
%if "%{_audio_enable_service}" == "ON"
install -m 0644 packaging/aot-audioserver.service %{buildroot}%{_unitdir}/aot-audioserver.service
%endif # << _audio_enable_service
%if 0%{?enable_tools:1}
%install_service %{_service_target} aot-aidl-mediaserver.service
%install_service %{_service_target} aot-hidl-mediaserver.service
%endif  # << enable_tools
%install_service %{_service_target} aot-mediaserver.service
%if "%{_audio_enable_service}" == "ON"
%install_service %{_service_target} aot-audioserver.service
%endif # << _audio_enable_service

%if 0%{?enable_ut:1}
%if 0%{?vd_gcov:1}
mkdir -p %{buildroot}%{_datadir}/gcov/obj
find . \( -name '*.gcno' -o -name '*.cpp' -o -name '*.c' -o -name '*.hpp' -o -name '*.h' \) ! -path "./libs/*" ! -path "*/test/*" ! -path "*/CompilerIdC/*" ! -path "*/CompilerIdCXX/*" -exec cp --parents -r '{}' %{buildroot}%{_datadir}/gcov/obj ';'
%endif  # << vd_gcov
%endif  # << enable_ut

%post	
/sbin/ldconfig	

%postun	
/sbin/ldconfig

%files
%manifest android-remote-mediaserver.manifest
%defattr(-,root,root,-)
%{_unitdir}/aot-mediaserver.service
%{_unitdir}/%{_service_target}/aot-mediaserver.service
%if "%{_audio_enable_service}" == "ON"
%{_unitdir}/aot-audioserver.service
%{_unitdir}/%{_service_target}/aot-audioserver.service
%endif # << _audio_enable_service
%{_libdir}/libandroid-remote-*.so*
%{_bindir}/aot-mediaserver
%if "%{_audio_enable_service}" == "ON"
%{_bindir}/aot-audioserver
%endif # << _audio_enable_service
%if 0%{?enable_tools:1}
%{_bindir}/aot-hidl-mediaserver
%{_bindir}/aot-aidl-mediaserver
%endif  # << enable_tools

%files devel
%defattr(-,root,root,-)
%{_pkgconfigdir}/android-remote-mediaserver-tv.pc
%{_includedir}/*

%if 0%{?enable_ut:1}
%files ut
%{_bindir}/ut-arms-codec
%if "%{_audio_enable_service}" == "ON"
%{_bindir}/ut-arms-audiotrack
%endif # << _audio_enable_service
%{_bindir}/ut-arms-common

%if 0%{?vd_gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif  # << vd_gcov
%endif  # << enable_ut
