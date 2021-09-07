from Cython.Build import cythonize
from distutils.core import setup
from distutils.extension import Extension


extension = [
    Extension("config", ["config.pyx"]),  # 配置文件
]


def compile():
    setup(ext_modules=cythonize(
        extension,
        language_level=3,
        annotate=True)
    )
