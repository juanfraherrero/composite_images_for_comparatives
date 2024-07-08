from PIL import Image, ImageDraw, ImageFont
import sys
import os


# Función para recortar la imagen desde el centro
def crop_center(image, crop_size):
    width, height = image.size
    new_width, new_height = crop_size
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
    return image.crop((left, top, right, bottom))


def safe_open_image(image_path, size):
    if image_path == "":
        return None
    try:
        return crop_center(Image.open(image_path), (size, size))
    except (IOError, FileNotFoundError):
        return None


def get_resource_path(relative_path):
    """Get the absolute path to the resource"""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def generateComposite(images, size, column_names, output) -> None:
    images = [
        [safe_open_image(image_path, size) for image_path in image_paths]
        for image_paths in images
    ]

    # Todas las imágenes tienen el mismo tamaño
    width, height = size, size

    cant_columns = len(images)
    cant_rows = len(max(images, key=len))

    spacing = 10  # Definir espacio entre imágenes
    col_name_height = 64  # Definir altura de los nombres de las columnas

    total_width = (width + spacing) * cant_columns + spacing
    total_height = (height + spacing) * cant_rows + spacing + col_name_height

    # Crear una nueva imagen con el tamaño adecuado
    new_image = Image.new("RGB", (total_width, total_height), color="white")

    # Crear objeto de dibujo
    draw = ImageDraw.Draw(new_image)

    # Definir la fuente para los nombres de las columnas
    try:
        font = ImageFont.truetype(get_resource_path("font.ttf"), col_name_height)
        print("Font loaded successfully")
    except IOError:
        font = ImageFont.load_default()

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
            if (
                j < len(images) and i < len(images[j]) and images[j][i] is not None
            ):  # Si hay una imagen en esa posición y si no estoy fuera de índice
                new_image.paste(
                    images[j][i],
                    (
                        j * (width + spacing) + spacing,
                        col_name_height + spacing + i * (height + spacing),
                    ),
                )

    # Guardar la nueva imagen
    new_image.save(output)
    new_image.show()
