from setuptools import setup, find_packages

setup(
    name="loan_prediction",
    version="1.0",
    packages=find_packages(),
    python_requires='>=3.8,<3.12',
    install_requires=[
        'streamlit==1.44.1',
        'numpy==1.26.4',
        'pandas==2.2.3',
        'scikit-learn==1.3.2',
        'plotly==5.18.0',
        'seaborn==0.13.2',
        'pillow==10.2.0',
        'cython==3.0.8'
    ]
)