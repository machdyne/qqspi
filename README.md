# QQSPI Pmod&trade; compatible module

The QQSPI module provides access to four Quad SPI devices via a 12-pin Pmod&trade; compatible interface.

![QQSPI](https://github.com/machdyne/qqspi/blob/3f11bcd27e6f9a4e80be4de0e299f313d4a9237c/qqspi.png)

This repo contains schematics, pinouts and example Verilog code for the LD-QQSPI-PSRAM32 module.

Find more information on the [LD-QQSPI-PSRAM32 product page](https://machdyne.com/product/qqspi-psram32/).

## Modes

| PMOD/SS | PMODCS0 | PMODCS1 | -> | QSPI1/CE | QSPI2/CE | QSPI3/CE | QSPI4/CE |
| ------- | ------- | ------- | -- | -------- | -------- | -------- | -------- |
| H | X | X | -> | H | H | H | H |
| L | L | L | -> | L | H | H | H |
| L | H | L | -> | H | L | H | H |
| L | L | H | -> | H | H | L | H |
| L | H | H | -> | H | H | H | L |

## Pinout

| Pin | Signal |
| --- | ------ |
| 1 | /SS (active low) |
| 2 | SIO0 (MOSI) |
| 3 | SIO1 (MISO) |
| 4 | SCK |
| 5 | GND |
| 6 | 3V3 |
| 7 | SIO2 |
| 8 | SIO3 |
| 9 | CS0 |
| 10 | CS1 |
| 11 | GND |
| 12 | 3V3 |

## License

The contents of this repo are released under the [Lone Dynamics Open License](LICENSE.md) with the following exceptions:

- The KiCad design files contain parts of the [kicad-pmod](https://github.com/mithro/kicad-pmod) library which is released under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).

- The KiCad design files may contain symbols and footprints released under other licenses; please contact us if we've failed to give proper attribution.

Note: You can use these designs for commercial purposes but we ask that instead of producing exact clones, that you either replace our trademarks and logos with your own or add your own next to ours.

