import yaml
from PIL import Image, ImageDraw, ImageFont

# Cargar el archivo YAML
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

if config["images"] is None:
    print("No images found")
    exit()

if len(config["images"]) != len(config["column_names"]):
    print("The number of titles does not match the number of columns")
    exit()


# Recortar la imagen desde el centro
def crop_center(image, crop_size):
    width, height = image.size
    new_width, new_height = crop_size
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
    return image.crop((left, top, right, bottom))


images = [
    [
        crop_center(Image.open(image_path), (config["size"], config["size"]))
        for image_path in row
    ]
    for row in config["images"]
]

# Todas las imágenes tienen el mismo tamaño
width, height = config["size"], config["size"]

cant_columns = len(images)
cant_rows = len(max(images, key=len))

spacing = 10
column_name_height = 64

# Crear una nueva imagen con el tamaño adecuado
total_width = (width + spacing) * cant_columns + spacing
total_height = (height + spacing) * cant_rows + spacing + column_name_height
new_image = Image.new("RGB", (total_width, total_height), color="white")

# Crear objeto de dibujo
draw = ImageDraw.Draw(new_image)

# Definir la fuente para los nombres de las columnas
try:
    font = ImageFont.truetype("font.ttf", column_name_height)
    print("Font loaded successfully")
except IOError:
    font = ImageFont.load_default()

# Dibujar los nombres de las columnas
for index, column in enumerate(config["column_names"]):
    draw.text(
        (
            (width + spacing) * (index)
            + (width // 2)
            - draw.textsize(column, font=font)[0] // cant_columns,
            0,
        ),
        column,
        fill="black",
        font=font,
    )

# Pegar las imágenes en la nueva imagen
for i in range(cant_rows):
    for j in range(cant_columns):
        if j < len(images) and i < len(images[j]) and images[j][i] is not None:
            new_image.paste(
                images[j][i],
                (
                    j * (width + spacing) + spacing,
                    column_name_height + spacing + i * (height + spacing),
                ),
            )

# Guardar la nueva imagen
new_image.save(config["output"] + ".jpg")
new_image.show()
