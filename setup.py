import setuptools

setuptools.setup(
    name="pytobot",
    version="1.2.1",
    author="dmitrijkotov",
    author_email="dmitrijkotov634@mail.ru",
    description="Run script as Telegram bot",
    url="https://github.com/dmitrijkotov634/pytobot",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["pytobot=pytobot.pytobot:main"]
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3",
    install_requires=[
        "requests"
    ]
)