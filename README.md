# patent citation package generator

This is a test script to translate a subset of Matt Marx's [Reliance on Science dataset](https://zenodo.org/record/3755799) into JSON-LD files, which can in turn be uploaded onto the graph reduction tool [rex](https://underlay.github.io/rex/).

### installing

```

```

If you fork the script, be sure to replace the 'remote_repo' variable with a link to wherever you're storing the code online, to make sure the provenance is correct, and change the email address to yours so I don't get a snarky letter from PubMed.

```
email = 'agnesfcameron@protonmail.com'
remote_repo = "https://github.com/agnescameron/matt_pkgs_test"
```

Currently, this script is *not* very generalisable past its current use-case, particularly as it uses API calls to pull patent and publication metadata. It would be pretty straightforward to adapt this script to work on either similarly-formatted patent data, or an existing database with the required metadata already stored.

### if you want to generate .nt files

run:

```
./normalise.sh
```

on the folder you wish to normalise.