from django.shortcuts import render, redirect


def partnership(request):
    return render(request, 'partnership/partnership.html')


def partnership_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        print("New partner: ", name, contact, phone, email)

    return redirect('partnership')
