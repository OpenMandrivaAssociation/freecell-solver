%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define staticname %mklibname %{name} -d -s

Name:		freecell-solver
Summary:	Library and application for solving Freecell card games
Version:	6.2.0
Release:	1
License:	MIT
Group:		Games/Cards
Source0:	http://fc-solve.shlomifish.org/downloads/fc-solve/%{name}-%{version}.tar.xz
Patch0:		freecell-solver-5.0-no-Lusrlib.patch
URL:		http://fc-solve.shlomifish.org/
Requires:	%{libname} = %{version}-%{release}
BuildRequires:	cmake
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	gmp-devel
BuildRequires:	gperf
BuildRequires:	make
BuildRequires:	perl(autodie)
BuildRequires:	perl(lib)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(Digest::SHA)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(lib)
BuildRequires:	perl(List::MoreUtils)
BuildRequires:	perl(parent)
BuildRequires:	perl(Path::Tiny)
BuildRequires:	perl(strict)
BuildRequires:	perl(Template)
BuildRequires:	perl(warnings)
BuildRequires:	perl-devel
BuildRequires:	python-random2
BuildRequires:	pkgconfig(python3)
BuildRequires:	python3dist(six)
Requires:	%{libname}%{?_isa} = %{version}-%{release}

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
%autosetup -p1
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
%cmake -DLOCALE_INSTALL_DIR=%{_datadir}/locale -DLIB_INSTALL_DIR=%{_libdir} -DMAX_NUM_FREECELLS=8 -DMAX_NUM_STACKS=12 -DFCS_WITH_TEST_SUITE=OFF
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
%{_bindir}/make_pysol_freecell_board.py
%{_bindir}/fc_solve_find_index_s2ints.py
%{_bindir}/find-freecell-deal-index.py
%{_bindir}/gen-multiple-pysol-layouts
%{_bindir}/transpose-freecell-board.py
%{_bindir}/pi-make-microsoft-freecell-board
%{_mandir}/*/*
%{_docdir}/*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/freecell-solver/*.h
%{_libdir}/pkgconfig/*.pc
