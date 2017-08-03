%{?scl:%scl_package atinject}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}atinject
Version:        1
Release:        24.20100611svn86.2%{?dist}
Summary:        Dependency injection specification for Java (JSR-330)
License:        ASL 2.0
URL:            http://code.google.com/p/atinject/
BuildArch:      noarch

# latest release doesn't generate javadocs and there is no source
# tarball with pom.xml or ant build file
#
# svn export -r86 http://atinject.googlecode.com/svn/trunk atinject-1
# rm -rf atinject-1/{lib,javadoc}/
# tar caf atinject-1.tar.xz atinject-1
Source0:        %{pkg_name}-%{version}.tar.xz

# These manifests based on the ones shipped by eclipse.org
Source1:        MANIFEST.MF
Source2:        MANIFEST-TCK.MF

Source3:        http://www.apache.org/licenses/LICENSE-2.0.txt

# Compile with source/target 1.5
Patch0:         %{pkg_name}-target-1.5.patch

BuildRequires:  %{?scl_prefix}javapackages-local
BuildRequires:  java-devel
BuildRequires:  %{?scl_prefix}junit

Provides:       %{?scl_prefix}javax.inject

%description
This package specifies a means for obtaining objects in such a way as
to maximize reusability, testability and maintainability compared to
traditional approaches such as constructors, factories, and service
locators (e.g., JNDI). This process, known as dependency injection, is
beneficial to most nontrivial applications.

%package        javadoc
Summary:        API documentation for %{pkg_name}

%description    javadoc
%{summary}.

%package        tck
Summary:        TCK for testing %{pkg_name} compatibility with JSR-330
Requires:       %{name} = %{version}-%{release}
Requires:       %{?scl_prefix}junit

%description    tck
%{summary}.

%prep
%setup -n %{pkg_name}-%{version} -q
cp %{SOURCE3} LICENSE
mkdir lib
build-jar-repository -p lib junit

%patch0 -p1

# Fix dep in TCK pom
sed -i -e 's/pom\.groupId/project.groupId/' tck-pom.xml

# J2EE API symlinks
%mvn_file :javax.inject atinject javax.inject/atinject

# TCK sub-package
%mvn_file :javax.inject-tck atinject-tck
%mvn_package :javax.inject-tck tck

%build
set -e
alias rm=:
alias xargs=:
alias javadoc='javadoc -Xdoclint:none'
. ./build.sh

# Inject OSGi manifests required by Eclipse.
jar umf %{SOURCE1} build/dist/javax.inject.jar
jar umf %{SOURCE2} build/tck/dist/javax.inject-tck.jar

%mvn_artifact pom.xml build/dist/javax.inject.jar
%mvn_artifact tck-pom.xml build/tck/dist/javax.inject-tck.jar

%install
%mvn_install

# Javadocs
install -d -m 755 %{buildroot}%{_javadocdir}/%{pkg_name}/tck
cp -pr build/javadoc/* %{buildroot}%{_javadocdir}/%{pkg_name}
cp -pr build/tck/javadoc/* %{buildroot}%{_javadocdir}/%{pkg_name}/tck

%files -f .mfiles
%doc LICENSE
%dir %{_javadir}/javax.inject
%dir %{_mavenpomdir}/javax.inject

%files tck -f .mfiles-tck

%files javadoc
%doc LICENSE
%{_javadocdir}/atinject

%changelog
* Thu Jun 22 2017 Michael Simacek <msimacek@redhat.com> - 1-24.20100611svn86.2
- Mass rebuild 2017-06-22

* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 1-24.20100611svn86.1
- Automated package import and SCL-ization

* Thu Feb 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1-24.20100611svn86
- Use build-classpath to symlink junit JAR

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1-23.20100611svn86
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1-22.20100611svn86
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-21.20100611svn86
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1-20.20100611svn86
- Disable javadoc doclint

* Thu Mar 12 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1-19.20100611svn86
- Add javapackages Maven coordinates to manifests

* Wed Feb 18 2015 Mat Booth <mat.booth@redhat.com> - 1-18.20100611svn86
- Add OSGi manifest to tck jar
- Install with mvn_install

* Mon Jun 09 2014 Michal Srb <msrb@redhat.com> - 1-17.20100611svn86
- Apply the "source/target 1.5" patch

* Mon Jun  9 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1-16.20100611svn86
- Compile with source/target 1.5

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-15.20100611svn86
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1-14.20100611svn86
- Use Requires: java-headless rebuild (#1067528)

* Mon Aug 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1-13.20100611svn86
- Add javax.inject provides and directory

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-12.20100611svn86
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1-11.20100611svn86
- Remove unneeded BRs
- Install missing LICENSE file
- Update to current packaging guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-10.20100611svn86
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1-9.20100611svn86
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Jul 23 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1-8.20100611svn86
- Add zip BR

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-7.20100611svn86
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 24 2012 Krzysztof Daniel <kdaniel@redhat.com> - 1-6.20100611svn86
- Added OSGi manifest.

* Mon Feb 13 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1-5.20100611svn86
- Add tck subpackage
- Use upstream build method

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-4.20100611svn86
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 10 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1-3.20100611svn86
- Use maven3 to build
- Versionless jars & javadocs

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1-2.20100611svn86
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 21 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1-1.20100611svn86
- Initial version of the package
