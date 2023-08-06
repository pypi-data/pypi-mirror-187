## Palourde

![version](https://img.shields.io/badge/version-1.0.4-blue) ![python](https://img.shields.io/badge/python-%3E=3.10-brightgreen) ![postman](https://img.shields.io/badge/postman%20collection-2.1-yellowgreen) [![Downloads](https://static.pepy.tech/badge/palourde)](https://pepy.tech/project/palourde)

Palourde converts **a v2.1 Postman Collection**,  into a **Markdown File**.


[How to export your postman collection](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/#exporting-collections)


Palourde **won't display** your private tokens and api keys.


<br>

### Installation
---

```shell
pip install palourde
```

<br>

### Usage
---

```shell
palourde demo.postman_collection.json
```

This should generate a `demo.md` file in the same folder.

See [Demos](https://github.com/bagabool/palourde/tree/main/demo).