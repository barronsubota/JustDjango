from django.views.generic import DetailView, FormView, ListView
from django.urls import reverse
from .models import Product
from feedback.models import Feedback
from feedback.forms import FeedbackForm

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    def get_queryset(self):
        return Product.objects.all().order_by('-created_at')

class ProductDetailView(DetailView, FormView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    form_class = FeedbackForm

    def get_success_url(self):
        return reverse('products:detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # список усіх відгуків для цього продукту
        context['feedback_list'] = Feedback.objects.filter(
            product=self.object
        ).order_by('-created_at')
        return context

    def form_valid(self, form):
        # прив’язуємо новий відгук до поточного продукту
        feedback = form.save(commit=False)
        feedback.product = self.object
        if self.request.user.is_authenticated:
            feedback.user = self.request.user
        feedback.save()
        return super().form_valid(form)
