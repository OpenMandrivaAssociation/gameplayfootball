%define _disable_ld_no_undefined 1

%global oname GameplayFootball
%global name %(echo %oname | tr [:upper:] [:lower:])

Summary:	Football game
Name:		gameplayfootball
License:	ASL 2.0
Group:		Communications
Release:	1
Version:	0.2
URL:		https://www.linphone.org
Source0:	https://github.com/vi3itor/GameplayFootball/archive/%{version}/GameplayFootball-%{version}.tar.gz
Source10:	gameplayfootball.xpm
Source11:	gameplayfootball.6
Patch0:		gameplayfootball-0.2-cmake_version.patch
Patch1:		gameplayfootball-0.2-cmake_link.patch
Patch2:		gameplayfootball-0.2-cmake_install.patch
# Pardus
Patch10:	002-Config2UserHome.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	imagemagick
BuildRequires:	boost-devel
BuildRequires:	cmake(openal)
BuildRequires:	cmake(sdl2)
BuildRequires:	cmake(sdl2_image)
BuildRequires:	cmake(sdl2_ttf)
BuildRequires:	pkgconfig(directfb)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(SDL2_gfx)
BuildRequires:	pkgconfig(sqlite3)
#BuildRequires:	mesa-tools
BuildRequires:	x11vnc
BuildRequires:	x11-server-xvfb

%description
Football game, a fork of discontinued GameplayFootball
written by Bastiaan Konings Schuiling.

In 2019, Google Brain team picked up a game and created
a Reinforcement Learning environment based on it - Google
Research Football. They made some improvements to the game,
updated the libraries, but threw away everything (e.g. menus,
audio effects, etc.) that was not necessary for their task.

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_libdir}/lib*.so
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.xpm
%{_datadir}/applications/openmandriva-%{name}.desktop
%{_mandir}/man6/%{name}.6*

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n GameplayFootball-%{version}

# icon
cp %{SOURCE10} %{name}.xpm

%build
export CFLAGS="%{optflags} -O3 -fPIC"
export CXXFLAGS="%{optflags} -O3 -fPIC"
export LD_FLAGS=="%{ldflags}"
%cmake \
	-G Ninja
%ninja_build -j1

%install
%ninja_install -C build

# .desktop file
install -dm 0755 %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/openmandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
GenericName=Gameplay Football
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;
X-Vendor=OpenMandriva
EOF

# icons
for d in 16 32 48 64 72 128 256
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -background none -size "${d}x${d}" %{name}.xpm \
			%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
convert -size 32x32 %{name}.xpm \
	%{buildroot}%{_datadir}/pixmaps/%{name}.xpm

# manpage
install -pm 0755 -d %{buildroot}/%{_mandir}/man6/
install -pm 0644 %{SOURCE11} %{buildroot}/%{_mandir}/man6/

