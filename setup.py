from setuptools import setup, find_packages
setup(name="bluetooth-attack", version="2.0.0", author="bad-antics", description="Bluetooth/BLE exploitation and security testing", packages=find_packages(where="src"), package_dir={"": "src"}, python_requires=">=3.8")
