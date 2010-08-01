%define name zgv
%define version 5.9
%define release %mkrel 4

Summary:       Console-based picture viewer for many graphics formats
Name:          %{name}
Version:       %{version}
Release:       %{release}
Source0:       %{name}-%{version}.tar.bz2
Patch1:        zgv-5.6.rgb-path.patch
License:       GPL
Group:         Graphics
BuildRoot:     %{_tmppath}/%{name}-buildroot
Prefix:        %{_prefix}
BuildRequires: svgalib-devel jpeg-devel png-devel tiff-devel

%description
Zgv is a picture viewer for the linux console (svgalib), with a
thumbnail-based file selector. 

Zgv is one of the most powerful console-based image viewers
available. It uses a thumbnail-based file selector, handles both
scrolling and fit-to-window, and can be driven completely from the
keyboard (although it also has pretty spiffy mouse features for a
console app).

Zgv is closely related to xzgv, so if you're familiar with xzgv, zgv
should be a piece of cake.

If you need a good image viewer that works from the linux console, you
probably want zgv.

%prep
%setup -q
%patch1 -p0 -b .rgb-path

%build
%make

%install
rm -rf %{buildroot}

# Wow, this is an ugly hack. Thanks to the Conectiva packagers
# for getting this to work at all....

mkdir -p %{buildroot}/{%{_bindir},%{_infodir},%{_mandir}/man1}
mv src/Makefile src/Makefile.old
cat src/Makefile.old | sed -e "\
s@ -o root -g root@@g" > src/Makefile
mv etc/bin.makefile etc/bin.makefile.old
cat etc/bin.makefile.old | sed -e "\
s@ -o root -g root@@g" > etc/bin.makefile

# fix makefile
sed -i 's,$(RM).*/usr/share/man/man1/zgv.1*.*/usr/share/info/zgv*,#&,' doc/Makefile

%makeinstall \
	BINDIR=%{buildroot}/%{_bindir} \
	INFODIR=%{buildroot}/%{_infodir} \
	MANDIR=%{buildroot}/%{_mandir}/man1
chmod 644 doc/sample.zgvrc
cd %{buildroot}/%{_infodir}
mv zgv zgv.info
for a in 1 2 3 4 ; do
	mv zgv-$a zgv-$a.info
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog AUTHORS NEWS README README.fonts INSTALL TODO COPYING SECURITY doc/sample.zgvrc
%{_mandir}/man1/%{name}.1.*
%{_infodir}/%{name}*
%{_bindir}/%{name}
