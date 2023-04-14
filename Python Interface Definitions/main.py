from circle_module import circle

# In general .pyi files are interface definitions or stub files
# We can outsource the type hinting and documentation into a separate file
# py and pyi file should have same name
# pyi files central source for type hints and overview
# also useful if you want to provide the interfaces to someone but not the implementation
# use cases for that: not yet implemented, abstract definition without concrete implementation
# most of the time we provide pyi and py file
# for IDEs also very useful
# https://peps.python.org/pep-0484/#stub-files

# According to PEP-484
# Extension modules
# Third-party modules whose authors have not yet added type hints
# Standard library modules for which type hints have not yet been written
# Modules that must be compatible with Python 2 and 3
# Modules that use annotations for other purposes


print(circle.circumference(20))
print(circle.circumference("hello"))
