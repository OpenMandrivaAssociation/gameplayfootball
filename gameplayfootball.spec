%define _disable_lto 1
%define _disable_ld_no_undefined 1

%global oname GameplayFootball
%global name %(echo %oname | tr [:upper:] [:lower:])

Summary:	Football game
Name:		gameplayfootball
License:	ASL 2.0
Group:		Communications
Release:	1
Version:	0.2
URL:		http://www.linphone.org
Source0:	https://github.com/vi3itor/GameplayFootball/archive/%{version}/GameplayFootball-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	ninja
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

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n GameplayFootball-%{version}

%build
export CFLAGS="%{optflags} -O3 -fPIC"
export CXXFLAGS="%{optflags} -O3 -fPIC"
export LD_FLAGS=="%{ldflags}"
%cmake \
	-G Ninja
%ninja_build

%install
#ninja_install -C build

# binary
install -pm 0755 -d %{buildroot}/%{_bindir}/
install -pm 0755 build/%{name} %{buildroot}/%{_bindir}/

# libraries
install -pm 0755 -d %{buildroot}/%{_libdir}/
for l in libblunted2.so	\
		libdatalib.so	\
		libgamelib.so	\
		libhidlib.so	\
		libleaguelib.so	\
		libmenulib.so	\
; do
	install -pm 0755 build/$l %{buildroot}/%{_libdir}/
done

# data
install -pm 0755 -d %{buildroot}/%{_datadir}/%{name}/
install -pm 0644 data/football.config %{buildroot}/%{_datadir}/%{name}/
cp -fra data/databases %{buildroot}/%{_datadir}/%{name}/
cp -fra data/media %{buildroot}/%{_datadir}/%{name}/

