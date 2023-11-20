from datetime import timezone
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
import qrcode
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import EventRegistrationForm, SignUpForm, LoginForm,LoginForm_Q
from django.contrib.auth.views import LoginView
from django.contrib import messages
from qrcode.image.pil import PilImage
from io import BytesIO
import secrets
from .models import UserProfile
from django.contrib.auth.models import User
import os
import cv2
from pyzbar.pyzbar import decode
import numpy as np
from .send_without_ath import email_sender as em
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        redirect_url = '/custom_login'
        return redirect(redirect_url)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

def land(request):
    return render(request,'landing.html')

  
def custom_login(request):
    login_form = LoginForm()
    signup_form = SignUpForm()

    if request.method == 'POST':
        if 'login-submit' in request.POST:
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('event_list')  
                else:
                    messages.error(request, 'Invalid username or password')
            else:
                messages.error(request, 'Login form is not valid')
                print(form.errors)
        elif 'signup-submit' in request.POST:
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                auth_login(request, user)
                messages.success(request, 'Signup successful!')
                return redirect('event_list')
            else:
                messages.error(request, 'Signup form is not valid')
                print(form.errors)

    return render(request, 'login.html', {'login_form': login_form, 'signup_form': signup_form})



# def qr_decode(image_path):
#     image = cv2.imread(image_path)
#     decoded_objects = decode(image)
#     code = []
#     for obj in decoded_objects:
#         code.append(f'{obj.data.decode("utf-8")}')
#     return "".join(code)

# def QR_login(request):
#     if request.method == "POST":
#         image = request.FILES.get('image')
#         if image:
#             image_path = uploaded_image(image)
#             decoded_code = qr_decode(image_path)
#             try:
#                 user_profile = UserProfile.objects.get(token=decoded_code)
#                 user = user_profile.user
#                 auth_login(request, user)
#                 return redirect('home') 
#             except UserProfile.DoesNotExist:
#                 pass

#     return render(request, 'qr.html')

# def uploaded_image(image):
#     img_path = os.path.join("static", "usr", image.name)
#     with open(img_path, 'wb+') as i:
#         for chunk in image.chunks():
#             i.write(chunk)
#     return img_path
# user_profile, created = UserProfile.objects.get_or_create(user=user)
#                 new_token = secrets.token_urlsafe(200)
#                 # Ensure the generated token is unique for the user profile
#                 while UserProfile.objects.filter(id=user_profile.id, token=new_token).exists():
#                     new_token = secrets.token_urlsafe(200)
#                 user_profile.token = new_token
#                 user_profile.save()

# Updated imports
from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from django.views.decorators import gzip
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.views.decorators import gzip
from .beep import long_beep
class VideoCamera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_MSMF)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)  
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000) 
        self.qr_counts = {}
        self.detected_qr_codes = set()
        self.stopped = False

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

    def stop(self):
        self.stopped = True

    def get_frame(self):
        if not self.cap.isOpened() or self.stopped:
            return None

        ret, frame = self.cap.read()
        if not ret or frame is None or frame.size == 0:
            return None

        decoded_frame = self.decode_qr_code(frame)

        return decoded_frame

    def decode_qr_code(self, frame):
        if frame is None or frame.size == 0:
            return frame

        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            decoded_objects = decode(gray)

            for obj in decoded_objects:
                qr_data = obj.data.decode('utf-8')

                if qr_data not in self.detected_qr_codes:
                    try:
                        ticket = PurchasedTicket.objects.get(token=qr_data)
                        user = ticket.user
                        email = user.email
                        name = user.first_name
                        event_reg = event_registration.objects.get(user=user)
                        is_valid = event_reg.payment_status

                        if is_valid:
                            long_beep(1)
                            em(email, name)
                            print(user.first_name, "has registered")
                            event_reg.payment_status = False
                            event_reg.save()
                        else:
                            long_beep(3)
                            print("Qr Expired")

                        points = obj.polygon
                        if len(points) > 4:
                            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                            points = hull

                        num_of_points = len(points)
                        for j in range(num_of_points):
                            cv2.line(frame, tuple(points[j]), tuple(points[(j + 1) % num_of_points]), (0, 0, 255), 2)

                        self.qr_counts[qr_data] = self.qr_counts.get(qr_data, 0) + 1
                        self.detected_qr_codes.add(qr_data)

                    except UserProfile.DoesNotExist:
                        print(f"No user found for token: {qr_data}")

        except cv2.error as e:
            print(f"OpenCV error: {e}")

        return frame


def qr_code_decoder(request):
    template = loader.get_template('qr_code_decoder.html')
    return HttpResponse(template.render({}, request))
def gen(camera):
    while not camera.stopped:
        frame = camera.get_frame()
        if frame is not None:
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        else:
            break
    camera.__del__()
@gzip.gzip_page
def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')

def stop_stream(request):
    try:
        camera = VideoCamera()
        camera.stop()
        del camera
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})



@login_required
def event_list(request):
    event = Event.objects.all()
    current_user = request.user 
    event_ids = set(
        PurchasedTicket.objects.filter(user=current_user).values_list('event_id', flat=True)
    )
    return render(request, 'home.html', {'courses': event,'user': current_user, 'purchased_course_ids': event_ids})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Event,PurchasedTicket,event_registration
from .qr_creation import generate_qr_code as g
from .send_wit_ath import send_email_ath as sea

@login_required
def add_to_purchased(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = user
            registration.event = event
            done =False
            done = sea(user.email,user.first_name,user,event)
            if done:
                registration.save()
                return redirect('event_list')
        else:
            print(form.errors)
    else:
        form = EventRegistrationForm()

    return render(request, 'registration.html', {'form': form, 'name': user.first_name, 'event': event})


from .models import Gallery
@login_required
def gallery_view(request):
    gallery_images = Gallery.objects.all()
    unique_years = Gallery.objects.values_list('year', flat=True).distinct()
    context = {
        'gallery_images': gallery_images,
        'unique_years': unique_years,
    }
    return render(request, 'gallery.html', context)

import openpyxl
from django.shortcuts import render
from django.http import HttpResponse
from .models import PurchasedTicket, Event,event_registration
from pytz import timezone as pytz_timezone

def export_view(request):
    if request.method == 'POST':
        selected_id = request.POST.get('selectedNumber')
        purchased_list_items = PurchasedTicket.objects.filter(event_id=selected_id)
        register = event_registration.objects.filter(event_id=selected_id)
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.append(['SL No', 'Participant Name', 'Email', 'Event Name','Cost','USN','Purchase Date'])  
        for k,(i,j) in enumerate(zip(purchased_list_items,register),start=1):
            purchase_date = i.purchase_date.astimezone(pytz_timezone('Asia/Kolkata'))
            purchase_date = purchase_date.replace(tzinfo=None)
            user = get_object_or_404(User, id=i.user_id)
            event = get_object_or_404(Event,id=i.event_id)
            worksheet.append([k, user.first_name, user.email, event.event_name,event.price,j.usn,purchase_date]) 
             
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=participants.xlsx'
        workbook.save(response)
        return response
    return render(request, 'home.html')


from.send_without_ath import email_sender as es
@login_required
def remove_purchased(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user
    if request.method == 'POST':
            purchased_ticket = get_object_or_404(PurchasedTicket, user_id=user.id, event_id=event.id)
            registration = get_object_or_404(event_registration, user_id=user.id, event_id=event.id)
            purchased_ticket.delete()
            registration.delete()
            message =" Your registration has been cancelled, your payment will be refunded within next 24 hours."
            subject = "registration has been cancelled"
            es(user.email,user.first_name,message,subject)
            return redirect('event_list')
    return HttpResponse("Invalid request")

def tour(request):
    return render(request,'vtour.html')