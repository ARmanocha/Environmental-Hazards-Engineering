#!/bin/sh
# Downloads the COMET-LiCSAR products used in the Kīlauea 2018 example (about 40 MB) into raw/.
# Frame 124A_06996_091406: Sentinel-1 track 124, ascending. Open Government Licence v3.
set -e
F=124A_06996_091406
CEDA=https://data.ceda.ac.uk/neodc/comet/data/licsar_products/124/$F
META=https://gws-access.jasmin.ac.uk/public/nceo_geohazards/LiCSAR_products/124/$F/metadata
mkdir -p raw
for p in 20180420_20180502 20180502_20180508; do
  for x in cc diff_pha diff_unfiltered_pha unw; do
    curl -fL -o raw/$p.geo.$x.tif $CEDA/$p/$p.geo.$x.tif
  done
done
curl -fL -o raw/$F.geo.hgt.tif $META/$F.geo.hgt.tif
