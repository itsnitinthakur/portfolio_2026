# portfolio/forms.py
from django import forms

from .models import ContactMessage, Product

INPUT_CLASSES = (
    "block w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-base "
    "text-slate-900 placeholder-slate-400 shadow-sm focus:border-blue-600 "
    "focus:outline-none focus:ring-2 focus:ring-blue-600/30"
)


class ContactForm(forms.ModelForm):
    # Hidden from people, filled in by bots. A filled-in value means spam.
    website = forms.CharField(required=False, label="Leave this field empty")

    class Meta:
        model = ContactMessage
        fields = [
            "name",
            "email",
            "company",
            "country",
            "phone",
            "wechat_id",
            "inquiry_type",
            "product",
            "subject",
            "message",
        ]
        labels = {
            "name": "Your name",
            "email": "Email",
            "company": "Company",
            "country": "Country",
            "inquiry_type": "What is this about?",
            "product": "Machine you're interested in (optional)",
        }
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "company": forms.TextInput(attrs={"autocomplete": "organization"}),
            "country": forms.TextInput(attrs={"autocomplete": "country-name"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel", "inputmode": "tel"}),
            "message": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "website":
                field.widget.attrs.update({"tabindex": "-1", "autocomplete": "off"})
                continue
            field.widget.attrs.setdefault("class", INPUT_CLASSES)
        self.fields["message"].widget.attrs["minlength"] = 10
        product_field = self.fields["product"]
        product_field.queryset = Product.objects.published().order_by("name")
        product_field.empty_label = "Not a specific machine"

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Please write at least a sentence or two.")
        return message

    def is_spam(self):
        return bool(self.cleaned_data.get("website"))
