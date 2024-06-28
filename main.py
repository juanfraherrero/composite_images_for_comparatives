import yaml
from PIL import Image, ImageDraw, ImageFont

# Cargar el archivo YAML
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


# Función para recortar la imagen al centro
def crop_center(image, crop_size):
    width, height = image.size
    new_width, new_height = crop_size
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
    return image.crop((left, top, right, bottom))


images = [
    [crop_center(Image.open(image_path), (600, 600)) for image_path in row]
    for row in config["images"]
]

# Asumimos que todas las imágenes tienen el mismo tamaño
width, height = config["size"], config["size"]

cant_columns = len(images)
cant_rows = len(
    max(images, key=len)
)  # obtener la mayopr cantidad de imagenes en una columnas

# Definir espacio entre imágenes y altura para los nombres de las columnas
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
    font = ImageFont.truetype("arial.ttf", column_name_height)
    print("Font loaded successfully")
except IOError:
    font = ImageFont.load_default()

# Nombres de las columnas
column_names = config["column_names"]

print("total size", total_width, total_height)

# Dibujar los nombres de las columnas
for index, column in enumerate(column_names):
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
        new_image.paste(
            images[j][i],
            (
                j * (width + spacing) + spacing,
                column_name_height + spacing + i * (height + spacing),
            ),
        )

# Guardar la nueva imagen
new_image.save(config["output"] + ".jpg")

# Mostrar la nueva imagen (opcional)
new_image.show()
