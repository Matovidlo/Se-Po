The Security and portability testing framework is based on automatization of setting up virtual environment in which the code is tested. It is using both docker and vagrant to achieve easy and fast security testing and VMs for portability testing. The whole execution is made with python script that has both GUI and CLI. 

System requirements
-------------------
Tested systems are Windows and Unix like operations systems. For Unix like systems it is prerequisite to install docker and vagrant. It is important that users that are installing these tools are following guidelines. Especially in docker installation there are prerequisite steps that should be taken in order to shrink attacker surface.


- At least Python3.7
- `Docker installation <https://docs.docker.com/get-docker/>` (choose your OS).
- `CIS guideline <https://www.cisecurity.org/benchmark/docker/>` or automated OS checker 
  `CIS docker benchmark <https://github.com/dev-sec/cis-docker-benchmark>`.
- `Vagrant installation <https://www.vagrantup.com/docs/installation>` does not require specific installation except of VM provider such as virtualbox or any other.
- Vagrant plugin extensions
- `Create storage driver to run docker <https://docs.docker.com/storage/storagedriver/select-storage-driver/>` it is expected to not use overlay and devicemapper storage driver since they are deprecated.
- `Create loopback device when no other device is available (Unix like OS)<https://ops.tips/blog/lvm-on-loopback-devices/>`.
- `Setup docker group and add trusted user into group <https://docs.docker.com/engine/install/linux-postinstall/>` to avoid potential harm when using ``sudo docker`` (Unix like OS).

