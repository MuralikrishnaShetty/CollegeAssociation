from pickle import TRUE
from tkinter.tix import TEXT
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm,  ProfileForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from datetime import datetime, date
from .models import Post, Finance
import smtplib
import aspose.words as aw
import os
#for downloading pdf
from django.shortcuts import render

from authenticate.models import Finance

from django.http import HttpResponse

from django.template.loader import get_template

from xhtml2pdf import pisa
def show_products(request):
    products = Finance.objects.all()

    context = {
        'products': products
    }

    return render(request, 'authenticate/showfinance.html', context)



'''def pdf_report_create(request):
    products = Finance.objects.all()

    template_path = 'authenticate/showfinance.html'

    context = {'products': products}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="products_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response '''
#end of pdf code
# Define your view here
def pdf_report_create(request):
    
	file = 'file.txt'  
	if os.path.isfile(file):
		os.remove(file)

	#print ("The file has been removed")
	finances = Finance.objects.all()
    

# Create a new Word document.
	doc = aw.Document()

# Create document builder.
	builder = aw.DocumentBuilder(doc)

# Start the table.
	table = builder.start_table()

# Insert cell.
	builder.insert_cell()

# Table wide formatting must be applied after at least one row is present in the table.
	table.left_indent = 20.0

# Set height and define the height rule for the header row.
	builder.row_format.height = 40.0
	builder.row_format.height_rule = aw.HeightRule.AT_LEAST

# Set alignment and font settings.
	builder.paragraph_format.alignment = aw.ParagraphAlignment.CENTER
	builder.font.size = 16
	builder.font.name = "Arial"
	builder.font.bold = True

	#builder.cell_format.width = 100.0
	builder.cell_format.width = 200.0
	builder.write("Date")

# We don't need to specify this cell's width because it's inherited from the previous cell.
	builder.insert_cell()
	builder.write("Time")

	builder.insert_cell()
	builder.cell_format.width = 200.0
	builder.write("posted by")
 
	builder.insert_cell()
	builder.cell_format.width = 200.0
	builder.write("Event Name")
 
	builder.insert_cell()
	builder.write("cost")
	builder.end_row()

	builder.cell_format.width = 200.0
	builder.cell_format.vertical_alignment = aw.tables.CellVerticalAlignment.CENTER

# Reset height and define a different height rule for table body.
	builder.row_format.height = 30.0
	builder.row_format.height_rule = aw.HeightRule.AUTO
	builder.insert_cell()

# Reset font formatting.
	builder.font.size = 12
	builder.font.bold = False
	count=1
	#builder.write("Row 1, Cell 2 Content")
	for  finance in finances:
     
		if count==1:
			builder.write(str(finance.date))
		else:
			builder.insert_cell()
		
			builder.write(str(finance.date))
      
		
		builder.insert_cell()
		
		builder.write(str(finance.time))

		builder.insert_cell()
		#builder.cell_format.width = 200.0
		builder.write(finance.fname+" "+finance.lname)
		
    	
		builder.insert_cell()
		#builder.cell_format.width = 200.0
		builder.write(finance.event)
  		
    
		builder.insert_cell()
		#builder.cell_format.width = 200.0
		builder.write(str(finance.cost))
		
		if count==1:
      
			builder.end_row()
			count=count+1
			continue


		
		count+=1
		
		builder.end_row()
	


		

# End table.
	builder.end_table()

# Save the document.
	doc.save("table.pdf")
	
	os.startfile("table.pdf")
	return redirect(show_finance )

# Create your views here.
def home(request): 
	return render(request, 'authenticate/home.html', {})

def login_user (request):
	if request.method == 'POST': #if someone fills out form , Post it 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:# if user exist
			login(request, user)
			messages.success(request,('Youre logged in'))
			return redirect('home') #routes to 'home' on successful login  
		else:
			messages.success(request,('Error logging in'))
			return redirect('login') #re routes to login page upon unsucessful login
	else:
		return render(request, 'authenticate/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request,('Youre now logged out'))
	return redirect('home')

def register_user(request):
	if request.method =='POST':
		form = ProfileForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ('Youre now registered'))
			return redirect('home')
	else: 
		form = ProfileForm() 
	context = {'form': form}
	return render(request, 'authenticate/register.html', context)

def edit_profile(request):
	if request.method =='POST':
		form = EditProfileForm(request.POST, instance= request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You have edited your profile'))
			return redirect('home')
	else: 		#passes in user information 
		form = EditProfileForm(instance= request.user) 

	context = {'form': form}
	return render(request, 'authenticate/edit_profile.html', context)
	#return render(request, 'authenticate/edit_profile.html',{})



def change_password(request):
	if request.method =='POST':
		form = PasswordChangeForm(data=request.POST, user= request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You have edited your password'))
			return redirect('home')
	else: 		#passes in user information 
		form = PasswordChangeForm(user= request.user) 

	context = {'form': form}
	return render(request, 'authenticate/change_password.html', context)

def no_permission(request):
	return render(request, 'authenticate/nopermission.html')

def save_post(request):
	cont = request.POST.get('post_content')
	time = datetime.now().time()
	dates = date.today()
	fname = request.user.first_name
	lname = request.user.last_name
	image= request.FILES['image']
	obj = Post(date= dates, time=time, content=cont, fname=fname, lname=lname,image=image)
	obj.save()
	recievers=[]
	for user in User.objects.all():
		recievers.append(user.email)
	sender_add='helpatwork23@gmail.com' 
	password='ipcpeapwaifigywp' 
	smtp_server=smtplib.SMTP("smtp.gmail.com",587)
	smtp_server.ehlo()
	smtp_server.starttls()
	smtp_server.ehlo() 
	smtp_server.login(sender_add,password) 
	messege = "A new Post has been added to SIT website. \nLogin to view \n\n\n\n\nRegards, \nTeam SIT"
	for user in recievers :
		try :
			smtp_server.sendmail(sender_add,user,messege)
		except:
			pass
	smtp_server.quit()
	messages.success(request, ('Your post has been saved successfully'))
	return redirect('home')

@login_required(login_url = '/login')
@user_passes_test(lambda u: u.is_staff, login_url='/nopermission')
def add_post (request):
		return render(request, 'authenticate/add_post.html')

@login_required(login_url = '/login')
def show_post (request):
	posts = Post.objects.all()
	return render(request,'authenticate/showpost.html', {'posts':posts})
	

@login_required(login_url = '/login')
@user_passes_test(lambda u: u.is_staff, login_url='/nopermission')
def add_finance (request):
		return render(request, 'authenticate/add_finance.html')
	
def save_finance(request):
	event  = request.POST.get('event')
	cost = request.POST.get('cost')
	time = datetime.now().time()
	dates = date.today()
	fname = request.user.first_name
	lname = request.user.last_name
	obj = Finance(date= dates, time=time, event=event, cost=cost, fname=fname, lname=lname)
	obj.save()	 
	recievers=[]
	for user in User.objects.all():
		recievers.append(user.email)
	sender_add='helpatwork23@gmail.com' 
	password='gkuufogsubzuqpam' 
	smtp_server=smtplib.SMTP("smtp.gmail.com",587)
	smtp_server.ehlo()
	smtp_server.starttls()
	smtp_server.ehlo() 
	smtp_server.login(sender_add,password) 
	messege = "A new finance detils has been added to SIT website. \nLogin to view \n\n\n\n\nRegards, \nTeam SIT"
	for user in recievers :
		try :
			smtp_server.sendmail(sender_add,user,messege)
		except:
			pass
	smtp_server.quit()
	messages.success(request, ('The Finance  has been saved successfully'))
	return redirect('home')

@login_required(login_url = '/login')
def show_finance (request):
	finances = Finance.objects.all()
	return render(request,'authenticate/showfinance.html', {'finances':finances})