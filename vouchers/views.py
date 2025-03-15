from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView
from .models import voucher  # Certifique-se de que o modelo Voucher existe
# vouchers/views.py
from django.views.generic import ListView
from .models import voucher
from datetime import timedelta
from django.utils import timezone
class VoucherListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = voucher
    template_name = 'voucher_list.html'
    context_object_name = 'vouchers'
    permission_required = 'vouchers.view_voucher'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        
        # Atualiza vouchers que foram criados há mais de 24 horas e estão com status "Ativo"
        from datetime import timedelta
        from django.utils import timezone
        expired_threshold = timezone.now() - timedelta(hours=24)
        qs.filter(data__lte=expired_threshold, status="Ativo").update(status="Expirado")
        
        user = self.request.user
        # Se for superusuário, vê todos os vouchers
        if user.is_superuser:
            filtered = qs
        else:
            userprofile = getattr(user, 'userprofile', None)
            if userprofile:
                filtered = qs.filter(rota__in=userprofile.rotas.all()).distinct()
            else:
                filtered = qs.none()
        return filtered

   
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import voucher
from .forms import VoucherForm

class VoucherCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = voucher
    form_class = VoucherForm
    template_name = 'voucher_create.html'
    success_url = reverse_lazy('voucher')  # Ajuste para onde quiser redirecionar após salvar
    permission_required = 'vouchers.add_voucher'


from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import voucher

class VoucherDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = voucher
    template_name = 'vouchers/voucher_confirm_delete.html'
    success_url = reverse_lazy('voucher')  # Para onde redirecionar após excluir
    permission_required = 'vouchers.change_voucher'

from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .forms import VoucherUpdateForm

class VoucherUpdateView(LoginRequiredMixin,UpdateView):
    model = voucher
    form_class = VoucherUpdateForm  # Usa o form COM gasto
    template_name = 'voucher_update.html'
    success_url = reverse_lazy('voucher')
    
    
from django.shortcuts import get_object_or_404, redirect
from .models import voucher
from django.contrib import messages

def voucher_activate_status(request, pk):
    voucher_obj = get_object_or_404(voucher, pk=pk)
    # Verifica se o status atual é "Pendente" antes de alterar
    if voucher_obj.status == "Pendente":
        voucher_obj.status = "Ativo"
        voucher_obj.save()
        messages.success(request, "Status alterado para Ativo.")
    else:
        messages.info(request, "O voucher já está ativo ou com outro status.")
    return redirect('voucher')  # Redireciona para a página de lista ou detalhe
