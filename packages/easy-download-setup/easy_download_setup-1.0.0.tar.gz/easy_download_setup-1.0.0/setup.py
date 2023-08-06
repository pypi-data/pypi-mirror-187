from setuptools import setup
setup(
    name='easy_download_setup',
    version='1.0.0',
    description='A easy to download.',
    author='liuzihao',
    author_email='liuzihao@qwcode.top',
    license='MIT',
    project_urls={
            'Source': 'https://github.com/liuzihaohao/liuzihaohao/blob/main/easy_download.py',
    },
    py_modules=['easy_download'],
    install_requires=['retry', 'tqdm','requests','multitasking'],
    python_requires='>=3',
)