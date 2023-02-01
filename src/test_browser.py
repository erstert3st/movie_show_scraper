from Database import Database
import pytest
import random
import requests
from SeleniumScraper import SeleniumScraper
import socket
from selenium import webdriver
import undetected_chromedriver.v2 as uc
import os 
import time

def test_checkBrowser():
    print("hi")
    assert SeleniumScraper("db").checkBrowser() == True
    print(" ")


if __name__ == "__main__":
    pytest.main(["tests.py"])