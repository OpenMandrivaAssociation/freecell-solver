%define basen freecell-solver
%define libname_orig lib%{basen}
%define major 0
%define libname %mklibname %{basen} %{major}
%define develname %mklibname %{basen} -d
%define staticname %mklibname %{basen} -d -s


Name: %{basen}
Version: 3.4.0
Release: %mkrel 2
License: MIT
Group: Games/Cards
Source: http://download.berlios.de/fc-solve/%{name}-%{version}.tar.bz2
Buildroot: %{_tmppath}/freecell-solver-root
URL: http://fc-solve.berlios.de/
Requires: %{libname} = %{PACKAGE_VERSION}
Summary: The Freecell Solver Executable
BuildRequires: cmake

%description
The Freecell Solver package contains the fc-solve executable which is
a command-line program that can be used to solve games of Freecell and
similar card solitaire variants.

This package also contains command line executables to generate the initial
boards of several popular Freecell implementations.

%package -n %{libname}
Summary: The Freecell Solver dynamic libraries for solving Freecell games
Group: Games/Cards

%description -n %{libname}
Contains the Freecell Solver libraries that are used by some programs to solve
games of Freecell and similar variants of card solitaire.

This package is mandatory for the Freecell Solver executable too.

%package -n %{develname}
Summary: The Freecell Solver development tools for solving Freecell games
Group: Games/Cards
Requires: %{libname} = %{PACKAGE_VERSION}

%description -n %{develname}
Freecell Solver is a library for automatically solving boards of Freecell and
similar variants of card Solitaire. This package contains the header files and 
static libraries necessary for developing programs using Freecell Solver.

You should install it if you are a game developer who would like to use 
Freecell Solver from within your programs.

%package -n %{staticname}
Summary: The Freecell Solver static libraries
Group: Games/Cards
Requires: %{develname} = %{PACKAGE_VERSION}

%description -n %{staticname}
Freecell Solver is a library for automatically solving boards of Freecell and
similar variants of card Solitaire. This package contains the static libraries.

It is not generally required.

%prep
%setup -q
# This is a hack that is meant to make sure the README of the board
# generation programs resides inside the board_gen sub-dir of the 
# documentation directory.
cd board_gen
mkdir doc
cd doc
mkdir board_gen
cd board_gen
cp ../../README .


%build
%cmake -DLOCALE_INSTALL_DIR=%{_datadir}/locale -DLIB_INSTALL_DIR=%{_libdir} -DMAX_NUM_FREECELLS=8 -DMAX_NUM_STACKS=12
%make

%install
rm -rf %buildroot
cd build
%{makeinstall_std}

rm -f %buildroot/usr/bin/make-microsoft-freecell-board

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libfreecell-solver.so*
/usr/share/freecell-solver/presetrc
/usr/share/freecell-solver/presets/*

%files -n %{staticname}
%defattr(-,root,root)
%{_libdir}/libfreecell-solver.a

%files
%defattr(-,root,root)
/usr/bin/fc-solve
/usr/bin/freecell-solver-fc-pro-range-solve
/usr/bin/freecell-solver-multi-thread-solve
/usr/bin/freecell-solver-range-parallel-solve
/usr/bin/make-aisleriot-freecell-board
/usr/bin/make-gnome-freecell-board
/usr/bin/make_pysol_freecell_board.py
/usr/bin/pi-make-microsoft-freecell-board
%{_mandir}/*/*
%{_docdir}/*

%files -n %{develname}
%defattr(-,root,root)
/usr/include/freecell-solver/*.h
/usr/bin/freecell-solver-config
%{_libdir}/pkgconfig/*.pc

%clean
rm -rf $RPM_BUILD_ROOT

