"""Views module for revenueapp."""
from unicodedata import name
from django.shortcuts import render, redirect
from django.views import View
# Django built-in edit views
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from revenueapp.models import Venue, Review
from revenueapp.forms import ReviewUpdateForm


class HomeView(View):
    def get(self, request):
        venues = Venue.objects.all()
        context ={
            'venues' : venues
        }
        
        return render(
            request=request, template_name='home.html', context=context
            )

class AboutView(View):
    def get(self, request):
        return render(request=request, template_name='about.html')

# CreateView creates a form and passes to the template 'venue_form.html'
class VenueCreateView(CreateView):
    model = Venue
    fields = '__all__'
    success_url = reverse_lazy('home')
    
# Testing foreignkey relationships in CreateView
class ReviewCreateView(CreateView):
    model = Review
    fields = '__all__'
    success_url = reverse_lazy('home')

class ReviewUpdateView(View):
    def get(self, request, pk):
        # get the review object where venue id = pk
        review = Review.objects.get(venue_id=pk)
        # create a form instance
        form = ReviewUpdateForm(instance=review)
        # pass the form to the template
        context = {'form': form}
        return render(request, 'review_update_form.html', context)
    def post(self, request, pk):
        # if the Cancel button is clicked, redirect to individual venue page where venue id = pk
        # Right now there is no URL for this, so I'm redirecting to home
        if 'Cancel' in request.POST:
            return redirect('home')
        # Otherwise, the Save button is clicked so update the review
        # Get the review object where venue id = pk
        old_review = Review.objects.get(venue_id=pk)
        # Instantiate the ModelForm with the POST data
        form = ReviewUpdateForm(request.POST, instance=old_review)
        # Save the new data
        form.save()
        return redirect('home')

