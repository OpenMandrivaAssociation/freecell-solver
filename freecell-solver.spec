%define basen freecell-solver
%define libname_orig lib%{basen}
%define major 0
%define libname %mklibname %{basen} %{major}
%define develname %mklibname %{basen} -d
%define staticname %mklibname %{basen} -d -s


Name:		%{basen}
Summary:	The Freecell Solver Executable
Version:	3.8.0
Release:	2
License:	MIT
Group:		Games/Cards
Source:		http://download.berlios.de/fc-solve/%{name}-%{version}.tar.bz2
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root
URL:		http://fc-solve.berlios.de/
Requires:	%{libname} = %{version}-%{release}
BuildRequires:	cmake

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
Requires: %{libname} = %{version}-%{release}

%description -n %{develname}
Freecell Solver is a library for automatically solving boards of Freecell and
similar variants of card Solitaire. This package contains the header files and 
static libraries necessary for developing programs using Freecell Solver.

You should install it if you are a game developer who would like to use 
Freecell Solver from within your programs.

%package -n %{staticname}
Summary: The Freecell Solver static libraries
Group: Games/Cards
Requires: %{develname} = %{version}-%{release}

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
rm -rf %{buildroot}
cd build
%makeinstall_std

rm -f %buildroot/usr/bin/make-microsoft-freecell-board

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libfreecell-solver.so*
%{_datadir}/freecell-solver/presetrc
%{_datadir}/freecell-solver/presets/*

%files -n %{staticname}
%defattr(-,root,root)
%{_libdir}/libfreecell-solver.a

%files
%defattr(-,root,root)
%{_bindir}/fc-solve
%{_bindir}/freecell-solver-fc-pro-range-solve
%{_bindir}/freecell-solver-multi-thread-solve
%{_bindir}/freecell-solver-range-parallel-solve
%{_bindir}/make-aisleriot-freecell-board
%{_bindir}/make-gnome-freecell-board
%{_bindir}/make_pysol_freecell_board.py
%{_bindir}/pi-make-microsoft-freecell-board
%{_mandir}/*/*
%{_docdir}/*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/freecell-solver/*.h
%{_bindir}/freecell-solver-config
%{_libdir}/pkgconfig/*.pc

%clean
rm -rf %{buildroot}



%changelog
* Fri Oct 14 2011 Andrey Bondrov <abondrov@mandriva.org> 3.8.0-1mdv2012.0
+ Revision: 704677
- New version 3.8.0

* Sun Dec 19 2010 Shlomi Fish <shlomif@mandriva.org> 3.4.0-2mdv2011.0
+ Revision: 623096
- import freecell-solver

