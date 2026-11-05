from setuptools import find_packages, setup

setup(
    name="arm_model_control", version="0.1.0", packages=find_packages(),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/arm_model_control"]),
        ("share/arm_model_control", ["package.xml"]),
    ],
    install_requires=["setuptools"], zip_safe=False,
    maintainer="hit", maintainer_email="hit@example.com",
    description="Model-only dual RM65 control and feedback", license="Proprietary",
    entry_points={"console_scripts": ["model_arm_node = arm_model_control.model_node:main"]},
)
