[app]
title = Super_APK
package.name = super_apk
package.domain = org.superapk

source.include_exts = py

requirements = python3,kivy==2.3.1,requests,cryptography,openai

android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21
android.archs = arm64-v8a,armeabi-v7a

requirements = python3,kivy==2.3.1,cryptography
android.permissions = INTERNET
