# Maintainer: Sébastien Luttringer

pkgname=abs-git
pkgver=$(git log -1 --pretty=format:%h)
pkgrel=$(date +%s)
pkgdesc='Archlinux Build System'
arch=('any')
url='https://github.com/seblu/abs'
license=('GPL2')
conflicts=('abs')
makedepends=('python-distribute')
depends=('python' 'python-xdg' 'bash')

package() {
  cd "$startdir"
  python setup.py install --root "$pkgdir"
}

# vim:set ts=2 sw=2 ft=sh et:
