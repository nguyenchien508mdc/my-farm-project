# apps/approval/views.py
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ApprovalRequest
from .interfaces import approval_system
from .forms import ApprovalActionForm

class ApprovalListView(ListView):
    model = ApprovalRequest
    template_name = 'approval/request_list.html'
    context_object_name = 'requests'
    paginate_by = 10

    def get_queryset(self):
        """Lấy danh sách request theo vai trò người dùng"""
        if self.request.user.is_superuser:
            return ApprovalRequest.objects.all().order_by('-request_date')
        
        # Requests mà user là người phê duyệt
        qs = approval_system.get_pending_requests_for_approver(self.request.user)
        
        # Requests mà user là người tạo (tuỳ chọn)
        if self.request.GET.get('show_my_requests'):
            qs |= ApprovalRequest.objects.filter(
                requester=self.request.user
            ).order_by('-request_date')
            
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Quản lý phê duyệt")
        return context

class ApprovalDetailView(DetailView):
    model = ApprovalRequest
    template_name = 'approval/request_detail.html'
    context_object_name = 'request'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ApprovalActionForm()
        context['can_approve'] = self.object.approver == self.request.user
        return context

class ApprovalActionView(FormView):
    form_class = ApprovalActionForm
    template_name = 'approval/request_detail.html'

    def form_valid(self, form):
        request_id = self.kwargs['pk']
        action = self.kwargs['action']
        notes = form.cleaned_data['notes']

        try:
            if action == 'approve':
                approval_system.approve_request(
                    request_id=request_id,
                    approver=self.request.user,
                    response_notes=notes
                )
                messages.success(self.request, _("Đã phê duyệt yêu cầu thành công"))
            elif action == 'reject':
                approval_system.reject_request(
                    request_id=request_id,
                    approver=self.request.user,
                    response_notes=notes
                )
                messages.success(self.request, _("Đã từ chối yêu cầu thành công"))
            
            return redirect('approval:request-detail', pk=request_id)

        except Exception as e:
            messages.error(self.request, str(e))
            return redirect('approval:request-detail', pk=request_id)

# API Views
class ApprovalRequestAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status = request.GET.get('status')
        qs = approval_system.get_pending_requests_for_approver(request.user)
        
        if status:
            qs = qs.filter(status=status)
            
        data = [{
            'id': req.id,
            'type': req.get_request_type_display(),
            'status': req.get_status_display(),
            'requester': req.requester.username,
            'created': req.request_date,
            'object': str(req.related_object)
        } for req in qs]
        
        return Response(data)

class ApprovalActionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, action):
        try:
            if action == 'approve':
                req = approval_system.approve_request(
                    request_id=pk,
                    approver=request.user,
                    response_notes=request.data.get('notes', '')
                )
            elif action == 'reject':
                req = approval_system.reject_request(
                    request_id=pk,
                    approver=request.user,
                    response_notes=request.data.get('notes', '')
                )
            else:
                return Response({'error': 'Invalid action'}, status=400)
            
            return Response({
                'status': 'success',
                'new_status': req.get_status_display()
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=400)