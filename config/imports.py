from pip._internal import main as pipmain

packages = [package.strip() for package in open('config/packages.txt').readlines()]

for package in packages:
	pipmain(['install', package])