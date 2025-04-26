from django import forms
from .models import Place
from PIL import Image

class PlaceAdminForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'
        help_texts = {
            'image': (
                'Минимальный размер: 880x330 пикселей.'
            ),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            try:
                img = Image.open(image)
                width, height = img.size
                if width < 875 or height < 330:
                    raise forms.ValidationError(
                        f"Загруженное изображение слишком маленькое: "
                        f"{width}x{height} пикселей. "
                        "Минимальный размер — 880x330 пикселей. "
                        "Пожалуйста, загрузите изображение большего размера."
                    )
            except Exception:
                raise forms.ValidationError(
                    "Изображение должно быть не менее 880x330 пикселей."
                )
        return image