import random
from django.http import HttpResponse
from django.shortcuts import redirect, render

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout


from game.models import *
from django.contrib.auth.decorators import login_required




def index(request):
    return render(request,'game/index.html')
@login_required(login_url='login')

def game(request):
    questions = Question.objects.all()
    if len(questions) >= 5:  # Ensure there are at least 10 questions available
        selected_questions = random.sample(list(questions), 5)  # Select 10 random questions
    else:
        selected_questions = questions  # Use all available questions if there are fewer than 10
    context = {'questions': selected_questions}
    return render(request,'game/game.html',context)


from django.http import HttpResponse

def submit_quiz(request):
    if request.method == 'POST':
        score = 0
        for question in Question.objects.all():
            submitted_answer_id = request.POST.get(f'question_{question.id}')
            if submitted_answer_id:
                submitted_answer = Answer.objects.get(id=submitted_answer_id)
                if submitted_answer.is_correct:
                    score += 1

        # Formatting the score for better appearance
        score_text = f'Your score: {score} / 5'

        # Adding playful messages based on the score
        if score == 5:
            message = "Wow! You're a quiz genius! 🎉"
        elif score >= 3:
            message = "Great job! You did well! 😄"
        elif score >= 1:
            message = "Not bad! Keep practicing! 😉"
        else:
            message = "Oops! Better luck next time! 🙁"

        # Constructing a response with formatted score and message
        response = HttpResponse()
        response.write(f'<h1>{score_text}</h1>')
        response.write(f'<p>{message}</p>')
        
        # JavaScript code to trigger text-to-speech
        response.write('<script>')
        response.write('var speech = new SpeechSynthesisUtterance();')
        response.write('speech.text = "Your score is ' + str(score) + ' out of 5. ' + message + '";')
        response.write('window.speechSynthesis.speak(speech);')
        response.write('</script>')
        
        return response
    return HttpResponse("Invalid request")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')  # Redirect to home page after registration
    else:
        form = UserCreationForm()
    return render(request, 'game/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('game')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'game/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('index')  # Redirect to home page after logout




from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr
@csrf_exempt
def speech_to_text(request):
    if request.method == 'POST':
        try:
            # Initialize the recognizer
            recognizer = sr.Recognizer()

            # Capture audio from the microphone
            with sr.Microphone() as source:
                # Adjust for ambient noise
                print("Adjusting for ambient noise. Please wait...")
                recognizer.adjust_for_ambient_noise(source, duration=5)  # Adjust for 5 seconds
                print("Adjusted for ambient noise. Speak now...")

                # Capture audio
                audio = recognizer.listen(source)

            print("Recognizing...")
            # Convert audio to text using Google Web Speech API
            text = recognizer.recognize_google(audio)
            response_data = {'text': text}
            return JsonResponse(response_data)
        except sr.UnknownValueError:
            response_data = {'error': 'Sorry, could not understand audio.'}
            return JsonResponse(response_data)
        except sr.RequestError as e:
            response_data = {'error': 'Error occurred; {0}'.format(e)}
            return JsonResponse(response_data)
    else:
        response_data = {'error': 'Method not allowed.'}
        return JsonResponse(response_data, status=405)

