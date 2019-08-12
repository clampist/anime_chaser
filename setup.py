from setuptools import setup, find_packages


setup(
    name='anime_chaser',
    version='0.1',
    description='Anime Chaser System base on Django',
    author='clampist',
    author_email='clampist@gmail.com',
    url='https://www.xxx.com',
    license='MIT',
    packages=find_packages('anime_chaser'),
    package_dir={'': 'anime_chaser'},
    # package_data={'': [
    #     'themes/*/*/*/*',
    # ]},
    include_package_data=True,
    install_requires=[
        'django==2.2.3',
        'mysqlclient==1.4.2.post1',
        'django-ckeditor==5.4.0',
        'djangorestframework==3.9.1',
        'django-redis==4.9.0',
        'django-autocomplete-light==3.2.10',
        'mistune==0.8.4',
        'Pillow==5.2.0',
        'coreapi==2.3.3',
        'hiredis==0.2.0',
        'xadmin==2.0.1',
        'django-debug-toolbar==2.0',
        'django-silk==3.0.2',
    ],
    extras_require={
        'ipython': ['ipython==7.6.1']
    },
    scripts=[
        'anime_chaser/manage.py',
        'anime_chaser/anime_chaser/wsgi.py',
    ],
    entry_points={
        'console_scripts': [
            'anime_chaser_manage = manage:main',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language ::  Python :: 3.6',
    ]
)
