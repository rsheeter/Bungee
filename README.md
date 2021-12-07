# Bungee Spice

Derivative of DJR's Bungee ([djr.com/bungee](https://djr.com/bungee)) made to demonstrate COLRv1 gradients.

## Hacked up copy with COLRv1 gradients

This repository contains a simple hack on Bungee to add gradients for the purpose of demonstrating COLRv1.

```
python scripts/make_gradient_colrv1.py fonts/Bungee_Color_Fonts/BungeeColor-Regular_colr_Windows.ttf
```

![image](https://user-images.githubusercontent.com/6466432/145077040-422a5b03-4874-4bcc-ac72-ae8adfe0c135.png)

Note the use of two gradients in opposing direction within a single glyph. To make your own variant, perhaps going
between light and dark blue:

### Establish a virtual environment your favorite way

```
# For example
python3 -m venv venv
source venv/bin/activate
pip install fonttools
```

### Change the gradient colors

Edit `scripts/make_gradient_colrv1.py`, for example:

```python
# BEFORE, red to gold
cpal.palettes[0].append(color('#ffd700'))
cpal_red = 0
grad_c1 = cpal_red
grad_c2 = 2
cpal.numPaletteEntries = len(cpal.palettes[0])
```

```python
# AFTER, blue to pinkish
cpal.palettes[0].append(color('#4000fa'))
cpal.palettes[0].append(color('#ff095'))
cpal_red = 0
grad_c1 = 2
grad_c2 = 3
cpal.numPaletteEntries = len(cpal.palettes[0])
```

Rebuild the font binary and test the result:

```shell
python scripts/make_gradient_colrv1.py fonts/Bungee_Color_Fonts/BungeeColor-Regular_colr_Windows.ttf
python -m http.server 8010
```

Open http://localhost:8010/test.html in a browser, it should look something like this:

![image](https://user-images.githubusercontent.com/6466432/145114577-9297eaed-ffdd-4a75-9ccd-f02162328850.png)

## Specimen

TODO link when one exists :)

## License

Bungee Spice is released under the SIL Open Font License. This license is available with a FAQ at <http://scripts.sil.org/OFL>

