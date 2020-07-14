# Maintainer: Michael Bleuez <michael.bleuez2@gmail.com>

pkgname='auto-ytdl-git'
pkgdesc='A youtube-dl wrapper with automatisation features'
pkgver=0.2.0
pkgrel=1
arch=('any')
url='https://github.com/michael/auto-ytdl'
license=('GPL3')
depends=('ffmpeg' 'youtube-dl')
makedepends=('python-setuptools')

md5sums=('1f617d2594296469de4f30abe8e6a756')
source=('$pkgname::http://github.com/michaelb/auto-ytdl')

build() {
  cd "$pkgname"
  python -m setuptools.launch setup.py build
}

package() {
  cd "$pkgname"
  python -m setuptools.launch setup.py install
}
