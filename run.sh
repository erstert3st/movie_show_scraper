#!/bin/bash

pytest test_browser.py || true
rm -rf /root/.config/google-chrome/Default/
unzip -o Default.zip -d /root/.config/google-chrome/
pytest test_browser.py || true


