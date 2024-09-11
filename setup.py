from setuptools import setup, find_packages

setup(
    name='alglin_projeto_3',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
    ],
    entry_points={
        'console_scripts': [
            'demo = camera.camera:run',
        ],
    },
    author='Vitor Raia e Pedro Fardin',
    description='Processador de vídeo em tempo real com rotação de imagem',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vitorraiaa/alglin_projeto_3.git',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
