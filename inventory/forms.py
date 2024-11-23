from django import forms
from .models import Product, ProductVariant, Item, Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['brand', 'item', 'price', 'barcode']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['product', 'variant', 'on_hand']

    # Override the variant field to filter options based on selected product
    variant = forms.ModelChoiceField(queryset=ProductVariant.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))
                self.fields['variant'].queryset = ProductVariant.objects.filter(product_id=product_id)
            except (ValueError, TypeError):
                self.fields['variant'].queryset = ProductVariant.objects.none()
        elif self.instance.pk:
            self.fields['variant'].queryset = ProductVariant.objects.filter(product=self.instance.product)
