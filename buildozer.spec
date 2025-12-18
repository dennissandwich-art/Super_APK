[app]

# Application metadata
title = Super_APK
package.name = super_apk
package.domain = org.superapk

# Source configuration
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.exclude_exts = spec
source.exclude_dirs = tests, bin, .buildozer, .git, __pycache__

# Version (auto-incremented)
version = 1.0.11

# Complete requirements - NO DUPLICATES
# All dependencies properly versioned for consistency
requirements = python3==3.11.8,kivy==2.3.1,kivymd==1.1.1,requests==2.31.0,cryptography==41.0.7,openai==1.12.0,anthropic==0.18.0,feedparser==6.0.10,pillow==10.2.0,pysocks==1.7.1,stripe==7.0.0,android

# Application icon
#icon.filename = %(source.dir)s/assets/icon.png

# Presplash
#presplash.filename = %(source.dir)s/assets/presplash.png

# Android specific configuration
[app:android]

# Complete Android permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,POST_NOTIFICATIONS,NFC,USE_BIOMETRIC,WAKE_LOCK

# API levels
android.api = 31
android.minapi = 21
android.ndk = 25b

# Architectures for optimization
android.archs = arm64-v8a,armeabi-v7a

# Android SDK/NDK auto-update
android.skip_update = False
android.accept_sdk_license = True

# Gradle dependencies for modern Android features
android.gradle_dependencies = com.android.tools.build:gradle:7.4.2,androidx.core:core:1.9.0

# Enable AndroidX support
android.enable_androidx = True

# Release configuration
android.release_artifact = aab
# For release builds: buildozer android release

# Orientation
orientation = portrait

# Fullscreen
fullscreen = 0

# Presplash configuration
#android.presplash_color = #FFFFFF

# App metadata
android.meta_data = com.google.android.gms.version=@integer/google_play_services_version

# Services (if needed for background tasks)
# services = StripeWebhookService:stripe_service.py

# Bootstrap
p4a.bootstrap = sdl2

# Python for Android branch
p4a.branch = master

# Local recipes (if any custom recipes needed)
# p4a.local_recipes = ./recipes

# Logcat filters (reduce logs in production)
# android.logcat_filters = *:S python:D

# Add Java options for better performance
android.add_gradle_repositories = maven { url 'https://jitpack.io' }

# ProGuard/R8 configuration for code obfuscation
# Uncomment for production builds
# android.gradle_dependencies = com.android.tools.build:gradle:7.4.2
# Add proguard rules file:
# android.add_src = proguard-rules.pro

[buildozer]

# Build directory
build_dir = ./.buildozer

# Binary directory
bin_dir = ./bin

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Display warning if buildozer is run as root
warn_on_root = 1
