from setuptools import setup, find_packages

setup(
    name='vibetrack',
    version='0.1.0',
    description='AI-powered Git change analyzer - Understand your code changes before pushing to GitHub!',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alireza Taheri Fakhr',
    author_email='alirezataherifakhr@gmail.com',
    url='https://github.com/alireza-taheriF/VibeTrack',
    project_urls={
        'Bug Reports': 'https://github.com/alireza-taheriF/VibeTrack/issues',
        'Source': 'https://github.com/alireza-taheriF/VibeTrack',
        'Documentation': 'https://github.com/alireza-taheriF/VibeTrack#readme',
    },
    packages=find_packages(),
    install_requires=[
        'rich>=13.0.0',
        'typer>=0.9.0',
        'requests>=2.28.0',
        'cryptography>=41.0.0'
    ],
    entry_points={
        'console_scripts': [
            'vibetrack = vibetrack.cli_en:app',
            'vt = vibetrack.cli_en:app',  # Short alias
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Environment :: Console',
    ],
    keywords='git, diff, ai, analysis, cli, developer-tools, code-review',
    python_requires='>=3.8',
    include_package_data=True,
)
