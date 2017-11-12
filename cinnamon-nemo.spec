# NOTE: "nemo" package name is already occupied, so use cinnamon-nemo
#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc

Summary:	Nemo - file manager for Cinnamon desktop
Summary(pl.UTF-8):	Nemo - zarządca plików dla środowiska Cinnamon
Name:		cinnamon-nemo
Version:	3.4.6
Release:	2
License:	LGPL v2+ (extensions API), GPL v2+ (Nemo itself)
Group:		X11/Applications
#Source0Download: https://github.com/linuxmint/nemo/releases
Source0:	https://github.com/linuxmint/nemo/archive/%{version}/nemo-%{version}.tar.gz
# Source0-md5:	00cd89cca684ea725aca1ffd549da73f
URL:		http://cinnamon.linuxmint.com/
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1:1.11
BuildRequires:	cinnamon-desktop-devel >= 2.6.1
BuildRequires:	exempi-devel >= 2.2.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.37.3
BuildRequires:	gobject-introspection-devel >= 0.6.4
BuildRequires:	gtk+3-devel >= 3.9.10
BuildRequires:	gtk-doc >= 1.4
BuildRequires:	intltool >= 0.40.1
BuildRequires:	libexif-devel >= 1:0.6.20
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libselinux-devel >= 2.0
BuildRequires:	libxml2-devel >= 1:2.7.8
BuildRequires:	pango-devel >= 1:1.28.3
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	tracker-devel >= 1.0
BuildRequires:	xorg-lib-libX11-devel
Requires(post,postun):	glib2 >= 1:2.37.3
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-libs = %{version}-%{release}
Requires:	exempi >= 2.2.0
Requires:	gsettings-desktop-schemas
Requires:	gvfs
Requires:	hicolor-icon-theme
Requires:	libexif >= 1:0.6.20
Requires:	libnotify >= 0.7.0
Requires:	libselinux >= 2.0
Requires:	libxml2 >= 1:2.7.8
Requires:	cinnamon-desktop >= 2.6.1
Requires:	pango >= 1:1.28.3
Requires:	shared-mime-info
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
Requires:	glib2 >= 1:2.37.3
Requires:	gtk+3 >= 3.9.10

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
Requires:	glib2-devel >= 1:2.37.3
Requires:	gtk+3-devel >= 3.9.10

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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
libnemo-extension API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libnemo-extension.

%prep
%setup -q -n nemo-%{version}

%build
%{__glib_gettextize}
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-compile \
	--disable-silent-rules \
	--disable-update-mimedb \
	--enable-debug%{!?debug:=no} \
	%{?with_apidocs:--enable-gtk-doc} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

# for external extensions (see libnemo-extension.pc for path)
install -d $RPM_BUILD_ROOT%{_libdir}/nemo/extensions-3.0
install -d $RPM_BUILD_ROOT%{_datadir}/nemo/extensions

#find_lang nemo

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

%files
# -f nemo.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING.EXTENSIONS ChangeLog NEWS README.md THANKS
%attr(755,root,root) %{_bindir}/nemo
%attr(755,root,root) %{_bindir}/nemo-autorun-software
%attr(755,root,root) %{_bindir}/nemo-connect-server
%attr(755,root,root) %{_bindir}/nemo-desktop
%attr(755,root,root) %{_bindir}/nemo-open-with
%attr(755,root,root) %{_libexecdir}/nemo-convert-metadata
%attr(755,root,root) %{_libexecdir}/nemo-extensions-list
%{_mandir}/man1/nemo.1*
%{_mandir}/man1/nemo-connect-server.1*
%dir %{_libdir}/nemo
%dir %{_libdir}/nemo/extensions-3.0
%{_datadir}/dbus-1/services/org.Nemo.service
%{_datadir}/dbus-1/services/org.nemo.freedesktop.FileManager1.service
%{_datadir}/glib-2.0/schemas/org.nemo.gschema.xml
%{_datadir}/gtksourceview-2.0/language-specs/nemo_action.lang
%{_datadir}/gtksourceview-3.0/language-specs/nemo_action.lang
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
%{_iconsdir}/hicolor/48x48/status/progress-*.png
%{_iconsdir}/hicolor/scalable/actions/collapse-menu-*symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/expand-menu-*symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/location-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/sidebar-*-symbolic.svg
%{_iconsdir}/hicolor/scalable/actions/view-compact-symbolic.svg
%{_iconsdir}/hicolor/scalable/apps/nemo.svg

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
