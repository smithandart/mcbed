from pathlib import Path
from PIL import Image

BED_COLORS = [
    'white',
    'silver',
    'gray',
    'black',
    'brown',
    'red',
    'orange',
    'yellow',
    'lime',
    'green',
    'cyan',
    'light_blue',
    'blue',
    'purple',
    'magenta',
    'pink'
]

BED_TOP = (256, 512) # Dimensions of the top of bed texture at 1024x1024
LEFT_UPPER = (96, 96) # Coordinate of left upper bed top for 1024x1024 bed texture
RIGHT_LOWER = (351, 607) # Coordinate of right lower bed top for 1024x1024 bed texture

def set_up():
    # Check for original_beds directory and add if it does not exist
    if not Path('original_beds').exists():
        Path.mkdir(Path('original_beds'))
        print('Created original_beds directory.')
        print('Bed textures will be needed.')

    # Check for modified_beds directory and add if it does not exist
    if not Path('modified_beds').exists():
        Path.mkdir(Path('modified_beds'))
        print('Created modified_beds directory.')

    # Check for custom_images directory and add if it does not exist
    if not Path('custom_images').exists():
        Path.mkdir(Path('custom_images'))
        print('Created custom_images directory.')


def prepare_bed(color : str) -> Image.Image:
    with Image.open(list(Path.glob(Path('original_beds'), f"{color}.*"))[0]) as img:
        return img.resize(size = (1024, 1024), resample=0)

def prepare_img(color : str) -> Image.Image:
    with Image.open(list(Path.glob(Path('custom_images'), f"{color}.*"))[0]) as img:

        if img.width > img.height / 2:
            diff = img.width - img.height / 2
            return img.resize(size = BED_TOP, box = (diff / 2, 0, img.width - diff / 2, img.height))

        if img.height > img.width * 2:
            diff = img.height - img.width * 2
            return img.resize(size = BED_TOP, box = (0, diff / 2, img.width, img.height - diff / 2))
        
        return img.resize(size = BED_TOP)

def main():
    set_up()
    for color in BED_COLORS:
        if not list(Path.glob(Path('original_beds'), f"{color}.*")):
            print(f"Missing original {color} bed texture.")
            continue

        new_bed = prepare_bed(color)

        if not list(Path.glob(Path('custom_images'), f"{color}.*")):
            print(f"Missing custom {color} image.")
            continue

        new_img = prepare_img(color)
        new_img = new_img.convert('RGBA')

        new_bed.alpha_composite(im = new_img, dest = LEFT_UPPER)
        new_bed.save(Path(f"modified_beds/{color}.png"))
        print(f"Created modified {color} bed texture.")




if __name__ == "__main__":
    main()
