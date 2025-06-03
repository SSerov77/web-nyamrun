import logging
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone


def partnership(request):
    return render(request, "partnership/partnership.html")


def partnership_submit(request):
    if request.method == "POST":
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        try:
            subject = "Новая заявка на партнерство"
            message = f"""
                Новая заявка на партнерство:

                Заведение: {name}
                Контактное лицо: {contact}
                Телефон: {phone}
                Email: {email}

                Дата: {timezone.now().strftime('%d.%m.%Y %H:%M')}
            """
            html_message = render_to_string(
                "partnership/email_partnership_text.html",
                {
                    "name": name,
                    "contact": contact,
                    "phone": phone,
                    "email": email,
                },
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                html_message=html_message,
                fail_silently=False,
            )

            messages.success(
                request,
                "Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.",
            )
        except Exception as e:
            messages.error(
                request,
                "Ошибка отправки. Попробуйте позже или свяжитесь с нами напрямую.",
            )
            logging.error(f"Ошибка отправки: {e}")

        return redirect("partnership")
