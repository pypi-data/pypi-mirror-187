# Lidarutils

Codes communs aux projets Python concernant le lidar.

## Installation via Conda

- sous Windows
```
si channel non declaré dans .condarc:
    conda install lidarutils -c \\store-baie005\DATA\LidarHD\conda_channel_IGN
sinon:
    conda install lidarutils
```

- sous Unix
```
conda install lidarutils -c /media/store-baie005/DATA/LidarHD/conda_channel_IGN
```

## Construction

- sous Windows
```
ci\conda_build.bat
```
- sous Linux
```
ci\conda_build.sh
```

## Déploiement

Avant de déployer sur le channel conda, il faut idéalement changer de version (TODO: Écrire un script qui le fait)


- sous Windows
```
ci\deploy.bat
```
- sous Linux
```
ci\deploy.bat
```


