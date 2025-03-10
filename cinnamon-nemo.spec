# NOTE: "nemo" package name is already occupied, so use cinnamon-nemo
#
# Conditional build:
%bcond_without	apidocs		# gtk-doc based API documentation
%bcond_without	selinux		# SELinux support
%bcond_without	tracker		# Tracker support

%define		translations_version	6.4.2
Summary:	Nemo - file manager for Cinnamon desktop
Summary(pl.UTF-8):	Nemo - zarządca plików dla środowiska Cinnamon
Name:		cinnamon-nemo
Version:	6.4.5
Release:	1
License:	LGPL v2+ (extensions API), GPL v2+ (Nemo itself)
Group:		X11/Applications
#Source0Download: https://github.com/linuxmint/nemo/tags
Source0:	https://github.com/linuxmint/nemo/archive/%{version}/nemo-%{version}.tar.gz
# Source0-md5:	8aa031084128c7fb6d7b9c75cc53c84d
#Source1Download: https://github.com/linuxmint/cinnamon-translations/tags
Source1:	https://github.com/linuxmint/cinnamon-translations/archive/%{translations_version}/cinnamon-translations-%{translations_version}.tar.gz
# Source1-md5:	2a92606a2dcdc696889f08edd12f6bb6
URL:		https://github.com/linuxmint/Cinnamon
BuildRequires:	cinnamon-desktop-devel >= 4.8.0
BuildRequires:	exempi-devel >= 2.2.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.45.7
BuildRequires:	gobject-introspection-devel >= 1.0
BuildRequires:	gtk+3-devel >= 3.10.0
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.4}
BuildRequires:	json-glib-devel >= 1.6
BuildRequires:	libexif-devel >= 1:0.6.20
BuildRequires:	libnotify-devel >= 0.7.0
%{?with_selinux:BuildRequires:	libselinux-devel >= 2.0}
BuildRequires:	libxml2-devel >= 1:2.7.8
BuildRequires:	meson >= 0.56.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pango-devel >= 1:1.44.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
%{?with_tracker:BuildRequires:	tracker3-devel >= 3.0}
BuildRequires:	xapps-devel >= 2.0.0
BuildRequires:	xorg-lib-libX11-devel
Requires(post,postun):	glib2 >= 1:2.45.7
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-libs = %{version}-%{release}
Requires:	exempi >= 2.2.0
Requires:	gsettings-desktop-schemas
Requires:	gvfs
Requires:	hicolor-icon-theme
Requires:	json-glib >= 1.6
Requires:	libexif >= 1:0.6.20
Requires:	libnotify >= 0.7.0
%{?with_selinux:Requires:	libselinux >= 2.0}
Requires:	libxml2 >= 1:2.7.8
Requires:	cinnamon-desktop >= 4.8.0
Requires:	pango >= 1:1.44.0
Requires:	shared-mime-info
%{?with_tracker:Requires:	tracker3 >= 3.0}
Requires:	xapps >= 2.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Nemo is the file manager for the Cinnamon desktop environment. 

%description -l pl.UTF-8
Nemo to zarządca plików dla środowiska graficznego Cinnamon.

%package libs
Summary:	Library for Nemo extensions
Summary(pl.UTF-8):	Biblioteka dla rozszerzeń Nemo
License:	LGPL v2+
Group:		Development/Libraries
Requires:	glib2 >= 1:2.45.7
Requires:	gtk+3 >= 3.10.0

%description libs
This package provides the library used by Nemo view extensions.

%description libs -l pl.UTF-8
Ten pakiet dostarcza bibliotekę używaną przez rozszerzenia widoku
zarządcy plików Nemo.

%package devel
Summary:	Support for developing Nemo extensions
Summary(pl.UTF-8):	Pliki do tworzenia rozszerzeń Nemo
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.45.7
Requires:	gtk+3-devel >= 3.10.0

%description devel
This package provides the header files needed for developing Nemo
extensions.

%description devel -l pl.UTF-8
Ten pakiet dostarcza pliki nagłówkowe niezbędne do tworzenia
rozszerzeń zarządcy plików Nemo.

%package apidocs
Summary:	libnemo-extension API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libnemo-extension
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
libnemo-extension API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libnemo-extension.

%prep
%setup -q -n nemo-%{version} -a1

%{__sed} -i -e '1s,/usr/bin/env bash,/bin/bash,' search-helpers/nemo-epub2text

%build
%meson \
	%{?with_apidocs:-Dgtk_doc=true} \
	%{?with_selinux:-Dselinux=true} \
	%{?with_tracker:-Dtracker=true}

%meson_build

%{__make} -C cinnamon-translations-%{translations_version}

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

# for external extensions (see libnemo-extension.pc for path)
install -d $RPM_BUILD_ROOT%{_libdir}/nemo/extensions-3.0
install -d $RPM_BUILD_ROOT%{_datadir}/nemo/extensions

cd cinnamon-translations-%{translations_version}
for f in usr/share/locale/*/LC_MESSAGES/nemo.mo ; do
	install -D "$f" "$RPM_BUILD_ROOT/$f"
done
cd ..

# not supported by glibc 2.39
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{frp,ie,jv,mo,ksw,rue}

%find_lang nemo

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_mime_database
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_mime_database
%update_icon_cache hicolor
%glib_compile_schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f nemo.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING.EXTENSIONS NEWS README.md THANKS debian/changelog
%attr(755,root,root) %{_bindir}/nemo
%attr(755,root,root) %{_bindir}/nemo-action-layout-editor
%attr(755,root,root) %{_bindir}/nemo-autorun-software
%attr(755,root,root) %{_bindir}/nemo-connect-server
%attr(755,root,root) %{_bindir}/nemo-desktop
%attr(755,root,root) %{_bindir}/nemo-epub2text
%attr(755,root,root) %{_bindir}/nemo-mso-to-txt
%attr(755,root,root) %{_bindir}/nemo-odf-to-txt
%attr(755,root,root) %{_bindir}/nemo-open-with
%attr(755,root,root) %{_bindir}/nemo-ppt-to-txt
%attr(755,root,root) %{_bindir}/nemo-xls-to-txt
%attr(755,root,root) %{_libexecdir}/nemo-extensions-list
%{_mandir}/man1/nemo.1*
%{_mandir}/man1/nemo-connect-server.1*
%{_mandir}/man1/nemo-desktop.1*
%dir %{_libdir}/nemo
%dir %{_libdir}/nemo/extensions-3.0
%{_datadir}/dbus-1/services/nemo.FileManager1.service
%{_datadir}/dbus-1/services/nemo.service
%{_datadir}/glib-2.0/schemas/org.nemo.gschema.xml
%{_datadir}/gtksourceview-2.0/language-specs/nemo_*.lang
%{_datadir}/gtksourceview-3.0/language-specs/nemo_*.lang
%{_datadir}/gtksourceview-4/language-specs/nemo_*.lang
%{_datadir}/mime/packages/nemo.xml
%{_datadir}/nemo
%{_datadir}/polkit-1/actions/org.nemo.root.policy
%{_desktopdir}/nemo.desktop
%{_desktopdir}/nemo-autorun-software.desktop
%{_desktopdir}/nemo-autostart.desktop
%{_iconsdir}/hicolor/16x16/actions/menu-bullet.png
%{_iconsdir}/hicolor/16x16/actions/menu-none.png
%{_iconsdir}/hicolor/16x16/actions/menu-sort-*.png
%{_iconsdir}/hicolor/*x*/actions/nemo-eject.png
%{_iconsdir}/hicolor/*x*/apps/nemo.png
%{_iconsdir}/hicolor/scalable/actions/location-symbolic*.svg
%{_iconsdir}/hicolor/scalable/actions/mount-archive-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/nemo-*-symbolic*.svg
%{_iconsdir}/hicolor/scalable/actions/sidebar-*-symbolic*.svg
%{_iconsdir}/hicolor/scalable/actions/view-compact-symbolic.svg
%{_iconsdir}/hicolor/scalable/apps/nemo.svg
%{_iconsdir}/hicolor/scalable/devices/drive-removable-media-usb-symbolic.svg
%{_iconsdir}/hicolor/scalable/status/nemo-bookmark-not-found-symbolic.svg
%{_iconsdir}/hicolor/scalable/status/nemo-progress-*-symbolic.svg

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnemo-extension.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnemo-extension.so.1
%{_libdir}/girepository-1.0/Nemo-3.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnemo-extension.so
%{_includedir}/nemo
%{_datadir}/gir-1.0/Nemo-3.0.gir
%{_pkgconfigdir}/libnemo-extension.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libnemo-extension
%endif
