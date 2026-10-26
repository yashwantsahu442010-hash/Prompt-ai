[app]
title = StudyAI Prompt Generator
package.name = studyaiprompt
package.domain = org.studyai
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,webp,atlas
version = 1.0.0
requirements = python3,kivy,requests,plyer
orientation = portrait
fullscreen = 0

[android]
android.permissions = INTERNET
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
