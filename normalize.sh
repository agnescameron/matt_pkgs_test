for i in *.jsonld;
  do name=`echo "$i" | cut -d'.' -f1`
  echo "$name"
  jsonld normalize $i > "package/${name}.nt"
  cat $i | jsonld normalize | ipfs add -Q --raw-leaves | ipfs cid base32
done