[app]
title = SpideyWordle
package.name = spideygame
package.domain = org.eraygurbuz
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json,txt
version = 0.1
requirements = python3,pygame
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.archs = arm64-v8a
android.allow_backup = True
# API ayarları (GitHub Actions için en stabili)
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.accept_sdk_license = True
p4a.branch = develop
