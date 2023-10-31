# Zebra P330i Print Settings

## Troubleshooting

### Pink wrinkles show up on the ID card.
This is caused by the ribbon melting / deforming during the print process.

Turn print head resistance down using the `!R XXXX` command in the stock printer driver from Zebra (not the BarTender one). You can turn it down to up to 200 below the setting listed on the underside of the printhead (label installed by the factory). We turned ours down to 2820 from 3020, but I think we ended up turning it back to the factory default value.

Turn intensity down 20% for each color. In the Zebra driver, this means set color intensity to -20 for C, M, Y. In the BarTender Driver, this means set color intensity to 4 instead of 5 for C, M, Y.

### ID card ribbon not advancing properly.
The ribbon advance belt (red O-ring) inside the printer had gotten super janky. We had to replace ours with a ribbon we got off of amazon.

### Ribbon showing up with the wrong type.
Our knockoff Zebra ribbon that we got from Amazon had the wrong ribbon RFID chip installed on it, and was showing up as a Resin ribbon instead of a CMYKO ribbon.

### Ribbon color frames are not aligned.
Perform a ribbon color sensor calibration by running the `!SA` command on the stocker printer driver.